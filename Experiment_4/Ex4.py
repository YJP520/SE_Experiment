#
# Crawler Edited by Pycharm.
# Time : 2022/09/27
# Author : YU.J.P
#

"""
    版本: V1.3
    基本功能:
    对给定的一个URL，能够将该网页的HTML文本下载到本地文件保存；
    利用正则表达式，将网页中的标题、正文、超链接、图片等元素分别提取出来，并能存放到指定的文件中；图片单独存储；
    根据提取的链接，采用广度优先方式抓取至少1000个网页，并提取上述指定的信息；
    扩展1：利用深度优先方式抓取网页，分析比较广度和深度抓取网页的差异；
    扩展2：利用建立HTML标签树的方法，实现网页中相应信息的提取；
"""

import urllib.request
import requests
import BitVector as BitVector
from bs4 import BeautifulSoup
import re


# 字体颜色设置类 格式：print(Color.xxx + "XXX")
class Color:
    carmine = '\033[95m'  # 洋红色
    blue = '\033[94m'  # 蓝色
    green = '\033[92m'  # 绿色
    yellow = '\033[93m'  # 黄色
    red = '\033[91m'  # 红色
    black = '\033[0m'  # 洋红色

    def __init__(self):
        pass


# 斑斓类
class BanLan:
    def __init__(self):
        pass

    @classmethod
    def Func(cls):
        print(Color.carmine + '# AMD YES')

    @classmethod
    def AMDYES(cls):
        print(Color.red +
              '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n' +
              '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n' +
              '⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⣉⣉⣠⣤⣤⣄⣀⡉⠛⠻⣿⣿⣿⣿\n' +
              '⣿⣿⣿⣿⣿⡿⢛⣥⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠙⣿⣿\n' +
              '⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠈⣿\n' +
              '⣿⠟⣴⠁⡆⠸⣿⣿⠀⡀⢿⣿⠏⡀⢸⣿⠀⣶⣶⣄⠈⣿⣿⣿⠀⣿\n' +
              '⡟⣸⡟⢀⣿⠀⢿⣿⠀⣷⠀⣿⢀⡇⢸⣿⠀⣿⣿⣿⠀⣿⣿⠃⢀⣿\n' +
              '⠀⣿⠀⣶⣶⣆⠈⣿⠀⣿⡆⠁⣾⡇⢸⣿⠀⠿⠟⠁⣠⡟⠁⣠⣿⣿\n' +
              '⡀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿\n' +
              '⣷⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⣿⣿⣿⣿⣿\n' +
              '⣿⣿⣤⠀⠉⠛⠛⠿⠿⠿⠿⠿⠛⠛⠋⠉⠀⠀⣀⣤⣾⣿⣿⣿⣿⣿\n' +
              '⣿⣿⣿⣿⣿⣶⣦⣤⣤⣤⣤⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n' +
              '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n')


# 网页分析类
class AnalyzeHtml:
    def __init__(self):
        pass

    @classmethod
    def analyze(cls):
        print(Color.green + '# 网页分析...')

        pass


# 节点类
class Node(object):
    def __init__(self,item):
        self.item = item  # 表示对应的元素
        self.left = None  # 表示左子节点
        self.right = None  # 表示右子节点

    def __str__(self):
        return str(self.item)  # print 一个 Node 类时会打印 __str__ 的返回值


# 创建 Tree 类
class Tree(object):
    def __init__(self):
        self.root = Node('root')  # 根节点定义为 root 永不删除，作为哨兵使用。






# 运行
if __name__ == '__main__':
    BanLan.Func()  # 斑斓
    AnalyzeHtml.analyze()  # 网页分析
    pass
