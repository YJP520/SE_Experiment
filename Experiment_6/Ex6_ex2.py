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
from simhash import Simhash
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

# 扩展实验2：你还可以用其他的相似度计算方法吗？如果有，将结果和余弦相似度的结果进行比较。

# 利用simhash算法筛选重复文档。

def simhash_demo(text1, text2):
    """
    求两文本的相似度
    :param text1:
    :param text2:
    :return:
    """
    a_simhash = Simhash(text1)
    b_simhash = Simhash(text2)
    max_hashbit = max(len(bin(a_simhash.value)), (len(bin(b_simhash.value))))
    # 汉明距离
    distince = a_simhash.distance(b_simhash)
    print(Color.red, '# 汉明距离:', distince)
    print(Color.red, '# 长度:', max_hashbit)
    similar = 1 - distince / max_hashbit
    return similar

# -------------------------------------------------------------------------------------------------------------

class Cos:
    def __init__(self, content1, content2):
        """
        :param content1: 文本 1
        :param content2: 文本 2
        """
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

    basePath = "F:/Projects/Python Pycharm/SE_Experiment/Experiment_6/Data/Data_T3"
    folder = os.listdir(basePath)

    for index in folder:
        print(Color.blue, "----------------------------------------")
        print(Color.green, '# 读入文件:' + index)
        filePath = basePath + '/' + index
        with open(filePath, 'r', encoding='utf-8') as f1:
            content2 = f1.read()
            ob = Cos(content1, content2)

# -------------------------------------------------------------------------------------------------------------

# MAIN
if __name__ == '__main__':

    text1 = "行者AI专注于游戏领域,多年的AI技术积淀,一站式提供文本、图片、音/视频内容审核,游戏AI以及数据平台服务"
    text2 = "行者AI专注于游戏领域,多年的AI技术积淀,二站式提供文本、图片、音 视频内容审核,游戏AI以及数据平台服务"
    similar = simhash_demo(text1, text2)
    print(Color.blue, "# 相似度:", similar)

    Cos(text1, text2)

    pass