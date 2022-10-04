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
import time
import tkinter as tk  # 窗口视窗
from tkinter import scrolledtext  # 消息窗口 带滑动条


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
class KS_PRO:
    def __init__(self):
        pass

    @classmethod
    def cutWords(cls, content):
        """
        jieba分词
        :param content: 文本内容
        :return: 分词列表
        """
        return list(jieba.cut(content))

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
    def getSimilarity_list(cls, list1, list2):
        """
        获取两段文本content1和content2的相似度
        :param list1: 文本 1
        :param list2: 文本 2
        :param k: 间隔长度
        :return: 相似度百分比
        """
        if list1 == list2:
            return 1
        set1, set2 = set(list1), set(list2)  # 集合1 & 集合2
        # print(Color.blue, set1)
        # print(Color.blue, set2)
        return 1.0 * len(set1 & set2) / len(set1 | set2)
        # inter = len(profile1.keys()) + len(profile2.keys()) - len(set1)
        # return 1.0 * inter / len(set1)

    @classmethod
    def test_1(cls):  # Kshingle 测试函数
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

        list1 = cls.cutWords(content1)
        wordsList1 = []
        for index in list1:
            if index not in "，。《》、？；：‘”【{】}、|=+-——）（*&……%￥#@！ ,<.>/?\'\";:[{]}=+-_)(*&^%$#@!":
                wordsList1.append(index)
        # print(Color.green, wordsList1)

        list2 = cls.cutWords(content2)
        wordsList2 = []
        for index in list2:
            if index not in "，。《》、？；：‘”【{】}、|=+-——）（*&……%￥#@！ ,<.>/?\'\";:[{]}=+-_)(*&^%$#@!":
                wordsList2.append(index)
        # print(Color.carmine, wordsList2)

        commonWords = set(wordsList1) & set(wordsList2)
        # print(Color.blue, commonWords)

        for index in list1:
            if index in commonWords:
                print(Color.green + index, end='')
            else:
                print(Color.black + index, end='')

        print("\n")
        for index in list2:
            if index in commonWords:
                print(Color.red + index, end='')
            else:
                print(Color.black + index, end='')

        # K_value = 2
        # print(Color.red, cls.getSimilarity(content1, content2, K_value))
        print(Color.red, '\nsimilarity =', cls.getSimilarity_list(wordsList1, wordsList2))


# -------------------------------------------------------------------------------------------------------------

