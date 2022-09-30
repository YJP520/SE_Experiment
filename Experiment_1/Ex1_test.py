# coding=utf-8

"""
    Created on 2018/10/20
    @author: pureyang
    @description:

    Use and update on 2022/09/13
    @author: YU.J.P
    @description:
        实验 1 测试
"""

import jieba
import matplotlib.pyplot as plt

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
