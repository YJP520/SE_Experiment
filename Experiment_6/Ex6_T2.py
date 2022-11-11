#
# Crawler Edited by Pycharm.
# Time : 2022/10/21
# Author : YU.J.P
#

"""
    版本: V1.0
    基本功能:
        - TF_IDF

    实验要求:
        根据给定的文档集合，统计单词在文档和文档集中出现的次数，根据TF和IDF来计算词项在文档集中的权重TFIDF；
        利用scikit-learn库来计算TFIDF；
        另外选定一篇文档，利用余弦相似度计算它和已有的20篇文档的相似度，对这20篇文档排序。
        扩展实验1：利用tfidf计算权重，利用simhash算法筛选重复文档。
        扩展实验2：你还可以用其他的相似度计算方法吗？如果有，将结果和余弦相似度的结果进行比较。


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
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
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

# 利用scikit-learn库来计算TFIDF；
def convert(filename, out_enc="UTF-8"):
    """
    可将任意编码形式的文档转换为UTF-8编码
    :param filename: 文件路径
    :param out_enc: 文件编码
    :return: 编码后的结果
    """
    content=codecs.open(filename,'rb').read()
    source_encoding = chardet.detect(content)['encoding']
    content=content.decode(source_encoding).encode(out_enc)
    codecs.open(filename, 'wb').write(content)


def fenci():
    # 保存分词结果的目录
    sFilePath = 'Data/Data_T2_Out'
    # 读取文档file 读取文件下的文档名 然后依次打开调用
    basePath = "F:/Projects/Python Pycharm/SE_Experiment/Experiment_6/Data/Data_T2"
    folder = os.listdir(basePath)
    # 利用列表corpus存储所有文档的文本
    corpus = []

    for index in folder:
        print(Color.blue, "----------------------------------------------------------------")
        filePath = basePath + '/' + index
        with open(filePath, 'r', encoding='utf-8') as f1:
            content = f1.read()
            # print(content)
            corpus.append(content)

            # 对文档进行分词处理，采用默认模式
            seg_list = jieba.cut(content, cut_all=True)
            # 对空格，换行符进行处理
            result = []
            for seg in seg_list:
                seg = ''.join(seg.split())
                if seg != '' and seg != "\n" and seg != "\n\n":
                    result.append(seg)
            # 将分词后的结果用空格隔开，保存至本地。比如"我来到北京清华大学"，分词结果写入为："我 来到 北京 清华大学"
            f2 = open(sFilePath + "/" + index + "-seg.txt", "w+")
            f2.write(' '.join(result))
            f2.close()
        f1.close()
    print(corpus)
    return corpus


def Tfidf(corpus):
    # 首先利用列表corpus存储所有文档的文本
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    word = vectorizer.get_feature_names()
    print(Color.red, word)

    weight = tfidf.toarray()
    print(Color.yellow, weight)

    tfidfDict = {}
    for i in range(len(weight)):
        for j in range(len(word)):
            getWord = word[j]
            getValue = weight[i][j]
            if getValue != 0:
                if tfidfDict.__contains__(getWord):
                    tfidfDict[getWord] += float(getValue)
                else:
                    tfidfDict.update({getWord: getValue})
    print(Color.green, tfidfDict)

    sorted_tfidf = sorted(tfidfDict.items(), key=lambda d: d[1], reverse=True)
    fw = open('Data/result1.txt', 'w')
    for i in sorted_tfidf:
        fw.write(i[0] + '\t' + str(i[1]) + '\n')

# -------------------------------------------------------------------------------------------------------------

# MAIN
if __name__ == '__main__':
    corpus = fenci()
    Tfidf(corpus)
    pass