# 自定义 GUI
class CustomGUI:
    __VERSION = 'MandySE-EX4_T2 V1.0'  # 版本信息 私有

    root_width = 800  # 窗口宽度
    root_height = 600  # 窗口高度

    # 构造函数
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(self.__VERSION)  # 窗体名
        self.root.geometry(str(self.root_width) + 'x' + str(self.root_height) + '+500+150')
        # 创建主菜单实例
        self.menubar = tk.Menu(self.root)
        # 显示菜单,将root根窗口的主菜单设置为menu
        self.root.config(menu=self.menubar)
        # 加载组件
        self.interface()
        # 输入框
        self.entry = tk.Entry(self.root, width=30, font=("dengxian", 16))
        self.entry.place(x=50, y=0)
        # 显示带滑动条的文本框
        # self.text = tk.Text(self.root, height=20, width=70,font=("dengxian", 12), cursor="arrow")
        self.text1 = scrolledtext.ScrolledText(self.root, height=20, width=45,font=("dengxian", 12), cursor="arrow")
        self.text1.place(x=0, y=200)
        self.text2 = scrolledtext.ScrolledText(self.root, height=20, width=45,font=("dengxian", 12), cursor="arrow")
        self.text2.place(x=420, y=200)
        self.colorInit()  # 颜色tag
        # 提示标签
        self.labelText = tk.Label(self.root, text='点击按钮开始测试φ(>ω<*) ', font=("dengxian", 12))
        self.labelText.place(x=50, y=100)
        # 定义按钮
        # update 更新显示内容 1
        self.button_1 = tk.Button(self.root, text='Update1', width=6, height=1, command=self.upgradeData_1)
        self.button_1.place(x=50, y=30)
        # update 更新显示内容 2
        self.button_2 = tk.Button(self.root, text='Update2', width=6, height=1, command=self.upgradeData_2)
        self.button_2.place(x=150, y=30)
        # find 查找并高亮显示
        self.button_3 = tk.Button(self.root, text='Find', width=6, height=1, command=self.findKey)
        self.button_3.place(x=250, y=30)
        # 文件 内容
        self.filePath1 = 'Data/Ex4_T2_Data/content1.txt'
        self.content1 = None  # 内容 1
        self.filePath2 = 'Data/Ex4_T2_Data/content2.txt'
        self.content2 = None  # 内容 2

    def colorInit(self):
        # foreground字体颜色 font字体样式,大小等 background 背景色
        # 设置tag即插入文字的大小,颜色等
        self.text1.tag_config('tag_red_yellow', foreground='red', background='yellow')
        self.text1.tag_config('tag_red_white', foreground='red', background='white')
        self.text1.tag_config('tag_green_yellow', foreground='green', background='yellow')
        self.text1.tag_config('tag_green_white', foreground='green', background='white')
        self.text1.tag_config('tag_blue_pink', foreground='blue', background='pink')
        self.text1.tag_config('tag_blue_white', foreground='blue', background='white')
        self.text1.tag_config('tag_black_white', foreground='black', background='white')

        self.text2.tag_config('tag_red_yellow', foreground='red', background='yellow')
        self.text2.tag_config('tag_red_white', foreground='red', background='white')
        self.text2.tag_config('tag_green_yellow', foreground='green', background='yellow')
        self.text2.tag_config('tag_green_white', foreground='green', background='white')
        self.text2.tag_config('tag_blue_pink', foreground='blue', background='pink')
        self.text2.tag_config('tag_blue_white', foreground='blue', background='white')
        self.text2.tag_config('tag_black_white', foreground='black', background='white')

    # 加载组件
    def interface(self):
        """"界面编写位置"""
        # 在 menubar 上设置菜单名，并关联一系列子菜单
        self.menubar.add_cascade(label="文件", menu=self.papers())
        self.menubar.add_cascade(label="查看", menu=self.about())

    # "文件" 指示按钮
    def papers(self):
        # menu = tk.Menu(self.menubar, tearoff=1)  # 创建子菜单实例
        # 1的话多了一个虚线,如果点击的话就会发现,这个菜单框可以独立出来显示
        menu = tk.Menu(self.menubar, tearoff=0)
        # 创建单选框
        for item in ['新建', '打开', '保存', '另存为']:
            menu.add_command(label=item)
        return menu

    # "查看" 指示按钮
    def about(self):
        amenu = tk.Menu(self.menubar, tearoff=0)
        # 添加复选框
        for item in ['项目复选框', '文件扩展名', '隐藏的项目']:
            amenu.add_checkbutton(label=item)
        return amenu

    # 定义一个插入在鼠标所在位置的函数
    def upgradeData_1(self):
        # 清空窗体内容
        # self.entry.delete(0, 'end')  # 输入框
        self.text1.delete(1.0, 'end')  # 文本框
        print('# text1删除原始数据...')

        # 加载文件数据
        if os.path.exists(self.filePath1):
            buffer = open(self.filePath1, 'r', encoding='utf-8')
            for content in buffer:
                self.text1.insert('insert', content, 'tag_black_white')
            buffer.close()
        print('# text1加载更新数据...')
        self.labelText = tk.Label(self.root, text='text1数据加载成功(｡･ω･｡)', font=("dengxian", 12))
        self.labelText.place(x=50, y=150)

    # 定义一个插入在鼠标所在位置的函数
    def upgradeData_2(self):
        # 清空窗体内容
        # self.entry.delete(0, 'end')  # 输入框
        self.text2.delete(1.0, 'end')  # 文本框
        print('# text2删除原始数据...')

        # 加载文件数据
        if os.path.exists(self.filePath2):
            buffer = open(self.filePath2, 'r', encoding='utf-8')
            for content in buffer:
                self.text2.insert('insert', content, 'tag_black_white')
            buffer.close()
        print('# text2加载更新数据...')
        self.labelText = tk.Label(self.root, text='text2数据加载成功(｡･ω･｡)', font=("dengxian", 12))
        self.labelText.place(x=50, y=150)

    # 搜索关键字
    def findKey(self):
        # 清空窗体内容
        self.text1.delete(1.0, 'end')  # 文本框
        print('# 删除text1原始数据...')
        self.text2.delete(1.0, 'end')  # 文本框
        print('# 删除text2原始数据...')

        # 开始搜索
        with open(self.filePath1, 'r', encoding='utf-8') as f1:
            self.content1 = f1.read()
        f1.close()
        with open(self.filePath2, 'r', encoding='utf-8') as f2:
            self.content2 = f2.read()
        f2.close()

        list1 = KS_PRO.cutWords(self.content1)
        wordsList1 = []
        for index in list1:
            if index not in "，。《》、？；：‘”【{】}、|=+-——）（*&……%￥#@！ ,<.>/?\'\";:[{]}=+-_)(*&^%$#@!":
                wordsList1.append(index)
        # print(Color.green, wordsList1)

        list2 = KS_PRO.cutWords(self.content2)
        wordsList2 = []
        for index in list2:
            if index not in "，。《》、？；：‘”【{】}、|=+-——）（*&……%￥#@！ ,<.>/?\'\";:[{]}=+-_)(*&^%$#@!":
                wordsList2.append(index)
        # print(Color.carmine, wordsList2)

        commonWords = set(wordsList1) & set(wordsList2)
        # print(Color.blue, commonWords)

        for index in list1:
            if index in commonWords:
                self.text1.insert('insert', index, 'tag_green_white')
            else:
                self.text1.insert('insert', index, 'tag_black_white')

        print("\n")
        for index in list2:
            if index in commonWords:
                self.text2.insert('insert', index, 'tag_red_white')
            else:
                self.text2.insert('insert', index, 'tag_black_white')

        print('# 查重更新数据...')
        similarity = KS_PRO.getSimilarity_list(wordsList1, wordsList2)
        print(Color.red, '\nsimilarity =', similarity)
        self.labelText = tk.Label(self.root, text='查重数据加载成功(｡･ω･｡) 相似度为' + '%.3g' % similarity, font=("dengxian", 12))
        self.labelText.place(x=50, y=150)

# -------------------------------------------------------------------------------------------------------------

# 运行
if __name__ == '__main__':
    # KS_PRO.test_1()  # 测试函数
    CustomGUI().root.mainloop()