#
# Window Edited by Pycharm.
# Time : 2022/09/16
# Author : YU.J.P
#

"""
    版本: V1.4
    基本功能:
        1. 搜索引擎 - 索引搜索技术 扩展1 - sanguo.txt 主要人物索引

"""

import os
import time
import jieba  # 统计 分词
import json
import tkinter as tk  # 窗口视窗
from tkinter import scrolledtext  # 消息窗口 带滑动条
# from Experiment_2 import Ex2  # 导入实验2的基础类 - Wordsindex


# ------- 实现三国索类 ----------------------------------------------------------------------------------------
def cutSan(sanTxt):
    cut_san = list(jieba.cut(sanTxt))
    # print(cut_san)

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


# 索引查找技术 - 实验任务 2 文本建立单词索引表
class WordsIndex:
    # 构造函数
    def __init__(self, filePath):
        self.content = None  # 词表 二维
        self.mainFigure = None  # 主要人物表
        self.indexDic = {}  # 字典 记录所有的索引信息
        self.filePath = filePath  # 源文件路径
        self.makeIndexTable()  # 生成
        pass

    # 切分单词 - 去除末尾换行符 私有函数
    def _remove_n(self, string):
        if string[-1] == '\n':
            return string[: len(string) - 1]
        else:
            return string

    # 单词去符号 - 判断末尾符号 私有函数
    def _remove_char(self, string):
        if len(string) == 0:
            return False
        elif string[-1] in ",.;:!":
            return True
        else:
            return False

    # 切分单词 - 以空格切分出每一个单词 私有函数
    def _splitBlank(self, line):
        line = line.split(" ")  # 以空格切分出单词
        # filter函数接收一个函数和一个list，这个函数的作用是对list中每个元素进行判断
        # 自动过滤掉不符合条件的元素，返回符合条件的元素
        line = list(filter(lambda c: c != ' ', line))
        line[-1] = self._remove_n(line[-1])  # 去除换行
        return line

    # 根据词表建立索引表 - 主要人物索引表。。。
    def makeIndexTable(self):
        # 建立词表
        with open(self.filePath, 'r', encoding='utf-8') as f:
            sanTxt = f.read()
        self.content = list(jieba.cut(sanTxt))  # 内容分词
        # print(self.content)

        sort_User = cutSan(sanTxt)  # 得到出现次数最多的人物
        print(sort_User[:15])
        self.mainFigure = list(dict(sort_User[:15]).keys())  # 主要人物关键词
        print(self.mainFigure)

        # print(len(wordsList))
        # print(len(self.content))

        # 暴力算法 - 建立索引表 速度非常慢。。。。
        for figure in self.mainFigure:
            self.indexDic[figure] = []  # 每个单词都有一个索引列表
            count = 0  # 索引数值变量
            for index in self.content:
                if figure == index:  # 再比较是否相等
                    self.indexDic[figure].append(count)
                count += len(index)  # 偏移含符号的索引值
        print(self.indexDic)

        # BM算法 建立索引表
        # for figure in mainFigure:
        #     self.indexDic[figure] = self.BoyerMooreStringMatch(sanTxt, figure)
        # print(self.indexDic)

    # 索引表写入文件
    def outputInFile(self, outPath):
        fileOut = open(outPath, 'w', encoding='utf-8')  # 打开文件并写入
        # # 获取索引列表 并打印
        # keyList, valueList = list(self.indexDic.keys()), list(self.indexDic.values())
        # # fileOut.write("%-20s" % '关键词' + '\t' + '索引位置\n')  # 左对齐
        # for i in range(0, len(keyList)):
        #     fileOut.write("%-20s" % keyList[i] + '\t')  # 左对齐
        #     for elem in valueList[i]:
        #         fileOut.write('%d,' % elem)
        #     fileOut.write('\n')

        js = json.dumps(self.indexDic)  # json数据
        fileOut.write(js)
        fileOut.close()

    # 索引表导入文件 类方法
    @classmethod
    def inputFromFile(cls, inPath):
        fileIn = open(inPath, 'r', encoding='utf-8')  # 打开文件并读取
        js = fileIn.read()
        indexDic = json.loads(js)  # 数据转换
        fileIn.close()
        return indexDic

    # 反回对应单词的位置列表
    @classmethod
    def getPosition(cls, keyWord, indexDic):
        keyList, valueList = list(indexDic.keys()), list(indexDic.values())
        for i in range(0, len(keyList)):
            if keyWord == keyList[i]:
                return valueList[i]
        return []

        # 模式匹配 Boyer-Moore

    @classmethod
    def BoyerMooreStringMatch(cls, S, P):
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


