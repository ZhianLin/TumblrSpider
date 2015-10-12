import os
import re
import sys


class Config:
    CONFIG_FILE = sys.path[0] + os.sep + 'config.txt'

    def initConfigFile(self):
        f = file(Config.CONFIG_FILE, 'w')

        blogs = ['bokuwachikuwa', 'wnderlst']
        fileTypes = ['jpg', 'png', 'gif']

        blogsStr = '|'.join(blogs)
        fileTypesStr = '|'.join(fileTypes)

        f.write('Blog=%s\n' % blogsStr)
        f.write('FileType=%s\n' % fileTypesStr)

        f.close()

    def readConfig(self):
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
