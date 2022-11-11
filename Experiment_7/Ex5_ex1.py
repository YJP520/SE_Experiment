#
# Crawler Edited by Pycharm.
# Time : 2022/10/07
# Author : YU.J.P
#

"""
    版本: V1.0
    基本功能:
        - 网页的重要性计算

    实验要求:
         给定网页链接关系，根据PageRank的计算公式计算网页的PR值，直到每个网页的PR值稳定为止，列出最终的PR值；
          假设每个网页的初始PR值相等。（计算结果保留小数点后5位数）
         根据PR值对网页重要性进行排序；如果有1,000,000个网页，你将使用什么排序技术，写出排序算法，查资料分析它与其它算法的优劣。
         扩展实验1：使用TextRank提取给定句子中的关键词。
         扩展实验2：利用NetworkX包(或其它)用图示的方式表示网络图。
         扩展实验3：利用NetworkX画出希拉里邮件中的人物关系图。

"""

import urllib.request
import requests
import BitVector as BitVector
from bs4 import BeautifulSoup
import re
import os
import jieba
from pygraph.classes.digraph import digraph
# JDK配置 https://www.cnblogs.com/nicholas_f/articles/1494073.html
from pyhanlp import *
import numpy as np


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

class TRIterator:
    def __init__(self, content, wdSize=4, d=0.85, count=100, delta=0.0001):
        self.windowSize = wdSize   # 共现窗口
        self.damping_factor = d  # 阻尼系数,即d
        self.max_iterations = count  # 最大迭代次数
        self.min_delta = delta  # 确定迭代是否结束的参数,即ϵ
        self._keyWords = self.getKeyWords(content)
        pass

    def getKeyWords(self, content):
        """
        获取名词、动词、形容词、副词
        :param content: 文本内容
        :return: 名词、动词、形容词、副词列表
        """
        signWords = HanLP.segment(content)  # 词性标注
        print(Color.green, "# 原始分词:", Color.blue, signWords)

        words = []
        sign = ['n', 'v', 'a']
        for index in signWords:
            index = str(index)  # 转成字符串
            position = 0
            for i in range(0, len(index) - 1):
                if index[i] == '/':
                    position = i
            if index[position + 1:] in sign:
                words.append(index[0: position])
        return words

    def textRank(self):
        """
        提取关键词
        :return: 关键词序列
        """
        print(Color.green, '# 分词展示:', Color.blue, self._keyWords)

        # 构建矩阵 设置共现窗口
        wordSet = list(set(self._keyWords))  # 关键词集合
        length = len(wordSet)  # 关键词个数
        print(Color.green, '# 集合展示:', Color.blue, wordSet)
# -------------------------------------------------------------------------------------------------------------


# MAIN
if __name__ == '__main__':
    content = '学程序的优秀男生还在写程序'
    TRIterator(content).textRank()
    pass