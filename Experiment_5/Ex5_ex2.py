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

# 扩展内容2：将最大匹配法结果和jieba等分词工具包的结果进行比较
class ChineseWords:
    def __init__(self):
        pass

    @classmethod
    def testJieba(cls, content):
        seg_list = jieba.cut(content, cut_all=True)
        print(Color.carmine, "/ ".join(seg_list))  # 全模式

        seg_list = jieba.cut(content, cut_all=False)
        print("【精确模式】: " + "/ ".join(seg_list))  # 精确模式，也是默认模式

        seg_list = jieba.cut_for_search(content)  # 搜索引擎模式
        print('【搜索引擎模式】：', ", ".join(seg_list))  # 搜索引擎模式

        # file_name = 'Data/实验五 分词jieba.txt'
        # content = open(file_name, 'rb').read()
        # tags = jieba.analyse.extract_tags(content, topK=10)
        #
        # print(Color.carmine, ",".join(tags))



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


# -------------------------------------------------------------------------------------------------------------


# MAIN
if __name__ == '__main__':

    content = '话说天下大势，分久必合，合久必分。' \
              '周末七国分争，并入于秦。' \
              '及秦灭之后，楚、汉分争，又并入于汉。' \
              '汉朝自高祖斩白蛇而起义，一统天下，后来光武中兴，传至献帝，遂分为三国。' \
              '推其致乱之由，殆始于桓、灵二帝。桓帝禁锢善类，崇信宦官。' \
              '及桓帝崩，灵帝即位，大将军窦武、太傅陈蕃共相辅佐。' \
              '时有宦官曹节等弄权，窦武、陈蕃谋诛之，机事不密，反为所害，中涓自此愈横。'

    # 正向最大匹配
    print(Color.green, "正匹配：")
    tokenizer = leftMax('Data/30wdict_utf8.txt')
    print(Color.blue, tokenizer.cut(content))

    # 结巴分词
    print(Color.carmine, "结巴分词：")
    ChineseWords.testJieba(content)

    pass
