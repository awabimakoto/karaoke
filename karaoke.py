#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3, os
from Tkinter import *
import vlc
cnx=sqlite3.connect('karaoke.db')
cursor=cnx.cursor()
area=''
gender=''
singer=''
song=''
language=''
arealist={u'日本':0,u'大陆':1,u'港台':2,u'其他':3}
genderlist={u'乐队组合':0,u'男歌手':1,u'女歌手':2}
languagelist={0:u'日语',1:u'国语',2:u'粤语',3:u'闽南语',4:u'英语',5:u'其他'}
languagereverse={u'日语':0,u'国语':1,u'粤语':2,u'闽南语':3,u'英语':4,u'其他':5}
i=vlc.Instance()
l=i.media_list_new()
p=i.media_list_player_new()
P=i.media_player_new()
p.set_media_list(l)
p.set_media_player(P)
P.set_fullscreen(True)

def player():
    global p
    p.play()

def select(type):
    global var,listselect,area,gender,singer,song
    var.set(type)
    listselect.delete(0,END)
    if type=='地区':
        for item in arealist:
            listselect.insert(END,item)
    elif type=='类型':
        for item in genderlist:
            listselect.insert(END,item)
    elif type=='歌手':
        query="select distinct singer from karaoke where area='"+str(arealist.get(area))+"' and gender='"+str(genderlist.get(gender))+"' order by singer"
        cursor.execute(query)
        for item in cursor:
            listselect.insert(END,item)
    elif type=='歌曲':
        query="select song,language from karaoke where area='"+str(arealist.get(area))+"' and gender='"+str(genderlist.get(gender))+"' and singer='"+singer+"' order by song"
        cursor.execute(query)
        for item in cursor:
            listselect.insert(END,(item[0],languagelist[item[1]]))
    else:
        pass

def choose(selection):
    global var,area,gender,singer,song,language
    if var.get()==u'地区':
        area=selection
    elif var.get()==u'类型':
        gender=selection
    elif var.get()==u'歌手':
        singer=selection
    elif var.get()==u'歌曲':
        song=selection.split()[0]
        language=languagereverse.get(selection.split()[1])
    else:
        pass

def add():
    global area,gender,singer,song,language,listcurrent,l,p
    if len(song):
       query="select id,song,singer,language,url from karaoke where area='"+str(arealist.get(area))+"' and gender='"+str(genderlist.get(gender))+"' and singer='"+singer+"' and song='"+song+"' and language="+str(language)
       cursor.execute(query)
       for item in cursor:
           realurl=os.popen("youtube-dl -g "+item[4]).read()
           if len(realurl):
               listcurrent.insert(END,(item[0],item[1],item[2],languagelist[item[3]]))
               realurl="%s"%realurl.rstrip()
               l.add_media(i.media_new(realurl))
    else:
        return None
    if p.get_state()!=3:
        p.play()

def skip():
    global p
    p.next()

def channel():
    global P
    channelmap={1:3,3:4,4:1}
    currentchannel=P.audio_get_channel()
    targetchannel=channelmap[currentchannel]
    P.audio_set_channel(targetchannel)

root=Tk()
root.title("karaoke")
root.after(1000,player)
var=StringVar()
status=Label(root,textvariable=var).pack(side=LEFT)
frameselect=Frame(root)
scrollselect=Scrollbar(frameselect,orient=VERTICAL)
listselect=Listbox(frameselect,yscrollcommand=scrollselect.set)
scrollselect.config(command=listselect.yview)
scrollselect.pack(side=RIGHT,fill=Y)
listselect.pack(side=LEFT,fill=BOTH,expand=1)
frameselect.pack(side=LEFT)
listselect.bind("<<ListboxSelect>>",lambda x:choose(listselect.selection_get()))
current=Label(root,text="播放列表")
current.pack(side=RIGHT)
framecurrent=Frame(root)
scrollcurrent=Scrollbar(framecurrent,orient=VERTICAL)
listcurrent=Listbox(framecurrent,yscrollcommand=scrollcurrent.set)
scrollcurrent.config(command=listcurrent.yview)
scrollcurrent.pack(side=RIGHT,fill=Y)
listcurrent.pack(side=LEFT,fill=BOTH,expand=1)
framecurrent.pack(side=RIGHT)
buttonarea=Button(root,text="地区",command=lambda:select('地区'))
buttongender=Button(root,text="类型",command=lambda:select('类型'))
buttonsinger=Button(root,text="歌手",command=lambda:select('歌手'))
buttonsong=Button(root,text="歌曲",command=lambda:select('歌曲'))
buttonadd=Button(root,text="点",bg="green",command=add)
buttonskip=Button(root,text="切",bg="yellow",command=skip)
buttonchannel=Button(root,text="原唱/伴奏",bg="blue",command=channel)
buttonarea.pack()
buttongender.pack()
buttonsinger.pack()
buttonsong.pack()
buttonadd.pack()
buttonskip.pack()
buttonchannel.pack()
root.mainloop()
cursor.close()
cnx.close()
