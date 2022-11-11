#
# Crawler Edited by Pycharm.
# Time : 2022/10/07
# Author : YU.J.P
#

"""
    版本: V1.0
    基本功能:
        - 网页的重要性计算

    实验要求:
         给定网页链接关系，根据PageRank的计算公式计算网页的PR值，直到每个网页的PR值稳定为止，列出最终的PR值；
          假设每个网页的初始PR值相等。（计算结果保留小数点后5位数）
         根据PR值对网页重要性进行排序；如果有1,000,000个网页，你将使用什么排序技术，写出排序算法，查资料分析它与其它算法的优劣。
         扩展实验1：使用TextRank提取给定句子中的关键词。
         扩展实验2：利用NetworkX包(或其它)用图示的方式表示网络图。
         扩展实验3：利用NetworkX画出希拉里邮件中的人物关系图。

"""

import urllib.request

import networkx as nx
import requests
import BitVector as BitVector
from bs4 import BeautifulSoup
import re
import os
import jieba
from matplotlib import pyplot as plt
from pygraph.classes.digraph import digraph


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
# 利用NetworkX包(或其它)用图示的方式表示网络图。
def test1():
    G = nx.petersen_graph()
    plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.subplot(122)
    nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    plt.show()


def test2():
    G = nx.cycle_graph(12)
    pos = nx.spring_layout(G, iterations=200)
    nx.draw(G, pos, node_color=range(12), node_size=800, cmap=plt.cm.Greens)
    plt.show()


def test3():
    G = nx.DiGraph()
    # 添加节点z
    G.add_node('c')
    G.add_node('d')
    # 添加节点 1 2 3
    G.add_nodes_from(['d', 'e', 'g'])
    G.add_nodes_from([1, 2, 3])
    # 添加边  起点为x  终点为y
    G.add_edge('a', 'b')
    G.add_edge('c', 'd')
    # 添加多条边
    G.add_edges_from([('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'g'), ('e', 'g')])
    G.add_edges_from([(1, 2), (1, 3), (2, 3)])

    # 网络图绘制与显示
    nx.draw(G, with_labels=True)
    plt.show()


def test4():
    # 初始化一个有向图对象
    DG = nx.DiGraph()
    DG.add_node('YU')
    # 添加节点   传入列表
    DG.add_nodes_from(['A', 'B', 'C', 'D', 'E'])
    print(f'输出图的全部节点：{DG.nodes}')
    print(f'输出节点的数量：{DG.number_of_nodes()}')

    # 添加边  传入列表  列表里每个元素是一个元组  元组里表示一个点指向另一个点的边
    DG.add_edges_from([('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'A'), ('E', 'A'), ('E', 'D'), ('D', 'C'), ('B', 'C')])
    DG.add_edges_from([('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'A'), ('E', 'A'), ('E', 'D')])
    DG.add_edges_from([('A', 'YU'), ('B', 'YU'), ('C', 'YU'), ('D', 'YU'), ('E', 'YU')])
    print(f'输出图的全部边:{DG.edges}')
    print(f'输出边的数量：{DG.number_of_edges()}')

    # 可自定义节点颜色
    colors = ['pink', 'cyan', 'green', 'yellow', 'red', 'purple']
    # 运用布局
    pos = nx.circular_layout(DG)
    # 绘制网络图
    nx.draw(DG, pos=pos, with_labels=True, node_size=200, width=0.6, node_color=colors)
    # 展示图片
    plt.show()


# -------------------------------------------------------------------------------------------------------------

# MAIN
if __name__ == '__main__':
    # test1()  # 测试函数
    # test2()  # 测试函数
    # test3()  # 测试函数
    test4()  # 测试函数
    pass