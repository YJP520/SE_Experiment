"""
    @Time : 2022/09/12
    @Author : YU.J.P
    @Project : 实验 1 顺序检索技术
    @Description:
        DraftHistory.

"""

# 一个似乎有问题的算法。。。
class OrderMatch:

    # 模式串是否存在指定字符
    @classmethod
    def isCharacterIn(cls, string, character):
        try:
            pos = string.index(character)  # P 中包含 character
        except ValueError:
            pos = -1  # P 不包含 character
        return pos

    # 对比两个字符串
    @classmethod
    def match(cls, str1, str2):
        l1 = len(str1) - 1
        l2 = len(str2) - 1

        if l1 != l2:  # 长度不等 直接跳过
            return -2, None
        while l1 >= 0:  # 逆向依次比对字符
            if str1[l1] != str2[l1]:  # 坏字符
                return l1, str1[l1]  # 返回坏字符位置
            l1 -= 1  # 递减
        return 0, None  # 比对成功

    # 模式匹配 Boyer-Moore
    @classmethod
    def BoyerMooreStringMatch(cls, S, P):
        position = []  # 索引列表
        P_length = len(P) - 1
        S_length = len(S) - 1
        start, end = 0, 0  #
        while S_length > 0:
            end = start + len(P)  # 更新end
            print(S[start:end])  # 打印此时的对比串
            matchResult = OrderMatch.match(S[start:end], P)  # 比对的结果
            if matchResult[0] == -2:  # 找到尾部 结束
                break
            if matchResult[0] == 0:  # 此时已经找到一个
                position.append(start)
                start += len(P)  # 重新开始查找下一个
            else:  # 坏字符
                # 返回的坏字符 是否在P中存在 然后进行对齐
                pos = OrderMatch.isCharacterIn(P, matchResult[1])
                if matchResult[0] == P_length:  # 尾部第一个字符不同
                    if pos != -1:  # P包含坏字符 P移动对齐
                        start += len(P) - 1 - pos
                    else:
                        start += len(P)  # 坏字符不包含 直接跳过
                else:  # 有相同后缀
                    print("do")
                    # if pos == -1:
                    # 好后缀原则
                    goodPos = OrderMatch.isCharacterIn(P, P[P_length])
                    if goodPos == P_length:  #
                        start += P_length + 1
                    else:
                        start += P_length - goodPos
                    print("there...")
        return position


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

# 颜色输出类
class Color:
    def __init__(self):
        pass

    # 测试颜色
    @classmethod
    def getRed_Yellow(cls):
        # ---1-高亮显示 31-前景色红色  43-背景色黄色---
        return '\033[1;31;43m'

    # 黑色
    @classmethod
    def getBlack_White(cls):
        # ---1-高亮显示 30-前景色黑色  47-背景色白色---
        return '\033[1;30;47m'

    # 红色
    @classmethod
    def getRed_White(cls):
        # ---1-高亮显示 31-前景色红色  47-背景色白色---
        return '\033[1;31;47m'

    # 绿色
    @classmethod
    def getGreen_White(cls):
        # ---1-高亮显示 32-前景色绿色  47-背景色白色---
        return '\033[1;32;47m'

    # 蓝色
    @classmethod
    def getBlue_White(cls):
        # ---1-高亮显示 34-前景色蓝色  47-背景色白色---
        return '\033[1;34;47m'

