# TumblrSpider
逐页爬取多个汤站博客中指定的多个文件类型。

Download all files in indicated extensions from indicated Tumblr blogs page by page. 

タンブラー上のエロい画像をダウンロードする。日本語苦手だから笑わないで。

---

##配置：

预置范(tuī)例(jiàn)：

	Blog=nondenete|eeekou
	FileType=jpg|png|gif

Blog对应的是需要爬取的博客。

FileType对应的是文件类型也即扩展名。

暂时没有排错处理，请不要自己创造其他配置方式。

---

##使用：

直接启动tumblrspider.py，会按照博客分别创建不同的文件夹并下载到各自的文件夹里。

爬取过程中发现文件存在则终止当前博客的爬取，所以可以使用计划任务每天爬取新内容。

######日志丑哭了我知道的。

---