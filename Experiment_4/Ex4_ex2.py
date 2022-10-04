#
# Crawler Edited by Pycharm.
# Time : 2022/09/30
# Author : YU.J.P
#

"""
    版本: V1.0

    实验要求:
        给定两个文本串，设置不同的K值，计算它们的k-shingle集合，并进行相似度计算；分析不同的k值对相似度的影响；
        利用K-shingle算法，计算两个给定文档的相似度，查找重复字符串，并将重复字符串高亮显示出来；
        扩展实验：对给定的一个文档，计算它和某路径下的所有文档的相似度，将相似度高于某阈值的文档名称和重复内容显示出来。
        扩展实验：自己编写I-match和simhash方法的代码，并对选定的文档进行相似度计算，对结果进行对比

"""

import urllib.request
import requests
import BitVector as BitVector
from bs4 import BeautifulSoup
import re
import os
import jieba
import jieba.analyse
import numpy as np


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
# I_Match 算法
class I_Match:
    def __init__(self):
        pass


# I_Match 改进 算法
class I_Match_Improve:
    def __init__(self):
        pass


# Simhash算法:
#   simhash算法的核心思想是降维，将文章表示为特征值集合，再降维为一个b位的hash特征向量，
#   通过比较两个simhash之间的海明（ Hamming）距离来衡量相似性
class SimHash(object):
    def __init__(self):
        pass

    @classmethod
    def _simHash(cls, content):
        """
        :param content: 文本内容
        :return: 哈希
        """
        # 1. jieba分词 可以使用TF-IDF方法获取一篇文章权重最高的前topK个词（feature）和权重（weight）
        seg = jieba.cut(content)
        keyWords = jieba.analyse.extract_tags("|".join(seg), topK=10, withWeight=True)
        # print(Color.carmine, keyWords)

        # 3. 加权
        keyList = []  # 所有权值
        print(Color.black, "----------------------------------")
        for feature, weight in keyWords:
            print(Color.green, 'feature:' + feature,end=' ')
            print(Color.blue, 'weight: %g' % weight)
            weight = int(weight)
            # 2. 计算hash值
            binStr = cls._string_hash(feature)
            # print(Color.green, 'string_hash: ' + binStr)
            weightList = []  # feature 加权
            for c in binStr:
                if c == '1':
                    weightList.append(weight)
                else:
                    weightList.append(-weight)
            keyList.append(weightList)
        # print(Color.carmine, keyList)
        # 4. 合并 权值相加
        listSum = np.sum(np.array(keyList), axis=0)
        # print(Color.blue, listSum)

        # 为空
        if not keyList:
            return '00'
        # 5. 降维
        simHash = ''
        for i in listSum:
            if i > 0:
                simHash = simHash + '1'
            else:
                simHash = simHash + '0'
        return simHash

    @classmethod
    def _string_hash(cls, source):
        """
        :param source: 关键字
        :return: hash值
        """
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]

            return str(x)

    @classmethod
    def _getDistance(cls, hashStr1, hashStr2):
        """
        计算汉明距离
        :param hashStr1: 哈希值 1
        :param hashStr2: 哈希值 2
        :return: 汉明距离
        """
        length = 0
        for index, char in enumerate(hashStr1):
            if char == hashStr2[index]:
                continue
            else:
                length += 1
        return length

    @classmethod
    def getSimHash(cls, content1, content2):
        """
        :param content1: 文本 1
        :param content2: 文本 2
        :return: 汉明距离
        """
        hashStr1 = cls._simHash(content1)
        hashStr2 = cls._simHash(content2)
        return cls._getDistance(hashStr1, hashStr2)


# -------------------------------------------------------------------------------------------------------------

# 运行
if __name__ == '__main__':
    print(Color.green, 'Experiment_4', Color.yellow, '---', Color.carmine, 'Ex4_ex2')

    filePath1 = 'Data/Ex4_T2_Data/content1.txt'
    content1 = None  # 内容 1
    filePath2 = 'Data/Ex4_T2_Data/content2.txt'
    content2 = None  # 内容 2
    with open(filePath1, 'r', encoding='utf-8') as f1:
        content1 = f1.read()
    f1.close()
    with open(filePath2, 'r', encoding='utf-8') as f2:
        content2 = f2.read()
    f2.close()
    distance = SimHash.getSimHash(content1, content2)

    # s1 = '我在重庆的重庆理工大学'
    # s2 = '我在重庆的重庆大学上大学'
    # distance = SimHash.getSimHash(s1, s2)

    print(Color.black, "----------------------------------")
    print(Color.red, 'distance = {}'.format(distance))

    pass

