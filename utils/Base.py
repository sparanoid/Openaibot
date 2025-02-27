# -*- coding: utf-8 -*-
# @Time    : 9/22/22 11:04 PM
# @FileName: Base.py
# @Software: PyCharm
# @Github    ：sudoskys
import time

import rtoml
from rich.console import Console


def Logger():
    from loguru import logger

    # 日志机器
    logger.add(sink='run.log',
               format="{time} - {level} - {message}",
               level="INFO",
               rotation="500 MB",
               enqueue=True)
    return logger


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Tool(object):
    def __init__(self):
        """
        基本工具类
        """
        self.console = Console(color_system='256', style=None)
        self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def dictToObj(self, dictObj):
        if not isinstance(dictObj, dict):
            return dictObj
        d = Dict()
        for k, v in dictObj.items():
            d[k] = self.dictToObj(v)
        return d


class ReadConfig(object):
    def __init__(self, config=None):
        """
        read some further config!

        param paths: the file path
        """
        self.config = config

    def get(self):
        return self.config

    def parseFile(self, paths, toObj: bool = True):
        data = rtoml.load(open(paths, 'r'))
        self.config = data
        if toObj:
            self.config = Tool().dictToObj(data)
        return self.config

    def parseDict(self, data):
        self.config = Tool().dictToObj(data)
        return self.config

    @staticmethod
    def saveDict(paths, data):
        return rtoml.dump(data, open(paths, 'w'))
