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
import bs4 as bs
import nltk
import heapq
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
from sklearn.metrics.pairwise import cosine_similarity
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
# 扩展实验2：查阅其他的摘要生成方法，并和“滑动窗口的方法”进行比较



# -------------------------------------------------------------------------------------------------------------

# # MAIN
# if __name__ == '__main__':
#
#     pass