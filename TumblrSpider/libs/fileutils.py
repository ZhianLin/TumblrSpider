# coding:utf-8

import os


class FileUtils:
    @staticmethod
    def mkdir(directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)

    @staticmethod
    def fileExists(filename):
        return os.path.isfile(filename)

    @staticmethod
    def createFile(filename):
        open(filename, 'w').close()
