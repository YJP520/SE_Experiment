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
from sklearn.metrics.pairwise import cosine_similarity
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

# 外选定一篇文档，利用余弦相似度计算它和已有的20篇文档的相似度，对这20篇文档排序。

class Cos:
    def __init__(self, fileName, content1, content2):
        """
        :param fileName: 文件名
        :param content1: 文本 1
        :param content2: 文本 2
        """
        self.fileNme = fileName

        self.words1 = self.cutWords(content1)  # 单词序列 1
        # print(Color.green, self.words1)

        self.words2 = self.cutWords(content2)  # 单词序列 2
        # print(Color.green, self.words2)

        self.wordsSet = self.getSet() # 单词并集
        # print(Color.green, self.wordsSet)

        self.V1 = self.getVector(self.words1)  # 向量 1
        print(Color.blue, self.V1)

        self.V2 = self.getVector(self.words2)  # 向量 2
        print(Color.blue, self.V2)

        a = []
        a.append(self.V1)
        a.append(self.V2)
        similarity = cosine_similarity(a)
        print(similarity)

        self.similarity = self.culculate()  # 相似度
        print(Color.red, 'similarity = ', self.similarity)



    def cutWords(self, content):
        """
        jieba 分词
        :return: 单词序列
        """
        seg_list = jieba.cut(content)
        words = []
        for seg in seg_list:
            seg = ''.join(seg.split())
            if seg != '' \
                    and seg != ' ' \
                    and seg != '，' \
                    and seg != '？' \
                    and seg != '。' \
                    and seg != "\n" \
                    and seg != "\n\n":
                words.append(seg)
        return words

    def getSet(self):
        """
        :return: 单词集合
        """
        return set(self.words1 + self.words2)

    def getVector(self, words):
        """
        计算向量
        :return: 向量
        """
        dic = {}
        # 初始化向量
        for index in self.wordsSet:
            dic[index] = 0
        for index in words:
            if index in dic:
                dic[index] += 1
        print(Color.carmine, dic)
        return list(dic.values())

    def culculate(self):
        # 分子
        molecule = 0.0
        # 左右平方和
        left = 0.0
        right = 0.0
        # 计算
        for i in range(len(self.wordsSet)):
            v1 = self.V1[i]
            v2 = self.V2[i]
            molecule += v1 * v2
            left += v1 * v1
            right += v2 * v2
        # 分母
        denominator = math.sqrt(left) * math.sqrt(right)
        similarity = molecule / denominator
        # 返回相似度
        return similarity


# 计算与20篇文本的相似度
def test():
    # 读取文档 file 读取文件下的文档名 然后依次打开调用
    with open('Data/Data_T2/37921', 'r', encoding='utf-8') as f1:
        content1 = f1.read()

    similarityDic = {}  # 文本对象字典

    basePath = "F:/Projects/Python Pycharm/SE_Experiment/Experiment_6/Data/Data_T3"
    folder = os.listdir(basePath)

    for index in folder:
        print(Color.blue, "----------------------------------------")
        print(Color.green, '# 读入文件:' + index)
        filePath = basePath + '/' + index
        with open(filePath, 'r', encoding='utf-8') as f1:
            content2 = f1.read()
            ob = Cos(index, content1, content2)
            similarityDic[index] = ob.similarity
    print(Color.carmine, similarityDic)
    # 字典排序
    similarityDic = sorted(similarityDic.items(), key=lambda x: x[1], reverse=False)
    print(Color.green, similarityDic)


# -------------------------------------------------------------------------------------------------------------


# MAIN
if __name__ == '__main__':
    # content1 = 'i love you and i want to sing for you.'
    # content2 = 'MandiSa sing for me every week on monday and saturday.'
    # ob = Cos(content1, content2)

    test()

    pass