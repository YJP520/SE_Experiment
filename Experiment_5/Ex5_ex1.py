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

# 扩展内容1：对实验一的sanguo.txt进行分词，并计算每个词出现的次数，利用matplotlib包画图展示

plt.rcParams['font.sans-serif'] = ['SimHei']  # 引入加载字体名
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def cutSan(sanTxt):
    cut_san = list(jieba.cut(sanTxt))
    print(cut_san)

    dic = dict()
    excludes = ['大军', '荆州', '将军', '却说', '二人', '不可', '不能', '如此', '商议', '如何', '主公', '军士', '左右',
                '军马', '引兵', '次日', '大喜', '天下', '东吴', '于是', '今日', '不敢', '魏兵', '陛下', '一人', '都督',
                '人马', '不知', '汉中', '只见', '众将', '后主', '蜀兵', '上马', '大叫', '太守', '此人', '夫人', '先主',
                '后人', '背后', '城中', '天子', '一面', '何不', '忽报', '先生', '百姓', '何故', '然后', '先锋', '不如',
                '赶来']

    for i in cut_san:
        if not i in excludes:
            if i == '孟德' or i == '丞相':
                i = '曹操'
            elif i == '玄德' or i == '玄德曰':
                i = '刘备'
            elif i == '孔明' or i == '孔明曰':
                i = '诸葛亮'
            elif i == '关公':
                i = '关羽'
            if len(i) > 1:
                if not dic.get(i):
                    dic[i] = 0
                dic[i] += 1

    sort_User = sorted(dic.items(), key=lambda t: t[1], reverse=True)
    return sort_User


# 绘图 直方图
def showResult(data, topN):
    print(data[:topN])

    X = range(topN)
    y = list()
    labels = list()
    for i in data[:topN]:
        labels.append(i[0])
        y.append(i[1])

    print(y)

    plt.bar(X, y)
    plt.xticks(X, labels)
    plt.title('三国人数统计')
    plt.xlabel('英雄人物')
    plt.ylabel('次数')
    plt.show()


if __name__ == '__main__':
    # 读取文件
    with open('Data/sanguo.txt', 'r', encoding='utf-8') as f:
        sanTxt = f.read()

    # cut_san = list(jieba.cut(sanTxt))
    # print(cut_san)

    sort_User = cutSan(sanTxt)
    print(sort_User)
    showResult(sort_User, 10)