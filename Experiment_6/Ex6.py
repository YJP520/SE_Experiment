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

        idf_word = cls.idf(words_idf, docs)
        print(Color.blue, idf_word)

        word_tfidf = cls.tf_idf(tf_word, idf_word)
        print(Color.red, word_tfidf)

        return word_tfidf

# -------------------------------------------------------------------------------------------------------------


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

# TF_IDF 生成词云

FLAGS = set('a an b f i j l n nr nrfg nrt ns nt nz s t v vi vn z eng'.split())

def cut(text):
    for sentence in split('[^a-zA-Z0-9\u4e00-\u9fa5]+', text.strip()):
        for w in dt.cut(sentence):
            if len(w.word) > 2 and w.flag in FLAGS:
                yield w.word

class TFIDF:
    def __init__(self, idf):
        self.idf = idf

    @classmethod
    def train(cls, texts):
        model = TfidfVectorizer(tokenizer=cut)
        model.fit(texts)
        idf = {w: model.idf_[i] for w, i in model.vocabulary_.items()}
        return cls(idf)

    def get_idf(self, word):
        return self.idf.get(word, max(self.idf.values()))

    def extract(self, text, top_n=10):
        counter = Counter()
        for w in cut(text):
            counter[w] += self.get_idf(w)
        #return [i[0:2] for i in counter.most_common(top_n)]
        return [i[0] for i in counter.most_common(top_n)]


def tf_idf_wordsCloud():
    t0 = time()
    with open('Data/textOfCloud.txt', encoding='utf-8')as f:
        _texts = f.read().strip().split('\n')
        # print(Color.red, _texts)
    tfidf = TFIDF.train(_texts)
    # print(_texts)
    for _text in _texts:
        # seq_list=jieba.cut(_text, cut_all=True)  #全模式
        seq_list = jieba.cut(_text, cut_all=False)  #精确模式
        # seq_list=jieba.cut_for_search(_text,)    #搜索引擎模式
        # print(Color.green, list(seq_list))
        # print(Color.blue, tfidf.extract(_text))
        with open('Data/wordsCloud.txt', 'w', encoding='utf-8') as g:
            for i in tfidf.extract(_text):
                g.write(str(i) + " ")
    print(time() - t0)

    filename = "Data/wordsCloud.txt"
    with open(filename, 'r', encoding='utf-8') as f:
        resultciyun = f.read()

    wordcloud = WordCloud(font_path='C:\Windows\Fonts\simfang.ttf').generate(resultciyun)
    # wordcloud = WordCloud(font_path="simsun.ttf").generate(resultciyun)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


# -------------------------------------------------------------------------------------------------------------

# MAIN
if __name__ == '__main__':
    # texts = ["我喜欢苹果，你喜欢吗？",
    #         "每天一个苹果，医生远离你",
    #         "永远不要拿苹果和橘子比较",
    #         "相对于橘子而言，我更喜欢苹果"]
    # TF_IDF.getTFIDF(texts)

    # corpus = fenci()
    # Tfidf(corpus)

    tf_idf_wordsCloud()

    pass