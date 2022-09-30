#
# Window Edited by Pycharm.
# Time : 2022/09/20
# Author : YU.J.P
#

"""
    版本: V1.4
    基本功能:
        1. 爬虫
        2. fresh bot / deep crawl bot
        3. Bitmap
        4. MD5签名算法 / Bloom filter布隆过滤器

    对给定的一个URL，能够将该网页的HTML文本下载到本地文件保存；
    利用正则表达式，将网页中的标题、正文、超链接、图片等元素分别提取出来，并能存放到指定的文件中；图片单独存储；
    根据提取的链接，采用广度优先方式抓取至少1000个网页，并提取上述指定的信息；
    扩展1：利用深度优先方式抓取网页，分析比较广度和深度抓取网页的差异；
    扩展2：利用建立HTML标签树的方法，实现网页中相应信息的提取；

"""
import BitVector as BitVector
import requests
from bs4 import BeautifulSoup
import re


class Crawler:
    def __init__(self):
        pass

    @classmethod
    def get_html(cls, url):
        # user_agent = ''
        resp = requests.get(url)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            return resp.text

    @classmethod
    def parser(cls, url):
        list = []
        html = cls.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        # 支出http开头的子链接
        a = soup.find_all('a', attrs={'href': re.compile('^http')})
        # print(a)
        for i in a:
            list.append(i['href'])
            # print(i.get('href'))
        return list

    # 网页抓取测试函数
    @classmethod
    def test_1(cls):
        # url = 'http://www.sina.com.cn' # 新浪
        url = 'https://www.baidu.com'  # 百度
        url_list = Crawler.parser(url)
        for url in url_list:
            print(url)
        print('一共抓取%d个链接' % len(url_list))


# -------------------------------------------------------------------------------------

class SimpleHash:
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    # 生成hash值
    def hash(self, value):
        result = 0
        for i in range(len(value)):
            # 加权求和
            result += self.seed * result + ord(value[i])
        # 位运算保证最后的值在0到self.cap之间
        return (self.cap - 1) & result


# 布隆过滤器
class BloomFilter:
    def __init__(self, BIT_SIZE=1 << 25):
        self.BIT_SIZE = 1 << 25
        # 哈希种子 素数
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.bitset = BitVector.BitVector(size=self.BIT_SIZE)
        self.hashFunc = []
        # 生成对应大小的哈希表
        for i in range(len(self.seeds)):
            self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))

    # 将元素值加入过滤器中
    def insert(self, value):
        # 计算每一个哈希表
        for f in self.hashFunc:
            loc = f.hash(value)
            print(loc)
            self.bitset[loc] = 1

    # 是否已经在过滤器中
    def is_contain(self, value):
        if value is None:
            return False
        result = True
        # 判断每个哈希值是否都已经出现
        for f in self.hashFunc:
            loc = f.hash(value)
            result &= self.bitset[loc]
        return result


def test_2():
    url = r'https://www.sina.com.cn'
    bf = BloomFilter(1000)
    bf.insert(url)
    print(url, ' 是否包含: ', bf.is_contain(url))
    url2 = r'https://www.souhu.com.cn'
    print(url2, ' 是否包含: ', bf.is_contain(url2))


# -------------------------------------------------------------------------------------

# 运行
if __name__ == '__main__':
    # Crawler.test_1()  # 网页抓取测试函数
    test_2()  # 布隆过滤器
    pass
