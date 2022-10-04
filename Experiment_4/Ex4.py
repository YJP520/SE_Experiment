#
# Crawler Edited by Pycharm.
# Time : 2022/09/30
# Author : YU.J.P
#

"""
    版本: V1.0
    基本功能:
        - 二叉树，普通树

    实验要求:
        给定两个文本串，设置不同的K值，计算它们的k-shingle集合，并进行相似度计算；分析不同的k值对相似度的影响；
        利用K-shingle算法，计算两个给定文档的相似度，查找重复字符串，并将重复字符串高亮显示出来；
        扩展实验：对给定的一个文档，计算它和某路径下的所有文档的相似度，将相似度高于某阈值的文档名称和重复内容显示出来。
        扩展实验：自己编写I-match和simhash方法的代码，并对选定的文档进行相似度计算，对结果进行对比

"""

import urllib.request
import requests
import BitVector as BitVector
from bs4 import BeautifulSoup
import re
import os
import jieba


# -------------------------------------------------------------------------------------------------------------

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


# -------------------------------------------------------------------------------------------------------------

# 节点类
class Node(object):
    def __init__(self, item):
        self.item = item  # 表示对应的元素
        self.left = None  # 表示左子节点
        self.right = None  # 表示右子节点

    def __str__(self):
        return str(self.item)  # print 一个 Node 类时会打印 __str__ 的返回值


# 创建 Tree 类
class Tree(object):
    def __init__(self):
        self.root = Node('root')  # 根节点定义为 root 永不删除，作为哨兵使用。


# -------------------------------------------------------------------------------------------------------------

# 网页分析类
class AnalyzeHtml:
    def __init__(self):
        pass

    @classmethod
    def analyze(cls):
        print(Color.green + '# 网页分析...')
        pass


# -------------------------------------------------------------------------------------------------------------

# 运行
if __name__ == '__main__':
    AnalyzeHtml.analyze()  # 网页分析
    pass
