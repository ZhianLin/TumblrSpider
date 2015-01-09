#coding:gbk

'''
�����ļ��Ķ����ֵ��|�ָĿǰֻ֧�ֲ��ͺ��ļ����������������ο�Ԥ���������á�
�޸������ļ��ĸ�ʽ���ܵ��²���Ԥ�ϵĺ����
'''
import re, os
import urllib
import socket
import time

configFile = 'config.txt'

def initConfigFile():
    ''' ��ʼ�������ļ��� '''
    f = file(configFile, 'w')
    
    blogs = ['nondente', 'eeekou']
    fileTypes = ['jpg', 'png', 'gif']
    
    blogsStr = '|'.join(blogs)
    fileTypesStr = '|'.join(fileTypes)
    
    f.write('Blog=%s\n' %blogsStr)
    f.write('FileType=%s\n' %fileTypesStr)
    
    f.close()
        
def readConfig():
    ''' ��ȡ�����ļ��� '''
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
    ''' �˳����� '''
    print prompt
    raw_input('���س����˳�')
    exit()

class TumblrSpider:
    def __init__(self, blog, fileTypes):
        self.blog = blog
        self.baseUrl = 'http://%s.tumblr.com/page/' %self.blog
        self.dir = blog
        self.fileTypes = fileTypes
        
        self.goHunting = True
        
    def __assemblePageUrl(self, page):
        ''' ƴװָ��ҳ���URL��'''
        return '%s%d' %(self.baseUrl, page)
    
    def crawl(self):
        ''' ��ȡ���������ļ���ָ�����ļ����͡�'''
        if not os.path.isdir(self.dir):
                    os.mkdir(self.dir)
        
        print '��ʼ��ȡ%s�Ĳ��͡���' %self.blog
        
        page = 1
        while self.goHunting:
            url = self.__assemblePageUrl(page)
            
            print '׼����ȡ��%dҳ����' %page
            self.__crawlAPage(url)
        
            page += 1
    
    def __crawlAPage(self, url):
        ''' ��ȡһҳ������ָ���ļ����͡�'''
        page = self.__readPage(url)
        links = self.__findAllLinks(page)
        self.__retrieveAll(links)
        
    def __readPage(self, url):
        ''' ��ȡҳ��Դ���롣 '''
        for i in range(5):
            try:
                print '��������ҳ�桭��'
                response = urllib.urlopen(url)
                page = response.read()
                response.close()
            except:
                print '���ӳ�ʱ����������ԡ���'
                time.sleep(5)
            else:
                break
        
        if not page:
            quit('ҳ������ʧ��')
        else:
            return page
        
        
        
    def __findAllLinks(self, page):
        ''' ��ҳ��Դ������ƥ��������������ӡ� '''
        
        regex = r'(http.*\.(%s)).*Zoom' %'|'.join(self.fileTypes)
        result = re.findall(regex, page)
        
        links = []
        
        for match in result:
            links.append(match[0])
            
        print '�ҵ���%d���������ӡ�' %len(links)
        return links
        
    def __retrieveAll(self, links):
        ''' ���������ļ��� '''
        for i in range(len(links)):
            print '��������:%d/%d' %(i+1, len(links))
            fileName = self.__splitResourceName(links[i])
            path = self.dir+os.sep+fileName
            
            if os.path.isfile(path):
                print '�ļ��Ѵ��ڣ���ȡ��ֹ��'
                self.goHunting = False
                break;
            else:
                self.__retrieve(links[i], path)
                
    def __retrieve(self, url, path):
        ''' ���ص����ļ���ָ��Ŀ¼�� '''
        for i in range(5):
            try:
                urllib.urlretrieve(url, path)
            except:
                print '���ӳ�ʱ����������ԡ���'
                time.sleep(5)
            else:
                break;
            
    def __splitResourceName(self, url):
        ''' ��Url����ȡ�ļ����� '''
        return url.split('/')[-1]
        

if __name__ == '__main__':
    socket.setdefaulttimeout(30)
    
    dic = readConfig()
    
    for blog in dic['blogs']:
        spider = TumblrSpider(blog, dic['fileTypes'])
        spider.crawl()
        
    quit('������ϡ�')