#
# Window Edited by Pycharm.
# Time : 2022/09/16
# Author : YU.J.P
#

"""
    版本: V1.4
    基本功能:
        1. 搜索引擎 - 索引搜索技术

"""
import os
import time
import tkinter as tk  # 窗口视窗
from tkinter import scrolledtext  # 消息窗口 带滑动条

from Experiment_2 import Ex2  # 导入实验2的基础类 - Wordsindex


# 自定义 GUI
class CustomGUI:
    __VERSION = 'MandySE-EX2 V1.4'  # 版本信息 私有

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
        # 提示标签
        self.labelText = tk.Label(self.root, text='点击按钮开始测试φ(>ω<*) ', font=("dengxian", 12))
        self.labelText.place(x=580, y=100)
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
        self.filePath = 'Data/实验2.2_单文档查找用例.txt'
        # self.filePath = 'Data/Romeo And Juliet.txt'
        # self.filePath = 'Data/sanguo.txt'
        self.outPath = 'Data/wordsIndex.txt'  # 既是输出文件路径 又是导入文件路径

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
        self.labelText.place(x=580, y=100)

    # 按钮2  建立索引表
    def buildIndexTable(self):
        self.index_Ob = Ex2.WordsIndex(self.filePath)  # 建立对象
        indexDic = self.index_Ob.indexDic  # 直接获取索引字典
        self.index_Ob.outputInFile(self.outPath)  # 写入文件
        self.labelText = tk.Label(self.root, text='索引表建立成功(o´ω`o)ﾉ', font=("dengxian", 12))
        self.labelText.place(x=580, y=100)

    # 搜索关键字
    def findKey(self):
        # 清空窗体内容
        self.text.delete(1.0, 'end')  # 文本框
        print('# 删除原始数据...')

        # 开始搜索
        with open(self.filePath, 'r', encoding='utf-8') as f:
            S = f.read()
        P = self.entry.get()  # 获取模式串
        # 异常处理 P
        print("# 关键字：" + P)
        S_len, P_len = len(S), len(P)

        start = time.time()  # 开始计时
        indexDic = Ex2.WordsIndex.inputFromFile(self.outPath)  # 导入文件 获取索引字典

        # # 获取索引列表 并打印
        # keyList, valueList = list(indexDic.keys()), list(indexDic.values())
        # for i in range(0, len(keyList)):
        #     print(Ex2.Color.green + "%-15s" % keyList[i], end='\t')  # 左对齐
        #     for elem in valueList[i]:
        #         print(Ex2.Color.carmine + "", elem, end=',')
        #     print()

        position = Ex2.WordsIndex.getPosition(P, indexDic)
        loseTime = time.time() - start
        print("查找用时: ", loseTime)  # 结束计时
        print("索引位置：", position)

        if len(position) == 0:
            self.labelText = tk.Label(self.root, text='关键词不存在o(╥﹏╥)o', font=("dengxian", 12))
            self.labelText.place(x=580, y=100)
        else:
            self.labelText = tk.Label(self.root, text='关键词查找成功(*/ω＼*)', font=("dengxian", 12))
            self.labelText.place(x=580, y=100)

        self.text.tag_config('tag_black_white', foreground='black', background='white')
        self.text.tag_config('tag_green_yellow', foreground='green', background='yellow')

        count = 0
        for index in position:
            while count < index:  # 普通显示
                # print(Ex2.Color.black + S[count], end="")
                self.text.insert('insert', S[count], 'tag_black_white')
                count += 1  # 加空格
            for i in range(0, P_len):  # 关键高亮显示
                # print(Ex2.Color.green + S[count], end="")
                self.text.insert('insert', S[count], 'tag_green_yellow')
                count += 1  # 加空格
        while count < S_len:  # 普通显示
            # print(Ex2.Color.black + S[count], end="")
            self.text.insert('insert', S[count], 'tag_black_white')
            count += 1  # 加空格


# 运行
if __name__ == '__main__':
    CustomGUI().root.mainloop()
