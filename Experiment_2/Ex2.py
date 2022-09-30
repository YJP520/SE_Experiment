"""
    @Time : 2022/09/12
    @Author : YU.J.P
    @Project : 实验 2 索引检索技术
    @Description:
        Set up on 2022/09/16 - Establish IndexTable.
        Upgrade on 2022/09/17 -

"""
import json


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


# 索引查找技术 - 实验任务 1 指定书目建立单词索引表
class IndexSearch:
    # 构造函数
    def __init__(self, filePath):
        self.content = None  # 词表 二维
        self.indexDic = {}  # 字典 记录所有的索引信息
        self.filePath = filePath  # 源文件路径
        self.makeIndexTable()  # 完成创建
        pass

    # 切分单词 - 去除末尾换行符 私有函数
    def _remove_n(self, string):
        if string[-1] == '\n':
            return string[: len(string) - 1]
        else:
            return string

    # 切分单词 - 以空格切分出每一个单词 私有函数
    def _splitBlank(self, line):
        line = line.split(" ")  # 以空格切分出单词
        # filter函数接收一个函数和一个list，这个函数的作用是对list中每个元素进行判断
        # 自动过滤掉不符合条件的元素，返回符合条件的元素
        line = list(filter(lambda c: c != ' ', line))
        line[-1] = self._remove_n(line[-1])  # 去除换行
        return line

    # 建立词表 私有方法
    def _establishIndexTable(self):
        # 建立词表
        fileOS = open(self.filePath, 'r', encoding='utf-8')  # 打开文件
        try:
            self.content = fileOS.readlines()  # 行列表
            i = 0  # 变量
            while i < len(self.content):
                self.content[i] = self._splitBlank(self.content[i])
                i += 1
            # 打印测试
            # for line in content:   # 打印每行
            #     print(line)
        except Exception as e:
            print(e.args)  # 打印异常
        finally:
            fileOS.close()  # 关闭文件

    # 根据词表建立索引表
    def makeIndexTable(self):
        self._establishIndexTable()
        words = set()  # 记录所有的关键词
        for index in self.content:
            for i in range(0, len(index)):
                if i != 0:  # 不添加 索引ID
                    words.add(index[i])
        wordsList = list(words)  # set()集合不支持索引，需要转换成list
        # print(wordsList)  # 打印关键词
        for word in wordsList:
            self.indexDic[word] = []  # 字典的值为列表
            for index in self.content:
                if word in index:  # 如果关键词在列表中
                    self.indexDic[word].append(index[0])  # 对应单词 添加索引号
        # print(indexDic)  # 打印测试

    # 索引表写入文件
    def outputInFile(self, outPath):
        fileOut = open(outPath, 'w', encoding='utf-8')  # 打开文件并写入
        # 获取索引列表 并打印
        keyList, valueList = list(self.indexDic.keys()), list(self.indexDic.values())
        fileOut.write("%-20s" % '关键词' + '\t' + '书号索引\n')  # 左对齐
        for i in range(0, len(keyList)):
            fileOut.write("%-20s" % keyList[i] + '\t')  # 左对齐
            for elem in valueList[i]:
                fileOut.write(elem + ',')
            fileOut.write('\n')

        fileOut.close()


# 测试 1
def test1():
    filePath = 'Data/实验2.1 建立词汇索引表_用例.txt'
    outPath = 'Data/indexTable.txt'
    index_Ob = IndexSearch(filePath)  # 建立对象
    indexDic = index_Ob.indexDic  # 直接获取索引字典
    index_Ob.outputInFile(outPath)  # 写入文件

    # 获取索引列表 并打印
    keyList, valueList = list(indexDic.keys()), list(indexDic.values())
    for i in range(0, len(keyList)):
        print(Color.green + "%-15s" % keyList[i], end='\t')  # 左对齐
        for elem in valueList[i]:
            print(Color.carmine + elem, end=',')
        print()


# 索引查找技术 - 实验任务 2 文本建立单词索引表
class WordsIndex:
    # 构造函数
    def __init__(self, filePath):
        self.content = None  # 词表 二维
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

    # 建立词表 私有方法
    def _establishIndexTable(self):
        # 建立词表
        fileOS = open(self.filePath, 'r', encoding='utf-8')  # 打开文件
        try:
            self.content = fileOS.readlines()  # 行列表
            i = 0  # 变量
            while i < len(self.content):
                self.content[i] = self._splitBlank(self.content[i])
                i += 1
            # # 打印测试
            # for line in self.content:  # 打印每行
            #     print(line)
        except Exception as e:
            print(e.args)  # 打印异常
        finally:
            fileOS.close()  # 关闭文件

    # 根据词表建立索引表
    def makeIndexTable(self):
        self._establishIndexTable()
        words = set()  # 记录所有的关键词
        for line in self.content:
            for index in line:
                if self._remove_char(index):
                    words.add(index[: len(index) - 1])  # 去符号
                else:
                    words.add(index)
        wordsList = list(words)  # set()集合不支持索引，需要转换成list
        # print(wordsList)  # 打印关键词

        for word in wordsList:
            self.indexDic[word] = []  # 每个单词都有有个索引列表
            count = 0  # 索引数值变量
            for line in self.content:
                for index in line:
                    temp = index  # 赋值
                    if self._remove_char(index):  # 先去符号
                        temp = index[: len(index) - 1]
                    if word == temp:  # 再比较是否相等
                        self.indexDic[word].append(count)
                    count += len(index)  # 偏移含符号的索引值
                    count += 1  # 加上默认的空格 ！！！
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


# 测试 2
def test2():
    filePath = 'Data/实验2.2_单文档查找用例.txt'
    outPath = 'Data/sanguoIndex.txt'  # 既是输出文件路径 又是导入文件路径

    index_Ob = WordsIndex(filePath)  # 建立对象
    indexDic = index_Ob.indexDic  # 直接获取索引字典
    index_Ob.outputInFile(outPath)  # 写入文件

    # indexDic = WordsIndex.inputFromFile(outPath)  # 导入文件 获取索引字典

    # 获取索引列表 并打印
    keyList, valueList = list(indexDic.keys()), list(indexDic.values())
    for i in range(0, len(keyList)):
        print(Color.green + "%-15s" % keyList[i], end='\t')  # 左对齐
        for elem in valueList[i]:
            print(Color.carmine + "", elem, end=',')
        print()


# 运行
if __name__ == "__main__":
    # test1()  # 测试 1
    test2()  # 测试 2

# ---------------- RESOURCE BEGIN ------------------------------------------------------------------

## filter and lambda
# list_num = [1, 2, 3, 0, 8, 0, 3]
# print(list(filter(lambda x: x != 2, list_num)))


# ---------------- RESOURCE END ------------------------------------------------------------------
