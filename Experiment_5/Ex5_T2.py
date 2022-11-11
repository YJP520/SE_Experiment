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

# 读入一篇给定的中文文本，采用最大匹配法进行中文分词（正向和逆向）
class leftMax:
    def __init__(self, dict_path):
        self.dictionary = set()  # 定义字典
        self.maximum = 0  # 最大匹配长度

        with open(dict_path, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary.add(line)
                if len(line) > self.maximum:
                    self.maximum = len(line)

    def cut(self, content):
        result = []
        length = len(content)
        index = 0
        while length > 0:
            word = None
            for size in range(self.maximum, 0, -1):
                if length - size < 0:
                    continue
                piece = content[index:index + size]
                if piece in self.dictionary:
                    word = piece
                    result.append(word)
                    length -= size
                    index += size
                    break
            if word is None:
                length -= 1
                result.append(content[index])
                index += 1
        return result


def test1():
    print(Color.green, "正匹配：")
    content = '研究生命的起源'
    tokenizer = leftMax('Data/30wdict_utf8.txt')
    print(Color.blue, tokenizer.cut(content))

# -------------------------------------------------------------------------------------------------------------


class rightMax:
    def __init__(self, dict_path):
        self.dictionary = set()  # 定义字典
        self.maximum = 0  # 最大匹配长度

        with open(dict_path, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary.add(line)
                if len(line) > self.maximum:
                    self.maximum = len(line)

    def cut(self, content):
        result = []
        index = len(content)
        while index > 0:
            word = None
            for size in range(self.maximum, 0, -1):
                if index - size < 0:
                    continue
                piece = content[(index - size):index]
                if piece in self.dictionary:
                    word = piece
                    result.append(word)
                    index -= size
                    break
            if word is None:
                index -= 1
                result.append(content[(index - 1):index])
        return result[::-1]  # 由于append为添加至末尾，故需反向打印


def test2():
    print(Color.green, "逆向匹配：")
    content = '研究生命的起源'
    tokenizer = rightMax('Data/30wdict_utf8.txt')
    print(Color.blue, tokenizer.cut(content))

# -------------------------------------------------------------------------------------------------------------

def doubleMax(content, path):
    left = leftMax(path)
    right = rightMax(path)

    leftMatch = left.cut(content)
    rightMatch = right.cut(content)

    # 返回分词数较少者
    if (len(leftMatch) != len(rightMatch)):
        if (len(leftMatch) < len(rightMatch)):
            return leftMatch
        else:
            return rightMatch
    else:  # 若分词数量相同，进一步判断
        leftsingle = 0
        rightsingle = 0
        isEqual = True  # 用以标志结果是否相同
        for i in range(len(leftMatch)):
            if (leftMatch[i] != rightMatch[i]):
                isEqual = False
            # 统计单字数
            if (len(leftMatch[i]) == 1):
                leftsingle += 1
            if (len(rightMatch[i]) == 1):
                rightsingle += 1
        if (isEqual):
            return leftMatch
        if (leftsingle < rightsingle):
            return leftMatch
        else:
            return rightMatch


def test3():
    # content = "北京大学生前来应聘算法工程师岗位"
    content = '研究生命的起源'
    print(doubleMax(content, 'Data/30wdict_utf8.txt'))


# -------------------------------------------------------------------------------------------------------------


# MAIN
if __name__ == '__main__':
    test1()
    test2()
    # test3()
    pass