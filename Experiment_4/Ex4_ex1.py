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
# 给利用K-shingle算法，计算两个给定文档的相似度，查找重复字符串，并将重复字符串高亮显示出来
# 文本查重技术 K-shingle
class KShingle:
    # 相似度阈值
    MINI_LIMIT = 0.5

    def __init__(self):
        pass

    @classmethod
    def getShingle(cls, content, k):
        """
        K-Shingle 获取字典
        :param content: 文本内容
        :param k: 间隔长度
        :return: dic
        """
        dic = dict()  # 新建字典
        for i in range(0, len(content) - k + 1):
            part = content[i:i + k]  # 拆分词
            if part in dic:  # 重复单词数量 +1
                dic[part] += 1
            else:  # 新单词赋值为 1
                dic[part] = 1
        return dic  # 返回字典

    @classmethod
    def getSimilarity(cls, content1, content2, k):
        """
        获取两段文本content1和content2的相似度
        :param content1: 文本 1
        :param content2: 文本 2
        :param k: 间隔长度
        :return: 相似度百分比
        """
        if content1 == content2:
            return 1
        set1, set2 = set(), set()  # 集合1 & 集合2
        profile1 = cls.getShingle(content1, k)  # 字典 1
        profile2 = cls.getShingle(content2, k)  # 字典 2
        for i in profile1.keys():
            set1.add(i)  # 加入到set中
        for i in profile2.keys():
            set2.add(i)  # 加入到set中
        # print(Color.blue, set1)
        # print(Color.blue, set2)
        return 1.0 * len(set1 & set2) / len(set1 | set2)
        # inter = len(profile1.keys()) + len(profile2.keys()) - len(set1)
        # return 1.0 * inter / len(set1)

    @classmethod
    def getSimilarContent(cls, content1, content2, k):
        """
        获取两段文本content1和content2的相似度
        :param content1: 文本 1
        :param content2: 文本 2
        :param k: 间隔长度
        :return: 相似内容
        """
        profile1 = cls.getShingle(content1, k)  # 字典 1
        profile2 = cls.getShingle(content2, k)  # 字典 2
        return set(profile1.keys()) & set(profile2.keys())

    @classmethod
    def test_1(cls):  # Kshingle 测试函数
        print(Color.green, 'Experiment_4', Color.yellow, '---', Color.carmine, 'Ex4_ex1')

        basePath = "F:/Projects/Python Pycharm/SE_Experiment/Experiment_4/Data/Ex2_ex1_Data"
        folder = os.listdir(basePath)

        # print(type(folder))
        # for index in folder:
        #     print(Color.green + '# ', index)

        # path = 'F:/Projects/Python Pycharm/SE_Experiment/Experiment_4/Data'
        # for dirPath, dirNames, fileNames in os.walk(path):
        #     print(Color.carmine, dirPath, dirNames, fileNames)

        content1 = '我在重庆的重庆理工大学'
        for index in folder:
            print(Color.blue, "----------------------------------------------------------------")
            print(Color.black, 'content1:' + content1)  # 打印原文本
            filePath = basePath + '/' + index
            with open(filePath, 'r', encoding='utf-8') as f:
                content2 = f.read()
            f.close()
            print(Color.yellow, 'content2:' + content2)  # 打印原文本
            K_value = 2
            dic = cls.getShingle(content2, K_value)  # 调用测试
            # print(Color.blue, dic)  # 打印字典
            similarity = cls.getSimilarity(content1, content2, K_value)
            print(Color.red, 'similarity =', similarity)

            if similarity >= KShingle.MINI_LIMIT:
                similarContent = cls.getSimilarContent(content1, content2, K_value)
                print(Color.carmine,'文件名:', index)
                print(Color.green,  '重复:', similarContent)


# -------------------------------------------------------------------------------------------------------------

# 运行
if __name__ == '__main__':
    KShingle.test_1()  # 测试函数
    pass
