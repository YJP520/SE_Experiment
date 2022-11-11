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
# 读取一篇文本，使用“滑动窗口的方法”抽取文档摘要（结合K-Shingle算法以及TF-IDF算法），试着设置不同的窗口大小，分析比较生成的摘要的不同

class TFIDF_Abstract:
    def __init__(self, keyString, filePath, cutSize=40):
        # 摘要窗口大小
        self.cutSize = cutSize
        # 搜索关键词列表
        self.keyWords = self.cutWordsByBlank(keyString)
        # 以空格隔开的搜索关键词
        self.keyWordsWithBlank = self.cutWordsWithBlank(keyString)[0]
        # 文档内容
        self.content = self.getContent(filePath)
        # 文档内容以空格分词
        self.corpus = self.cutWordsWithBlank(self.content)
        # 文档关键词 TFIDF值
        self.tfidfDic = self.tfidf(self.corpus)
        # 关键词索引位置
        self.indexPos = self.getKeyWordsPos(self.keyWords, self.content)
        # 获取摘要句子
        self.abstracts = self._cutAbstract()
        # 摘要分词
        self.abstractWords = self._cutAbstractWords()
        # 计算TFIDF总和最大的文档
        self.maxTfidfPos = self._getMaxTfidfPos()
        # 最重要的摘要
        self.abstract = self.abstracts[self.maxTfidfPos]

        print(Color.black, self.content)
        print(self.tfidfDic)
        print(Color.red, self.indexPos)
        for index in self.abstracts:
            print(Color.blue, index)
        for index in self.abstractWords:
            print(Color.green, index)
        print(Color.red, self.maxTfidfPos)
        print(Color.red, self.abstract)

    @classmethod
    def getContent(cls, filePath):
        """
        打开文件读取内容
        :param filePath: 文件路径
        :return: 文件内容
        """
        with open(filePath, 'r', encoding='utf-8') as f1:
            content = f1.read()
        f1.close()
        return content

    @classmethod
    def cutWordsWithBlank(cls, content):
        """
        得到以空格分隔的单词序列
        :param content: 文本
        :return: 以空格分隔的单词序列
        """
        corpus = []
        # 对文档进行分词处理，采用默认模式
        # seg_list = jieba.cut(content, cut_all=True)
        # 精确模式
        seg_list = jieba.cut(content, cut_all=False)
        # 搜索引擎模式
        # seg_list = jieba.cut_for_search(content)
        # 对空格，换行符进行处理
        result = ''
        for seg in seg_list:
            seg = ''.join(seg.split())
            if seg != '' \
                and seg != "，" \
                and seg != "。" \
                and seg != "、" \
                and seg != "\n" \
                and seg != "\n\n":
                result += seg + ' '  # 空格间隔
        # print(result)
        corpus.append(result)
        return corpus

    @classmethod
    def cutWordsByBlank(cls, keyString):
        """
        切分
        :param keyString:
        :return:
        """
        # wordsList = []
        # j = 0
        # for i in range(len(keyString)):
        #     print(i)
        #     if keyString[i] == ' ' and i < len(keyString) - 1:
        #         wordsList.append(keyString[j: i])
        #         j = i + 1
        #     elif len(keyString) - 1 == i and i > j:
        #         wordsList.append(keyString[j: i + 1])
        # # print(wordsList)
        # return wordsList

        wordsList = []
        seg_list = jieba.cut(keyString, cut_all=False)
        for seg in seg_list:
            seg = ''.join(seg.split())
            if seg != '' \
                    and seg != "，" \
                    and seg != "。" \
                    and seg != "、" \
                    and seg != "\n" \
                    and seg != "\n\n":
                wordsList.append(seg)
        return wordsList

    @classmethod
    def tfidf(cls, corpus):
        """
        计算 TF-IDF
        :param corpus: 分词列表
        :return: TF-IDF 值
        """
        # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        vectorizer = CountVectorizer()
        # 该类会统计每个词语的tf-idf权值
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(
            # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
            vectorizer.fit_transform(corpus))
        # 获取词袋模型中的所有词语
        word = vectorizer.get_feature_names()
        # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        weight = tfidf.toarray()
        # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        dic = {}
        for i in range(len(weight)):
            print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
            for j in range(len(word)):
                # 写入文档
                dic[word[j]] = weight[i][j]
                # 打印输出
                # print(word[j], weight[i][j])
        return dic

    @classmethod
    def BruteForceStringMatchAll(cls, S, P, pos=0):
        """
        Brute Force - BF串匹配算法 查找多次
        :param S: 模式串
        :param P: 匹配串
        :param pos: 开始索引位置
        :return: 索引位置列表
        """
        position = []  # 索引列表
        S_len, P_len = len(S), len(P)
        for i in range(pos, S_len - 1):
            j = 0
            while S[i + j] == P[j] and j < P_len:
                j += 1
                if j == P_len:
                    position.append(i)  # 找到一个就加到列表中
                    break  # 退出此层循环
        return position  # 返回列表

    @classmethod
    def getKeyWordsPos(cls, keyWords, content):
        print(Color.blue, keyWords)

        # 所有关键词的索引位置
        posList = []
        # 寻找索引位置
        for index in keyWords:
            listTemp = cls.BruteForceStringMatchAll(content, index)
            # 加入索引位置
            for pos in listTemp:
                posList.append(pos)
        # 去重
        posList = list(set(posList))
        # 排序
        posList.sort(reverse=False)
        return posList

    def _cutAbstract(self):
        """
        私有函数 根据窗口大小 关键词索引获取摘要
        :return: 摘要句子
        """
        abstracts = []
        for index in self.indexPos:
            string = self.content[index: index + self.cutSize]
            # print(string)
            abstracts.append(string)
        return abstracts

    def _cutAbstractWords(self):
        """
        对摘要句子做分词
        :return: 分词列表
        """
        abstractWords = []
        for index in self.abstracts:
            tempList = []
            seg_list = jieba.cut(index, cut_all=False)
            for seg in seg_list:
                seg = ''.join(seg.split())
                if seg != '' \
                    and seg != "，" \
                    and seg != "。" \
                    and seg != "、" \
                    and seg != "\n" \
                    and seg != "\n\n":
                    tempList.append(seg)
            # print(tempList)
            abstractWords.append(tempList)
        return abstractWords

    def _getMaxTfidfPos(self):
        # 摘要TFIDF总和依次存入
        tfidfValue = []
        keys = self.tfidfDic.keys()
        # 对每个摘要句子计算TFIDF总和
        for abstract in self.abstractWords:
            tfidf = 0.0
            for word in abstract:
                if word in self.keyWords and word in keys:
                    tfidf += self.tfidfDic[word]
            tfidfValue.append(tfidf)
        print(Color.red, tfidfValue)
        maxPos = tfidfValue.index(max(tfidfValue))
        # print(Color.red, maxPos)
        return maxPos


# -------------------------------------------------------------------------------------------------------------

# MAIN
if __name__ == '__main__':
    keyString = '搜索引擎 数学'
    # keyString = '搜索引擎 学科 知识'
    filePath = 'Data/Data_T1/自动摘要.txt'
    ob = TFIDF_Abstract(keyString, filePath)

    pass