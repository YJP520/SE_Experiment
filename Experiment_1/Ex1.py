"""
    @Time : 2022/09/12
    @Author : YU.J.P
    @Project : 实验 1 顺序检索技术
    @Description:
        Set up on 2022/09/12 - Finish Some Algorithms(BE and KMF).
        Upgrade on 2022/09/13 - Establish OrderMatch class and Finish BM.

"""

import time

'''
    说明：
    前景色         背景色           颜色
    ---------------------------------------
    30                40              黑色
    31                41              红色
    32                42              绿色
    33                43              黃色
    34                44              蓝色
    35                45              洋红
    36                46              青色
    37                47              白色
    显示方式             　 意义
    ----------------------------------
    0                    终端默认设置
    1                    高亮显示
    22　　　　　　　　　　 非高亮显示
    4                    使用下划线
    24　　　　　　　　　　 去下划线
    5                    闪烁
    25　　　　　　　　　　 去闪烁
    7                    反显
    27　　　　　　　　　　 非反显
    8                    不可见
    28　　　　　　　　　　 可见

    例：
    \033[1;32;41m   #---1-高亮显示 32-前景色绿色  41-背景色红色---
    \033[0m         #---采用终端默认设置，即取消后面输入的字体颜色---

'''


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


# 信息处理类
class OrderMatch:
    def __init__(self):
        pass

    # Brute Force - BF串匹配算法 查找一次
    @classmethod
    def BruteForceStringMatch(cls, S, P):
        for i in range(0, len(S) - 1):
            j = 0
            while S[i + j] == P[j] and j < len(P):
                j += 1
                if j == len(P):
                    return i
        return -1

    # Brute Force - BF串匹配算法 查找多次
    @classmethod
    def BruteForceStringMatchAll(cls, S, P, pos=0):
        position = []  # 索引列表
        S_len, P_len = len(S), len(P)
        for i in range(pos, S_len - 1):
            j = 0
            while S[i + j] == P[j] and j < P_len:
                j += 1
                if j == P_len:
                    position.append(i)  # 找到一个就加到列表中
                    break  # 退出此层循环
        return position  # 返回列表

    # 首先计算模式串的Next数组  这里是用回溯进行计算的
    @classmethod
    def calNext(cls, string):
        i = 0
        Next = [-1]
        j = -1
        while i < len(string) - 1:
            if j == -1 or string[i] == string[j]:  # 首次分析可忽略
                i += 1
                j += 1
                Next.append(j)
            else:
                j = Next[j]  # 会重新进入上面那个循环
        return Next

    # KMP算法 查找一次
    @classmethod
    def KMP_StringMatch(cls, S, P, pos=0):  # 从那个位置开始比较
        Next = OrderMatch.calNext(P)  # 计算 Next数组
        i = pos  # 开始位置，默认为 0
        j = 0
        while i < len(S) and j < len(P):
            if j == -1 or S[i] == P[j]:
                i += 1
                j += 1
            else:
                j = Next[j]
        if (j >= len(P)):
            return i - len(P)  # 说明匹配到最后了
        else:
            return 0

    # KMP算法 查找多次
    @classmethod
    def KMP_StringMatchAll(cls, S, P, pos=0):  # 从那个位置开始比较
        position = []  # 索引列表
        Next = OrderMatch.calNext(P)  # 计算 Next数组
        S_len, P_len = len(S), len(P)
        i = pos  # 开始位置，默认为 0
        j = 0
        while i < S_len and j < P_len:
            if j == -1 or S[i] == P[j]:
                i += 1
                j += 1
            else:
                j = Next[j]
            if j >= P_len:  # 说明匹配到最后了
                position.append(i - P_len)
                i += 1  # 更新位置
                j = 0  # 更新索引
        return position  # 返回列表

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


# 调用测试  Brute Force
def test1():
    print("---- Test1 ----")
    S = 'ABCDABCFGHIJKABCFGHIJKABCFGHIJKABCFGHIJKABCFGHIJK'
    P = 'ABCF'
    print(S)
    print(P)
    # print("索引位置：", OrderMatch.BruteForceStringMatch(S, P))
    print("索引位置：", OrderMatch.BruteForceStringMatchAll(S, P))


# 调用测试  KMP
def test2():
    print("---- Test2 ----")
    S = "ABCDABCFGHIJKABCFGHIJKABCFGHIJKABCFGHIJKABCFGHIJK"
    P = "ABCF"
    print(S)
    print(P)
    print("ABCF的Next数组: ", OrderMatch.calNext(P))
    # print("索引位置：", OrderMatch.KMP_StringMatch(S, P))
    print("索引位置：", OrderMatch.KMP_StringMatchAll(S, P))


# 调用测试 Boyer-Moore
def test3():
    print("---- Test3 ----")
    S = "CGTGCCTACTTACTTACTTACGAGAACGTGCCTACTTACTTACTTACGAGAACGTGCCTACTTACTTACTTACGAGAA"
    P = "CTTACTTAC"
    print(S)
    print(P)
    print("索引位置：", OrderMatch.BoyerMooreStringMatch(S, P))


