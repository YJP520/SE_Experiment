#
# Window Edited by Pycharm.
# Time : 2022/09/14
# Author : YU.J.P
#

"""
    版本: V1.2
    基本功能:
        1. 搜索引擎简易版

"""
import os
import time
import tkinter as tk  # 窗口视窗
from tkinter import scrolledtext  # 消息窗口

from Experiment_1 import Ex1


# 自定义 GUI
class CustomGUI:
    __VERSION = 'MandySE-EX1 V1.3'  # 版本信息 私有

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
        # 定义按钮
        self.button_1 = tk.Button(self.root, text='Update', width=6, height=1, command=self.upgradeData)
        self.button_1.place(x=580, y=30)
        self.button_2 = tk.Button(self.root, text='Find', width=6, height=1, command=self.findKey)
        self.button_2.place(x=690, y=30)

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
        # testTxt = "Data/test.txt"
        testTxt = "Data/sanguo.txt"
        if os.path.exists(testTxt):
            buffer = open(testTxt, 'r', encoding='utf-8')
            for content in buffer:
                self.text.insert('insert', content, 'tag_black_white')
            buffer.close()
        print('# 加载更新数据...')

    # 搜索关键字
    def findKey(self):
        # 清空窗体内容
        self.text.delete(1.0, 'end')  # 文本框
        print('# 删除原始数据...')

        # 开始搜索
        # with open('Data/Data/test.txt', 'r', encoding='utf-8') as f:
        with open('Data/sanguo.txt', 'r', encoding='utf-8') as f:
            S = f.read()
        P = self.entry.get()  # 获取模式串
        # 异常处理 P
        print("# 关键字：" + P)
        S_len, P_len = len(S), len(P)

        start = time.time()  # 开始计时
        position = Ex1.OrderMatch.BoyerMooreStringMatch(S, P)
        loseTime = time.time() - start
        print("查找用时: ", loseTime)  # 结束计时
        print("索引位置：", position)

        self.text.tag_config('tag_black_white', foreground='black', background='white')
        self.text.tag_config('tag_green_yellow', foreground='green', background='yellow')

        count = 0
        for index in position:
            while count < index:  # 普通显示
                # print(Ex1.Color.black + S[count], end="")
                self.text.insert('insert', S[count], 'tag_black_white')
                count += 1
            for i in range(0, P_len):  # 关键高亮显示
                # print(Ex1.Color.green + S[count], end="")
                self.text.insert('insert', S[count], 'tag_green_yellow')
                count += 1
        while count < S_len:  # 普通显示
            # print(Ex1.Color.black + S[count], end="")
            self.text.insert('insert', S[count], 'tag_black_white')
            count += 1


# 运行
if __name__ == '__main__':
    CustomGUI().root.mainloop()
