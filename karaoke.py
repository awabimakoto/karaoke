#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector, os
from subprocess import Popen
from Tkinter import *
cnx=mysql.connector.connect(user=os.getenv('USER'),database='karaoke')
cursor=cnx.cursor()
p=None
area=''
gender=''
singer=''
song=''
language=''
arealist={u'日本':0,u'大陆':1,u'港台':2,u'其他':3}
genderlist={u'乐队组合':0,u'男歌手':1,u'女歌手':2}
languagelist={0:u'日语',1:u'国语',2:u'粤语',3:u'闽南语',4:u'英语',5:u'其他'}
languagereverse={u'日语':0,u'国语':1,u'粤语':2,u'闽南语':3,u'英语':4,u'其他':5}

def player():
    global listcurrent,p
    root.after(1000,player)
    ps=os.popen("ps -A").read()
    count=ps.count("vlc")
    if count==0 and listcurrent.size():
        id=listcurrent.get(0)[0]
        query="select url from karaoke where id="+str(id)
        cursor.execute(query)
        for item in cursor:
            url=item[0]
        realurl=os.popen("youtube-dl -g "+url).read()
        realurl='"%s"'%realurl.rstrip()
        p=Popen('vlc '+realurl+' vlc://quit',shell=True)
        listcurrent.delete(0)
    else:
        try:
            p.poll()
        except:
            pass
        return None

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
    global area,gender,singer,song,language,listcurrent
    if len(song):
       query="select id,song,singer,language from karaoke where area='"+str(arealist.get(area))+"' and gender='"+str(genderlist.get(gender))+"' and singer='"+singer+"' and song='"+song+"' and language="+str(language)
       cursor.execute(query)
       for item in cursor:
           listcurrent.insert(END,(item[0],item[1],item[2],languagelist[item[3]]))
    else:
        return None

def skip():
    global p
    p.terminate()
    os.wait()

def top():
    global listcurrent
    pos=listcurrent.curselection()
    if pos:
        position=pos[0]
        content=tuple(listcurrent.selection_get().split())
        listcurrent.delete(pos)
        listcurrent.insert(0,content)
    else:
        return None

root=Tk()
root.after(1000,player)
var=StringVar()
status=Label(root,textvariable=var).pack(side=LEFT)
listselect=Listbox(root)
listselect.pack(side=LEFT)
listselect.bind("<<ListboxSelect>>",lambda x:choose(listselect.selection_get()))
current=Label(root,text="播放列表")
current.pack(side=RIGHT)
listcurrent=Listbox(root)
listcurrent.pack(side=RIGHT)
buttonarea=Button(root,text="地区",command=lambda:select('地区'))
buttongender=Button(root,text="类型",command=lambda:select('类型'))
buttonsinger=Button(root,text="歌手",command=lambda:select('歌手'))
buttonsong=Button(root,text="歌曲",command=lambda:select('歌曲'))
buttonadd=Button(root,text="点",bg="green",command=add)
buttonskip=Button(root,text="切",bg="yellow",command=skip)
buttontop=Button(root,text="顶",bg="red",command=top)
buttonarea.pack()
buttongender.pack()
buttonsinger.pack()
buttonsong.pack()
buttonadd.pack()
buttonskip.pack()
buttontop.pack()
root.mainloop()
cursor.close()
cnx.close()
