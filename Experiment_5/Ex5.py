#
# Crawler Edited by Pycharm.
# Time : 2022/10/14
# Author : YU.J.P
#

"""
    版本: V1.0
    基本功能:
        - 中文分词

    实验要求:
        利用jieba分词对读入的一篇中文文本进行分词，统计每个单词出现的次数和位置；
            （注：也可以使用其他的分词工具包，如 KAnalyzer， ICTCLAS，Paoding、MMSEG4J等）
        读入一篇给定的中文文本，采用最大匹配法进行中文分词（正向和逆向）
        扩展内容1：对实验一的sanguo.txt进行分词，并计算每个词出现的次数，利用matplotlib包画图展示
        扩展内容2：将最大匹配法结果和jieba等分词工具包的结果进行比较

"""

import urllib.request
import requests
import BitVector as BitVector
from bs4 import BeautifulSoup
import re
import os
import jieba
import jieba.analyse
from pygraph.classes.digraph import digraph
import networkx as nx
import matplotlib.pyplot as plt


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

class ChineseWords:


    def __init__(self):
        pass

    @classmethod
    def max_math_segment(cls, line, dic, size=5):
        max_size = size
        chars = line
        words = []
        idx = 0
        while idx < len(chars):
            matched = False
            for i in range(max_size, 0, -1):
                cand = chars[idx:idx + i]
                if cand in dic:
                    words.append(cand)
                    matched = True
                    break
            if not matched:
                i = 1
                words.append(chars[idx])
            idx += i
        return words

    @classmethod
    def testJieba(cls):

        seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
        print("【全模式】: " + "/ ".join(seg_list))  # 全模式

        seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
        print("【精确模式】: " + "/ ".join(seg_list))  # 精确模式，也是默认模式

        seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
        print('【搜索引擎模式】：', ", ".join(seg_list))  # 搜索引擎模式

        file_name = 'Data/实验五 分词jieba.txt'
        content = open(file_name, 'rb').read()
        tags = jieba.analyse.extract_tags(content, topK=10)

        print(",".join(tags))

        pass

# -------------------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------------------


# MAIN
if __name__ == '__main__':
    ChineseWords.testJieba()
    pass
