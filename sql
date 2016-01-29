CREATE TABLE `karaoke` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `song` tinytext NOT NULL,
  `singer` tinytext NOT NULL,
  `area` integer NOT NULL,	//0:日本 1:大陆 2:港台 3:其他
  `gender` integer NOT NULL,	//0:乐队组合 1:男歌手 2:女歌手
  `language` integer NOT NULL,	//0:日语 1:国语 2:粤语 3:闽南语 4:英语 5:其他
  `url` text NOT NULL	 //Youtube url
);