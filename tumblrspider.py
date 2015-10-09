#coding:utf-8

'''
配置文件的多个键值用|分割，目前只支持博客和文件类型两种设置项，请参考预置内容配置。
修改配置文件的格式可能导致不可预料的后果。
'''
import re, os
import urllib
import socket
import time

configFile = 'config.txt'

def initConfigFile():
    ''' 初始化配置文件。 '''
    f = file(configFile, 'w')
    
    blogs = ['nondente', 'eeekou']
    fileTypes = ['jpg', 'png', 'gif']
    
    blogsStr = '|'.join(blogs)
    fileTypesStr = '|'.join(fileTypes)
    
    f.write('Blog=%s\n' %blogsStr)
    f.write('FileType=%s\n' %fileTypesStr)
    
    f.close()
        
def readConfig():
    ''' 读取配置文件。 '''
    if not os.path.isfile(configFile):
        initConfigFile()
    
    f = file(configFile, 'r')
    
    configFileContent = ''.join(f.readlines())
    
    blogsStr = re.search('Blog=(.*)\n', configFileContent).group(1)
    fileTypesStr = re.search('FileType=(.*)\n', configFileContent).group(1)
    
    blogs = blogsStr.split('|')
    fileTypes = fileTypesStr.split('|')
    
    dic = {'blogs': blogs, 'fileTypes': fileTypes}
    
    f.close()
    
    return dic

def quit(prompt):
    ''' 退出程序。 '''
    print prompt
    raw_input('按回车键退出')
    exit()

class TumblrSpider:
    def __init__(self, blog, fileTypes):
        self.blog = blog
        self.baseUrl = 'http://%s.tumblr.com/page/' %self.blog
        self.dir = blog
        self.fileTypes = fileTypes
        
        self.goHunting = True
        
    def __assemblePageUrl(self, page):
        ''' 拼装指定页面的URL。'''
        return '%s%d' %(self.baseUrl, page)
    
    def crawl(self):
        ''' 爬取所有配置文件中指定的文件类型。'''
        if not os.path.isdir(self.dir):
                    os.mkdir(self.dir)
        
        print '开始爬取%s的博客……' %self.blog
        
        page = 1
        while self.goHunting and page < 500:
            url = self.__assemblePageUrl(page)
            
            print '准备爬取第%d页……' %page
            self.__crawlAPage(url)
        
            page += 1
    
    def __crawlAPage(self, url):
        ''' 爬取一页中所有指定文件类型。'''
        page = self.__readPage(url)
        links = self.__findAllLinks(page)
        self.__retrieveAll(links)
        
    def __readPage(self, url):
        ''' 读取页面源代码。 '''
        for i in range(5):
            try:
                print '正在连接页面……'
                response = urllib.urlopen(url)
                page = response.read()
                response.close()
            except:
                print '连接超时，五秒后重试……'
                time.sleep(5)
            else:
                break
        
        if not page:
            quit('页面连接失败')
        else:
            return page
        
        
        
    def __findAllLinks(self, page):
        ''' 从页面源代码中匹配出所有下载链接。 '''
        
#        regex = r'(http.*\.(%s)).*Zoom' %'|'.join(self.fileTypes)
#        regex = r'(http.*\.media\.tumblr\.com/([a-z]|[A-Z]|[0-9]){32}\.(%s))' %'|'.join(self.fileTypes)
        regex = r'(http://[0-9]{0,5}\.media\.tumblr\.com/([a-z]|[A-Z]|[0-9]){32}.*\.(%s))' %'|'.join(self.fileTypes)
        result = re.findall(regex, page)
        
        links = []
        
        for match in result:
            links.append(match[0])
            
        print '找到了%d个下载链接。' %len(links)
        return links
        
    def __retrieveAll(self, links):
        ''' 下载所有文件。 '''
        for i in range(len(links)):
            print '正在下载:%d/%d' %(i+1, len(links))
            fileName = self.__splitResourceName(links[i])
            path = self.dir+os.sep+fileName
            
            if os.path.isfile(path):
                print '文件已存在，爬取终止。'
                self.goHunting = False
                break;
            else:
                self.__retrieve(links[i], path)
                
    def __retrieve(self, url, path):
        ''' 下载单个文件到指定目录。 '''
        for i in range(5):
            try:
                urllib.urlretrieve(url, path)
            except:
                print '连接超时，五秒后重试……'
                time.sleep(5)
            else:
                break;
            
    def __splitResourceName(self, url):
        ''' 从Url中提取文件名。 '''
        return url.split('/')[-1]
        

if __name__ == '__main__':
    socket.setdefaulttimeout(30)
    
    dic = readConfig()
    
    for blog in dic['blogs']:
        spider = TumblrSpider(blog, dic['fileTypes'])
        spider.crawl()
        
    quit('下载完毕。')
