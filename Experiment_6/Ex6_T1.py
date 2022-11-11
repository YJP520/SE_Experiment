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

# 根据给定的文档集合，统计单词在文档和文档集中出现的次数，根据TF和IDF来计算词项在文档集中的权重TFIDF；

class TF_IDF:
    def __init__(self):
        pass

    @classmethod
    def cutWords(cls, content):
        """
        jieba 分词
        :param content:
        :return:
        """
        seg_list = jieba.cut(content)
        words = []
        for seg in seg_list:
            seg = ''.join(seg.split())
            if seg != '，' and seg != '？' and seg != '。' and seg != "\n" and seg != "\n\n":
                words.append(seg)
        return words

    @classmethod
    def proceed(cls, texts):
        """
        对文本预处理，以列表类型存放
        :param texts:
        :return:
        """
        docs = []
        for text in texts:
            doc = cls.cutWords(text)
            docs.append(doc)
        return docs

    @classmethod
    def wordsFrequency(cls, docs):
        """
        此处的docv存放各个文档中单词出现的频率
        :param texts: 文本
        :param docs: 文本分词预处理
        :return:
        """
        docv = []
        for i, doc in enumerate(docs):
            vec = {}
            for word in doc:
                if word not in vec:
                    vec[word] = 1
                else:
                    vec[word] += 1
            docv.append(vec)
        return docv

    @classmethod
    def tf(cls, docs, docv):
        """
        计算 tf
        :param docs:
        :return:
        """
        tf_word = []
        for i, doc in enumerate(docs):
            doc_count = len(doc)
            tf = {}
            for word in doc:
                word_count = docv[i][word]
                word_tf = 1.0 * word_count / doc_count
                tf[word] = word_tf
                tf_word.append(tf)
        return tf_word

    @classmethod
    def wordsIdf(cls, docs):
        """
        单词集合
        :param docs:
        :return:
        """
        words_idf = {}
        for i, doc in enumerate(docs):
            for word in doc:
                if word not in words_idf:
                    words_idf[word] = []
                    words_idf[word].append(i)
                else:
                    words_idf[word].append(i)
        for key in words_idf:
            words_idf[key] = len(set(words_idf[key]))
        return words_idf

    @classmethod
    def idf(cls, words_idf, docs):
        """
        计算 idf 值
        :param words_idf:
        :return:
        """
        idf_word = {}
        docs_count = len(docs)
        for word in words_idf:
            idf_word[word] = math.log(docs_count / (words_idf[word] + 1))
        return idf_word

    @classmethod
    def tf_idf(cls, tf_word, idf_word):
        word_tfidf = {}
        for word_vec in tf_word:
            for word in word_vec:
                word_tfidf[word] = 1.0 * word_vec[word] * idf_word[word]
        return word_tfidf

    @classmethod
    def getTFIDF(cls, texts):
        """
        返回 TF-IDF
        :return: TF-IDF values
        """
        docs = cls.proceed(texts)
        print(Color.blue, docs)

        docv = cls.wordsFrequency(docs)
        print(Color.green, docv)

        tf_word = cls.tf(docs, docv)
        print(Color.red, tf_word)

        words_idf = cls.wordsIdf(docs)
        print(Color.carmine, words_idf)

        idf_word = cls.idf(words_idf,docs)
        print(Color.blue, idf_word)

        word_tfidf = cls.tf_idf(tf_word, idf_word)
        print(Color.red, word_tfidf)

        return word_tfidf

# -------------------------------------------------------------------------------------------------------------

# MAIN
if __name__ == '__main__':
    texts = ["我喜欢苹果，你喜欢吗？",
            "每天一个苹果，医生远离你",
            "永远不要拿苹果和橘子比较",
            "相对于橘子而言，我更喜欢苹果"]

    TF_IDF.getTFIDF(texts)
    pass