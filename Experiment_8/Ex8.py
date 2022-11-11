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
import sklearn
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
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

# 利用scikit-learn库来计算TFIDF；

def tfidf_test():
    corpus = ["我 喜欢 超级 赛亚人",  # 第一类文本切词后的结果，词之间以空格隔开
              "他 喜欢 哪吒",  # 第二类文本的切词结果
              "一切 困难 我们 都 能 战胜 奥力给",  # 第三类文本的切词结果
              "今天 又 是 元气满满 的 一天"]  # 第四类文本的切词结果
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            print(word[j], weight[i][j])

# -------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------

# MAIN
if __name__ == '__main__':
    # tfidf_test()


    pass
