# coding:utf-8

import re
import os
import urllib
import socket
import time
import sys
import tempfile


class TumblrSpider:
    RETRY_LIMIT = 5

    def __init__(self, blog, fileTypes):
        self.blog = blog
        self.baseUrl = 'http://%s.tumblr.com/page/' % self.blog
        self.dir = sys.path[0] + os.sep + blog
        self.fileTypes = fileTypes

        self.goHunting = True

    def run(self):
        """ 主函数，爬取指定博客。 """
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        self.__crawl()

    def __crawl(self):
        """ 逐页爬取博客内容。 """
        print u'开始爬取 %s 的博客\n' % self.blog
        page = 1
        while self.goHunting:
            self.__crawlPage(page)
            page += 1
            print

    def __crawlPage(self, page):
        """ 爬取单页内容 """
        print u'尝试连接第 %d 页……' % page
        url = self.__assemblePageUrl(page)
        pageSrc = self.__readPage(url)
        links = self.__findAllLinks(pageSrc)
        print u'找到了 %d 个下载链接' % len(links)
        self.__retrieveAll(links)

    def __assemblePageUrl(self, page):
        """ 拼装页面URL。 """
        return '%s%d' % (self.baseUrl, page)

    def __readPage(self, url):
        """ 读取页面源代码。 """
        page = None

        for i in range(5):
            try:
                response = urllib.urlopen(url)
                page = response.read()
                response.close()
            except:
                print u'连接超时，五秒后重试……'
                time.sleep(5)
            else:
                break

        if not page:
            abort(u'连接失败，终止爬取。')
        else:
            return page

    def __findAllLinks(self, page):
        """ 从页面源码中匹配出所有下载链接。 """
        # regex written by xiyoulaoyuanjia@Github
        regex = r'(http://[0-9]{0,5}\.media\.tumblr\.com/([a-z]|[A-Z]|[0-9]){32}.*\.(%s))' % '|'.join(self.fileTypes)
        result = re.findall(regex, page)

        links = []

        for match in result:
            links.append(match[0])

        return links

    def __retrieveAll(self, links):
        """ 下载所有链接。 """
        for i in range(len(links)):
            if not self.goHunting:
                return

            for j in range(TumblrSpider.RETRY_LIMIT):
                try:
                    print u'开始下载 %d/%d' % (i + 1, len(links))
                    self.__retrieve(links[i])
                except:
                    print u'连接超时，五秒后重试……'
                    time.sleep(5)
                else:
                    break

    def __retrieve(self, link):
        """ 下载单个链接。 """
        filename = self.__splitResourceName(link)

        if os.path.isfile(filename):
            print u'文件已存在，终止爬取。'
            self.goHunting = False
            return
        else:
            path = self.dir + os.sep + filename
            self.__download(link, path)

    def __splitResourceName(self, url):
        """ 从下载链接中切分出文件名。 """
        return url.split('/')[-1]

    def __download(self, url, saveTo):
        """ 下载文件。 """
        tmp = tempfile.mktemp(".tmp")
        urllib.urlretrieve(url, tmp)
        os.rename(tmp, saveTo)


class Config:
    """ 爬虫配置。 """
    CONFIG_FILE = sys.path[0] + os.sep + 'config.txt'

    def initConfigFile(self):
        """ 初始化配置文件。 """
        f = file(Config.CONFIG_FILE, 'w')

        blogs = ['bokuwachikuwa', 'wnderlst']
        fileTypes = ['jpg', 'png', 'gif']

        blogsStr = '|'.join(blogs)
        fileTypesStr = '|'.join(fileTypes)

        f.write('Blog=%s\n' % blogsStr)
        f.write('FileType=%s\n' % fileTypesStr)

        f.close()

    def readConfig(self):
        """ 读取配置文件。 """
        if not os.path.isfile(Config.CONFIG_FILE):
            self.initConfigFile()

        f = file(Config.CONFIG_FILE, 'r')

        configFileContent = ''.join(f.readlines())

        blogsStr = re.search('Blog=(.*)\n', configFileContent).group(1)
        fileTypesStr = re.search('FileType=(.*)\n', configFileContent).group(1)

        blogs = blogsStr.split('|')
        fileTypes = fileTypesStr.split('|')

        dic = {'blogs': blogs, 'fileTypes': fileTypes}

        f.close()

        return dic


def abort(prompt):
    """ 退出程序。 """
    print prompt
    raw_input(u'按回车键退出')
    exit()


if __name__ == '__main__':
    socket.setdefaulttimeout(10)

    config = Config()
    dic = config.readConfig()

    for blog in dic['blogs']:
        spider = TumblrSpider(blog, dic['fileTypes'])
        spider.run()
        print

    abort(u'下载完毕。')
