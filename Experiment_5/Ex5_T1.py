#
# Crawler Edited by Pycharm.
# Time : 2022/10/14
# Author : YU.J.P
#

"""
    版本: V1.0
    基本功能:
        - 中文分词

    实验要求:
        利用jieba分词对读入的一篇中文文本进行分词，统计每个单词出现的次数和位置；
            （注：也可以使用其他的分词工具包，如 KAnalyzer， ICTCLAS，Paoding、MMSEG4J等）
        读入一篇给定的中文文本，采用最大匹配法进行中文分词（正向和逆向）
        扩展内容1：对实验一的sanguo.txt进行分词，并计算每个词出现的次数，利用matplotlib包画图展示
        扩展内容2：将最大匹配法结果和jieba等分词工具包的结果进行比较

"""

import urllib.request
import requests
import BitVector as BitVector
from bs4 import BeautifulSoup
import re
import os
import jieba
import jieba.analyse
from collections import Counter
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

# 用jieba分词对读入的一篇中文文本进行分词，统计每个单词出现的次数和位置；
class Statistic:
    def __init__(self):
        pass

    @classmethod
    def JiebaWords(cls, content, topk=10):
        """
        :param content: 文本
        :param topk: 高频词个数
        :return: 词频列表
        """
        # 分隔符
        divideChar = ['，', "。", "、", "！", "？", "的", "在", "了", "于"]
        # 分词列表
        split_words = list(x for x in jieba.cut(content, cut_all=False) if x not in divideChar)
        # 统计词 字典
        dic = {}  # 字典
        for word in split_words:
            dic[word] = dic.get(word, 0) + 1
        # 字典排序
        return sorted(dic.items(), key=lambda x: x[1], reverse=True)[:topk]  # get top 10

    @classmethod
    def BoyerMooreStringMatch(cls, S, P):
        """
        BoyerMooreStringMatch
        :param S: 文本内容
        :param P: 匹配串
        :return: 索引位置
        """
        position = []  # 索引列表
        S_len, P_len = len(S), len(P)
        if P_len == 0:
            return 0
        last = {}
        for index in range(P_len):  # 以P中字符为键索引为值创建字典
            last[P[index]] = index
        # 初始化索引辅助变量，使得P最右侧字符和S索引P_len - 1处对齐
        end, P_end = P_len - 1, P_len - 1
        while end < S_len:
            if S[end] == P[P_end]:
                if P_end == 0:  # 判断是否连续完成了len(P)次成功匹配
                    position.append(end)  # 记录结果
                    end += P_len  # 更新位置 继续比较
                else:  # 继续从右向左比对P和S对齐位置字符相同
                    end -= 1
                    P_end -= 1
            else:  # 坏字符原则 好后缀原则
                index = last.get(S[end], -1)  # 找到返回索引 没找到返回-1
                if index < P_end:  # S[end]不存在P中，即index = -1时，该条件及其操作依然成立
                    end += P_len - (index + 1)
                if index > P_end:
                    end += P_len - P_end
                P_end = P_len - 1  # 重新从右开始对P和S进行匹配
        return position

    @classmethod
    def BMWords(cls, content, wordsDic):
        wordsPos = {}
        for index, v in wordsDic:
            wordsPos[index] = cls.BoyerMooreStringMatch(content, index)
        return wordsPos

    @classmethod
    def testJieba(cls):
        """
        用jieba分词对读入的一篇中文文本进行分词，统计每个单词出现的次数和位置；
        :return: None
        """
        content = None
        file_name = 'Data/实验五 分词jieba.txt'
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()

        print(Color.red, "# 任务一 : jieba分词统计[前20个高频词]")
        wordsDic = cls.JiebaWords(content, 20)  # 统计词频
        wordsPos = cls.BMWords(content, wordsDic)  # 统计索引
        # 打印词频
        print(Color.yellow, '\n# 打印词频:')
        for key, value in wordsDic:
            print(Color.carmine, '[', end='')
            print(Color.blue, key, Color.green, ":", value, end='')
            print(Color.carmine, '],', end='')
        # 打印索引
        print(Color.yellow, '\n# 打印索引:')
        for key, value in wordsPos.items():
            print(Color.red, '[', end='')
            print(Color.blue, key, Color.green, ":", value, end='')
            print(Color.red, '],', end='')


# -------------------------------------------------------------------------------------------------------------

# MAIN
if __name__ == '__main__':
    Statistic.testJieba()
    pass
