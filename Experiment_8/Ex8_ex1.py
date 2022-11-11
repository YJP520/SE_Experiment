#
# Crawler Edited by Pycharm.
# Time : 2022/10/27
# Author : YU.J.P
#

"""
    版本: V1.0
    基本功能:
        - 摘要提取

    实验要求:
        读取一篇文本，使用“滑动窗口的方法”抽取文档摘要（结合K-Shingle算法以及TF-IDF算法），试着设置不同的窗口大小，分析比较生成的摘要的不同
        从搜狗语料库中选取几篇相关文档抽取其中摘要信息，进行比较
        扩展实验1：使用TextRank提取给定段落中的中心句，比较提取中心句与采用滑动窗口的方法得到的摘要的异同
        扩展实验2：查阅其他的摘要生成方法，并和“滑动窗口的方法”进行比较


"""
import codecs
import chardet
import math
import urllib.request
import requests
import BitVector as BitVector
from bs4 import BeautifulSoup
import re
import os
import jieba
import jieba.analyse
# TFIDF
import sklearn
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
# 从textrank4zh模块中导入提取关键词和生成摘要的类
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from pygraph.classes.digraph import digraph
import networkx as nx
import matplotlib.pyplot as plt
from re import split
from jieba.posseg import dt
from collections import Counter
from time import time
from wordcloud import WordCloud


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
# 扩展实验1：使用TextRank提取给定段落中的中心句，比较提取中心句与采用滑动窗口的方法得到的摘要的异同

'''
    展示textrank4zh模块的主要功能：
        提取关键词
        提取关键短语（关键词组）
        提取摘要（关键句）
'''


class TextRank_Abstract:
    def __init__(self, filePath):
        """
        构造函数
        :param filePath: 文档路径
        """
        self.content = self._getContent(filePath)
        self.abstract = self.textRank()

    def getAbstract(self):
        """
        :return: 返回摘要
        """
        return self.abstract

    def _getContent(self, filePath):
        """
        打开文件读取内容
        :param filePath: 文件路径
        :return: 文件内容
        """
        with open(filePath, 'r', encoding='utf-8') as f1:
            content = f1.read()
        f1.close()
        return content

    def textRank(self):
        """
        使用TextRank获取摘要
        :return: 摘要
        """
        # # 创建分词类的实例
        # text_rank_4w = TextRank4Keyword()
        # # 对文本进行分析，设定窗口大小为4，并将英文单词小写
        # text_rank_4w.analyze(text=self.content, lower=True, window=4)

        # # 从关键词列表中获取前20个关键词
        # for item in text_rank_4w.get_keywords(num=20, word_min_len=1):
        #     # 打印每个关键词的内容及关键词的权重
        #     print(item.word, item.weight)

        # # 从关键短语列表中获取关键短语
        # for phrase in text_rank_4w.get_keyphrases(keywords_num=20, min_occur_num=2):
        #     print(phrase)

        # 创建分句类的实例
        tr4s = TextRank4Sentence()
        # 英文单词小写，进行词性过滤并剔除停用词
        tr4s.analyze(text=self.content, lower=True, source='all_filters')
        # 抽取1条句子作为摘要
        for item in tr4s.get_key_sentences(num=1):
            # 打印句子的索引、权重和内容
            # print(item.index, item.weight, item.sentence)
            return item.sentence

# -------------------------------------------------------------------------------------------------------------

# MAIN
if __name__ == '__main__':
    # filePath = 'Data/Data_T1/自动摘要.txt'
    # filePath = 'Data/Data_T2/51.txt'
    filePath = 'Data/Data_T2/52.txt'
    ob = TextRank_Abstract(filePath)
    abstract = ob.getAbstract()
    print(Color.green, '摘要为：')
    print(Color.red, abstract)
    pass