# 整体测试
def testAll():
    # 读取文件
    with open('Data/sanguo.txt', 'r', encoding='utf-8') as f:
        sanTxt = f.read()
    # print(sanTxt)
    P = '诸葛亮'

    # 读取文件
    # with open('Data/Data/Jane Eyre.txt', 'r', encoding='utf-8') as f:
    #     sanTxt = f.read()
    # # print(sanTxt)
    # P = 'Hebrides'

    start = time.time()  # 开始计时
    print("索引位置：", OrderMatch.BruteForceStringMatchAll(sanTxt, P))
    theTime = time.time() - start  # 结束计时
    print(theTime)

    start = time.time()  # 开始计时
    print("索引位置：", OrderMatch.KMP_StringMatchAll(sanTxt, P))
    theTime = time.time() - start  # 结束计时
    print(theTime)

    start = time.time()  # 开始计时
    print("索引位置：", OrderMatch.BoyerMooreStringMatch(sanTxt, P))
    theTime = time.time() - start  # 结束计时
    print(theTime)
    pass


# 颜色显示测试
def testColor():
    print(Color.carmine + "Test")
    print(Color.green + "Test")
    print(Color.blue + "Test")
    print(Color.yellow + "Test")
    print(Color.red + "Test")
    print(Color.black + "Test")


# 搜索关键字高亮显示
def show():
    with open('Data/sanguo.txt', 'r', encoding='utf-8') as f:
        S = f.read()
    P = '曹操'
    S_len, P_len = len(S), len(P)

    start = time.time()  # 开始计时
    # position = OrderMatch.BruteForceStringMatchAll(S, P)
    # position = OrderMatch.KMP_StringMatchAll(S, P)
    position = OrderMatch.BoyerMooreStringMatch(S, P)
    print("索引位置：", position)
    print(time.time() - start)  # 结束计时

    # 控制台打印
    count = 0
    for index in position:
        # print(index)
        while count < index:
            print(Color.black + S[count], end="")
            count += 1
        for i in range(0, P_len):
            print(Color.green + S[count], end="")
            count += 1
    while count < S_len:
        print(Color.black + S[count], end="")
        count += 1


# 运行时间比拼：
def runningTime1():
    with open('Data/Romeo And Juliet.txt', 'r', encoding='utf-8') as f:
        S = f.read()

    figures = ['ROMEO', 'JULIET', 'MERCUTIO', 'the', 'are', "is", 'you', 'love', 'sorry', 'happy']
    print(figures)

    start = time.time()  # 开始计时
    for figure in figures:
        position = OrderMatch.BruteForceStringMatchAll(S, figure)
        # print("索引位置：", position)
    theTime = time.time() - start
    print("BF查找时间：", theTime)  # 结束计时

    start = time.time()  # 开始计时
    for figure in figures:
        position = OrderMatch.KMP_StringMatchAll(S, figure)
        # print("索引位置：", position)
    theTime = time.time() - start
    print("KMP查找时间：", theTime)  # 结束计时

    start = time.time()  # 开始计时
    for figure in figures:
        position = OrderMatch.BoyerMooreStringMatch(S, figure)
        # print("索引位置：", position)
    theTime = time.time() - start
    print("BM查找时间：", theTime)  # 结束计时


# 运行时间比拼：
def runningTime2():
    with open('Data/sanguo.txt', 'r', encoding='utf-8') as f:
        S = f.read()

    figures = ['曹操', '诸葛亮', '刘备', '关羽', '张飞', '吕布', '孙权', '云长',
               '赵云', '司马懿', '周瑜', '袁绍', '马超', '魏延', '黄忠' ]
    print(figures)

    start = time.time()  # 开始计时
    for figure in figures:
        position = OrderMatch.BruteForceStringMatchAll(S, figure)
        # print("索引位置：", position)
    theTime = time.time() - start
    print("BF查找时间：", theTime)  # 结束计时

    start = time.time()  # 开始计时
    for figure in figures:
        position = OrderMatch.KMP_StringMatchAll(S, figure)
        # print("索引位置：", position)
    theTime = time.time() - start
    print("KMP查找时间：", theTime)  # 结束计时

    start = time.time()  # 开始计时
    for figure in figures:
        position = OrderMatch.BoyerMooreStringMatch(S, figure)
        # print("索引位置：", position)
    theTime = time.time() - start
    print("BM查找时间：", theTime)  # 结束计时


# 运行
if __name__ == "__main__":
    # test1()  # 调用测试  Brute Force
    # test2()  # 调用测试  KMP
    # test3()  # 调用测试 Boyer-Moore
    # testAll()  # 整体测试
    # testColor()  # 颜色显示测试
    # show()  # 搜索关键字高亮显示
    # runningTime1()  # 运行时间比拼
    # runningTime2()  # 运行时间比拼
    pass

