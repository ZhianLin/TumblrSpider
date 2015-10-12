import re
import os
import urllib
import socket
import time
import sys

from libs.fileutils import FileUtils
from libs.config import Config


class TumblrSpider:
    RETRY_LIMIT = 5

    def __init__(self, blog, fileTypes):
        self.blog = blog
        self.baseUrl = 'http://%s.tumblr.com/page/' % self.blog
        self.dir = sys.path[0] + os.sep + blog
        self.fileTypes = fileTypes

        self.goHunting = True
        self.tempFile = self.dir + os.sep + 'downloading.tmp'

    def run(self):
        """ Main function. """
        FileUtils.mkdir(self.dir)
        self.__crawl()

    def __crawl(self):
        """ Crawl blog page by page. """
        print 'Start crawling blog [%s]' % self.blog
        page = 1
        while self.goHunting:
            self.__crawlPage(page)
            page += 1

    def __crawlPage(self, page):
        """ Crawl a single page. """
        print 'Connecting page %d......' % page
        url = self.__assemblePageUrl(page)
        pageSrc = self.__readPage(url)
        links = self.__findAllLinks(pageSrc)
        print '%s link(s) found' % len(links)
        self.__retrieveAll(links)

    def __assemblePageUrl(self, page):
        return '%s%d' % (self.baseUrl, page)

    def __readPage(self, url):
        """ Read page's source code. """
        page = None

        for i in range(5):
            try:
                response = urllib.urlopen(url)
                page = response.read()
                response.close()
            except:
                print 'Connection timeout, retry in 5s......'
                time.sleep(5)
            else:
                break

        if not page:
            abort('Connection failed, spider abort.')
        else:
            return page

    def __findAllLinks(self, page):
        """ Match all download links from source code. """
        # regex written by xiyoulaoyuanjia@Github
        regex = r'(http://[0-9]{0,5}\.media\.tumblr\.com/([a-z]|[A-Z]|[0-9]){32}.*\.(%s))' % '|'.join(self.fileTypes)
        result = re.findall(regex, page)

        links = []

        for match in result:
            links.append(match[0])

        return links

    def __retrieveAll(self, links):
        for i in range(len(links)):
            if not self.goHunting:
                return

            print 'Downloading: %d/%d' % (i + 1, len(links))
            self.__retrieve(links[i])

    def __retrieve(self, link):
        filename = self.__splitResourceName(link)

        if FileUtils.fileExists(filename):
            print 'File already exists, spider abort'
            self.goHunting = False
            return
        else:
            path = self.dir + os.sep + filename
            self.__download(link, path)

    def __splitResourceName(self, url):
        """ Split filename from url. """
        return url.split('/')[-1]

    def __download(self, url, saveTo):
        for i in range(TumblrSpider.RETRY_LIMIT):
            try:
                FileUtils.createFile(self.tempFile)
                urllib.urlretrieve(url, self.tempFile)
                os.rename(self.tempFile, saveTo)
            except:
                print 'Connection timeout, retry in 5s......'
                time.sleep(5)
            else:
                break


def abort(prompt):
    print prompt
    raw_input('Press Enter to exit')
    exit()


if __name__ == '__main__':
    socket.setdefaulttimeout(30)

    config = Config()
    dic = config.readConfig()

    for blog in dic['blogs']:
        spider = TumblrSpider(blog, dic['fileTypes'])
        spider.run()

    abort('Done.')
