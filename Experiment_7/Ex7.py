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
import requests
import BitVector as BitVector
from bs4 import BeautifulSoup
import re
import os
import jieba
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

class PageRank:
    def __init__(self):
        pass


class PRIterator:
    __doc__ = '''计算一张图中的PR值'''

    def __init__(self, dg):
        self.damping_factor = 0.85  # 阻尼系数,即d
        self.max_iterations = 100  # 最大迭代次数
        self.min_delta = 0.00001  # 确定迭代是否结束的参数,即ϵ
        self.graph = dg  # 要计算的图

    def page_rank(self):
        for node in self.graph.nodes():
            if len(self.graph.neighbors(node)) == 0:
                for node2 in self.graph.nodes():
                    digraph.add_edge(self.graph, (node, node2))

        nodes = self.graph.nodes()
        graph_size = len(nodes)

        if graph_size == 0:
            return {}
        page_rank = dict.fromkeys(nodes, 1.0 / graph_size)
        damping_value = (1.0 - self.damping_factor) / graph_size
        flag = False

        for i in range(self.max_iterations):
            change = 0
            for node in nodes:
                rank = 0
                for incident_page in self.graph.incidents(node):
                    rank += self.damping_factor * (page_rank[incident_page] / len(self.graph.neighbors(incident_page)))
                    rank += damping_value
                    change += abs(page_rank[node] - rank)  # 绝对值
                    page_rank[node] = rank
            print(Color.yellow, "# This is NO.%s iteration" % (i + 1), end=' ')
            print(Color.blue, page_rank)
            if change < self.min_delta:
                flag = True
                break
        if flag:
            print(Color.carmine, "# finished in %s iterations!" % node)
        else:
            print(Color.green, "# finished out of 100 iterations!")
        return page_rank

    @classmethod
    def read_data(cls, path):
        node_list = []
        edge_list = []
        with open(path) as f:
            lines = f.readlines()
            nodes = lines[1].split(' ')
            nodes[-1] = nodes[-1].split('\n')[0]
        for node in nodes:
            node_list.append(node)
            edges = lines[3:]
        for edge in edges:
            edge = edge.split(' ')
            edge[1] = edge[1].split('\n')[0]
            edge_list.append(edge)
        return node_list, edge_list

    @classmethod
    def test(cls):
        path = 'Data/Ex5_T1_Data/pagerank_four_nodes.txt'
        # path = 'Data/Ex5_T1_Data/pagerank_seven_nodes.txt'
        node_list, edge_list = cls.read_data(path)
        print(Color.carmine, '# 顶点信息：', node_list)
        print(Color.carmine, '# 边信息：', edge_list)

        dg = digraph()
        dg.add_nodes(node_list)
        for edg in edge_list:
            dg.add_edge(edg)

        pr = PRIterator(dg)
        page_ranks = pr.page_rank()
        print(Color.green, "# The final page rank is", page_ranks)


# -------------------------------------------------------------------------------------------------------------

# 图 1
def test2():
    G = nx.petersen_graph()
    plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.subplot(122)
    nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    plt.show()


# 图 2
def test3():
    G = nx.cycle_graph(24)
    pos = nx.spring_layout(G, iterations=200)
    nx.draw(G, pos, node_color=range(24), node_size=800, cmap=plt.cm.Blues)
    plt.show()


# -------------------------------------------------------------------------------------------------------------


# MAIN
if __name__ == '__main__':
    # PRIterator.test()  # 测试函数
    test2()  # 测试函数
    # test3()  # 测试函数
    pass
