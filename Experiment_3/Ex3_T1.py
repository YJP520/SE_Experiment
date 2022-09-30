#
# Crawler Edited by Pycharm.
# Time : 2022/09/23
# Author : YU.J.P
#

"""
    版本: V1.4
    基本功能:
    对给定的一个URL，能够将该网页的HTML文本下载到本地文件保存；
    利用正则表达式，将网页中的标题、正文、超链接、图片等元素分别提取出来，并能存放到指定的文件中；图片单独存储；
    根据提取的链接，采用广度优先方式抓取至少1000个网页，并提取上述指定的信息；
    扩展1：利用深度优先方式抓取网页，分析比较广度和深度抓取网页的差异；
    扩展2：利用建立HTML标签树的方法，实现网页中相应信息的提取；

"""

from urllib.request import urlopen  # 打开网址

# 对给定的一个URL，能够将该网页的HTML文本下载到本地文件保存；
def test_01():
    url = "http://www.baidu.com"
    resp = urlopen(url)
    content = resp.read().decode("UTF-8")
    # print(content)  # 解码

    with open('Data/mybaidu.html', mode='w', encoding='utf-8') as f:
        f.write(content)
        print("# 数据写入完成...")

# 运行
if __name__ == '__main__':
    test_01()
    pass