# ------- 实现三国索类 ----------------------------------------------------------------------------------------


# 自定义 GUI
class CustomGUI:
    __VERSION = 'MandySE-EX2-ex1 V1.4'  # 版本信息 私有

    root_width = 800  # 窗口宽度
    root_height = 400  # 窗口高度

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
        self.entry = tk.Entry(self.root, width=18, font=("dengxian", 16))
        self.entry.place(x=580, y=0)
        # 显示带滑动条的文本框
        # self.text = tk.Text(self.root, height=20, width=70,font=("dengxian", 12), cursor="arrow")
        self.text = scrolledtext.ScrolledText(self.root, height=20, width=70,font=("dengxian", 12), cursor="arrow")
        self.text.place(x=0, y=0)
        # 主要人物显示
        self.text2 = scrolledtext.ScrolledText(self.root, height=10, width=24, font=("dengxian", 12), cursor="arrow")
        self.text2.place(x=580, y=160)
        # 提示标签
        self.labelText = tk.Label(self.root, text='点击按钮开始测试φ(>ω<*) ', font=("dengxian", 12))
        self.labelText.place(x=580, y=90)
        # 用时标签
        self.labelTime = tk.Label(self.root, text='用时:', font=("dengxian", 12))
        self.labelTime.place(x=580, y=120)
        # 定义按钮
        # update 更新显示内容
        self.button_1 = tk.Button(self.root, text='Update', width=6, height=1, command=self.upgradeData)
        self.button_1.place(x=580, y=30)
        # build 建立索引库
        self.button_2 = tk.Button(self.root, text='Build', width=6, height=1, command=self.buildIndexTable)
        self.button_2.place(x=650, y=30)
        # find 查找并高亮显示
        self.button_3 = tk.Button(self.root, text='Find', width=6, height=1, command=self.findKey)
        self.button_3.place(x=720, y=30)
        # 索引表对象
        self.index_Ob = None
        self.filePath = 'Data/sanguo.txt'
        self.outPath = 'Data/sanguoIndex.txt'  # 既是输出文件路径 又是导入文件路径

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
    def upgradeData(self):
        # 清空窗体内容
        # self.entry.delete(0, 'end')  # 输入框
        self.text.delete(1.0, 'end')  # 文本框
        print('# 删除原始数据...')

        # foreground字体颜色 font字体样式,大小等 background 背景色
        # 设置tag即插入文字的大小,颜色等
        self.text.tag_config('tag_red_yellow', foreground='red',background='yellow')
        self.text.tag_config('tag_green_yellow', foreground='green', background='yellow')
        self.text.tag_config('tag_blue_pink', foreground='blue', background='pink')
        self.text.tag_config('tag_blue_white', foreground='blue', background='white')
        self.text.tag_config('tag_black_white', foreground='black', background='white')

        # 加载文件数据
        if os.path.exists(self.filePath):
            buffer = open(self.filePath, 'r', encoding='utf-8')
            for content in buffer:
                self.text.insert('insert', content, 'tag_black_white')
            buffer.close()
        print('# 加载更新数据...')
        self.labelText = tk.Label(self.root, text='数据加载成功(｡･ω･｡)', font=("dengxian", 12))
        self.labelText.place(x=580, y=90)

    # 按钮2  建立索引表
    def buildIndexTable(self):
        start = time.time()  # 开始计时
        self.index_Ob = WordsIndex(self.filePath)  # 建立对象
        indexDic = self.index_Ob.indexDic  # 直接获取索引字典
        self.index_Ob.outputInFile(self.outPath)  # 写入文件
        loseTime = time.time() - start  # 用时
        print("建立索引用时: ", loseTime)  # 结束计时

        self.labelText = tk.Label(self.root, text='索引表建立成功(o´ω`o)ﾉ', font=("dengxian", 12))
        self.labelText.place(x=580, y=90)
        self.labelTime = tk.Label(self.root, text='用时:' + str(loseTime)[: 5] + 's', font=("dengxian", 12))
        self.labelTime.place(x=580, y=120)

        # 清空窗体内容
        self.text2.delete(1.0, 'end')  # 文本框
        print('# text2删除原始数据...')
        print('# text2加载新的数据...')
        self.text2.tag_config('tag_red_yellow', foreground='red', background='yellow')
        self.text2.insert('insert', "关键人物:\n", 'tag_red_yellow')
        for i in range(0, len(self.index_Ob.mainFigure)):
            self.text2.insert('insert', self.index_Ob.mainFigure[i] + ', ')
            if (i + 1) % 3 == 0:
                self.text2.insert('insert', '\n')

    # 搜索关键字
    def findKey(self):
        # 清空窗体内容
        self.text.delete(1.0, 'end')  # 文本框
        print('# text删除原始数据...')

        # 开始搜索
        with open(self.filePath, 'r', encoding='utf-8') as f:
            S = f.read()
        P = self.entry.get()  # 获取模式串
        # 异常处理 P
        print("# 关键字：" + P)
        S_len, P_len = len(S), len(P)

        start = time.time()  # 开始计时
        indexDic = WordsIndex.inputFromFile(self.outPath)  # 导入文件 获取索引字典

        # # 获取索引列表 并打印
        # keyList, valueList = list(indexDic.keys()), list(indexDic.values())
        # for i in range(0, len(keyList)):
        #     print(Ex2.Color.green + "%-15s" % keyList[i], end='\t')  # 左对齐
        #     for elem in valueList[i]:
        #         print(Ex2.Color.carmine + "", elem, end=',')
        #     print()

        position = WordsIndex.getPosition(P, indexDic)
        loseTime = time.time() - start
        print("查找用时: ", loseTime)  # 结束计时
        print("索引位置：", position)

        self.labelTime = tk.Label(self.root, text='用时:' + str(loseTime)[: 5] + 's', font=("dengxian", 12))
        self.labelTime.place(x=580, y=120)

        if len(position) == 0:
            self.labelText = tk.Label(self.root, text='关键词不存在o(╥﹏╥)o', font=("dengxian", 12))
            self.labelText.place(x=580, y=90)
        else:
            self.labelText = tk.Label(self.root, text='关键词查找成功(*/ω＼*)', font=("dengxian", 12))
            self.labelText.place(x=580, y=90)

        self.text.tag_config('tag_black_white', foreground='black', background='white')
        self.text.tag_config('tag_green_yellow', foreground='green', background='yellow')

        print('# text加载新的数据...')
        count = 0
        for index in position:
            while count < index:  # 普通显示
                # print(Ex2.Color.black + S[count], end="")
                self.text.insert('insert', S[count], 'tag_black_white')
                count += 1
            for i in range(0, P_len):  # 关键高亮显示
                # print(Ex2.Color.green + S[count], end="")
                self.text.insert('insert', S[count], 'tag_green_yellow')
                count += 1
        while count < S_len:  # 普通显示
            # print(Ex2.Color.black + S[count], end="")
            self.text.insert('insert', S[count], 'tag_black_white')
            count += 1


# 运行
if __name__ == '__main__':
    CustomGUI().root.mainloop()
