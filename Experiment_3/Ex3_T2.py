#
# Crawler Edited by Pycharm.
# Time : 2022/09/23
# Author : YU.J.P
#

"""
    版本: V1.1
    基本功能:
    对给定的一个URL，能够将该网页的HTML文本下载到本地文件保存；
    利用正则表达式，将网页中的标题、正文、超链接、图片等元素分别提取出来，并能存放到指定的文件中；图片单独存储；
    根据提取的链接，采用广度优先方式抓取至少1000个网页，并提取上述指定的信息；
    扩展1：利用深度优先方式抓取网页，分析比较广度和深度抓取网页的差异；
    扩展2：利用建立HTML标签树的方法，实现网页中相应信息的提取；

"""
import urllib.request
import requests
from bs4 import BeautifulSoup
import re


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


# 利用正则表达式，将网页中的标题、正文、超链接、图片等元素分别提取出来，并能存放到指定的文件中；图片单独存储
class MyCrawler:
    def __init__(self):
        pass

    @classmethod
    def extract_title(cls, content):
        """
        提取网页 标题
        :param content: html文本
        :return: 返回html文本的标题
        """
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find('title')
        return title.text

    @classmethod
    def remove_empty_line(cls, content):
        """
        去除空行
        :param content: 需要处理的文本
        :return: 处理空行、空格好的文本
        """
        r = re.compile(r'''^\s+$''', re.M | re.S)
        content = r.sub('', content)
        r = re.compile(r'''\n+''', re.M | re.S)
        content = r.sub('\n', content)
        return content

    @classmethod
    def remove_js_css(cls, content):
        """
        去除script,style,meta，注释等脚本
        :param content: 需要处理的文本
        :return: 移除script,style,meta，注释等脚本脚本后的文本
        """
        r = re.compile(r'''<script.*?</script>''', re.I | re.M | re.S)
        s = r.sub('', content)
        r = re.compile(r'''<style.*?</style>''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<!--.*?-->''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<meta.*?>''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<ins.*?</ins>''', re.I | re.M | re.S)
        s = r.sub('', s)
        return s

    @classmethod
    def remove_any_tag(cls, content):
        """
        移除js,css脚本
        :param content: 需要处理的文本
        :return: 移除js,css脚本后的文本
        """
        content = re.sub(r'''<[^>]+>''', '', content)
        return content.strip()

    @classmethod
    def getImages(cls, content, path):
        """
        爬取图片
        :param content: 爬取网页内容
        :param path: 本地图片存储位置
        :return: None
        """
        Img = re.compile(r'src="(.+?\.jpg)"')  # 正则表达式匹配图片
        imageList = re.findall(Img, content)  # 结合re正则表达式和BeautifulSoup, 仅返回超链接
        print(imageList)

        if imageList is None:
            print(Color.red + "# ERROR ! No Useful URL...")
        else:
            print(Color.red + "# Begin Download Image DATA...")
            count = 0  # 计数器
            for imageUrl in imageList:
                # 打开网址，下载图片保存到本地
                urllib.request.urlretrieve(imageUrl, '{}{}.jpg'.format(path, count))
                count += 1
            print(Color.red + "# Download Image DATA Successfully...")

    @classmethod
    def extract_a_label(cls, content):
        """
        提取网页子网页,并写入文件
        :param content: 需要处理的文本
        :return: None
        """
        soup = BeautifulSoup(content, 'html.parser')
        alink = soup.find_all('a')
        # return alink
        # 写入文件
        file_ob = open('Data/a.txt', 'w', encoding='utf-8')
        for link in alink:
            a = link.get('href')
            key = link.string
            if key is not None and a is not None:
                file_ob.write(key + ':' + a + '\n')
        file_ob.close()
        print(Color.green + "# ALINK DATA Writing Successfully...")

    @classmethod
    def cuteCrawler(cls, url):
        """
        爬虫程序 - 将网页中的标题、正文、超链接、图片等元素分别提取出来，并能存放到指定的文件中；图片单独存储。
        :param url: 网页网址
        :return: None
        """
        dic = {}  # 字典
        id = 1  # 编号记录
        # 获取网页内容
        page = urllib.request.urlopen(url)
        content = page.read().decode('UTF-8')
        # 获取编号
        dic['id'] = id
        # 获取网址
        dic['url'] = url
        # 获取标题
        dic['title'] = cls.extract_title(content)
        # 获取图片 存储位置 : Image
        cls.getImages(content, 'Image\\')
        # 获取html正文
        html = cls.remove_empty_line(cls.remove_js_css(content))
        html = cls.remove_any_tag(html)
        html = cls.remove_empty_line(html)
        dic['html'] = html  # 加入字典
        print(Color.carmine, dic['html'])
        # 写入文件
        file_ob = open('Data/' + str(id) + '.txt', 'w', encoding='utf-8')
        # file_ob.write(json.dumps(dic, ensure_ascii=False))
        file_ob.write(str(dic))
        file_ob.close()
        print(Color.green + "# JSON DATA Writing Successfully...")
        # 获取子网页
        cls.extract_a_label(content)


# 运行
if __name__ == '__main__':
    # url = 'https://www.bilibili.com/'
    # url = 'http://www.sina.com.cn'  # 新浪
    # url = 'https://cn.bing.com/images/search?q=%E6%83%85%E7%BB%AA%E5%9B%BE%E7%89%87&qpvt=%e6%83%85%e7%bb%aa%e5%9b%be%e7%89%87&form=IGRE&first=1&cw=418&ch=652&tsc=ImageBasicHover'
    # url = 'https://www.csdn.net/?spm=1001.2101.3001.4476'
    # url = 'https://v.qq.com/'
    # url = 'https://www.cqut.edu.cn/'
    url = 'https://www.keaitupian.cn/meinv/'
    MyCrawler.cuteCrawler(url)
    pass


# --------------------------------------------------------------------------------------
# 可参考技术文档草稿：


# 我的宠物
class Crawler:
    def __init__(self):
        pass

    @classmethod
    def get_html(cls, url):
        # user_agent = ''
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        return resp.text

    # 提取网页 标题
    @classmethod
    def extract_title(cls, content):
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find('title')
        return title.text

    # 去除空行
    @classmethod
    def remove_empty_line(cls, content):
        """remove multi space """
        r = re.compile(r'''^\s+$''', re.M | re.S)
        s = r.sub('', content)
        r = re.compile(r'''\n+''', re.M | re.S)
        s = r.sub('\n', s)
        return s

    # 去除script,style,meta，注释等脚本
    @classmethod
    def remove_js_css(cls, content):
        """
            remove the the javascript and the stylesheet and the comment content
            (<script>....</script> and <style>....</style> <!-- xxx -->)
        """
        r = re.compile(r'''<script.*?</script>''', re.I | re.M | re.S)
        s = r.sub('', content)
        r = re.compile(r'''<style.*?</style>''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<!--.*?-->''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<meta.*?>''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<ins.*?</ins>''', re.I | re.M | re.S)
        s = r.sub('', s)
        return s

    # 移除js,css脚本
    @classmethod
    def remove_any_tag(cls, s):
        s = re.sub(r'''<[^>]+>''', '', s)
        return s.strip()

    @classmethod
    def remove_any_tag_but_a(cls, s):
        text = re.findall(r'''<a[^r][^>]*>(.*?)</a>''', s, re.I | re.S | re.S)
        text_b = cls.remove_any_tag(s)
        return len(''.join(text)), len(text_b)

    @classmethod
    def remove_image(cls, s, n=50):
        image = 'a' * n
        r = re.compile(r'''<img.*?>''', re.I | re.M | re.S)
        s = r.sub(image, s)
        return s

    @classmethod
    def remove_video(cls, s, n=1000):
        video = 'a' * n
        r = re.compile(r'''<embed.*?>''', re.I | re.M | re.S)
        s = r.sub(video, s)
        return s

    # 提取网页的正文
    @classmethod
    def extract_text(cls, content):
        s = cls.remove_empty_line(cls.remove_js_css(content))
        s = cls.remove_any_tag(s)
        s = cls.remove_empty_line(s)
        return s

    # 提取网页子网页
    @classmethod
    def extract_a_lable(cls, content):
        soup = BeautifulSoup(content, 'html.parser')
        alink = soup.find_all('a')
        # return alink
        # 写入文件
        file_ob = open('Data/a.txt', 'w', encoding='utf-8')
        for link in alink:
            a = link.get('href')
            key = link.string
            if key is not None and a is not None:
                file_ob.write(key + ':' + a + '\n')
        file_ob.close()
        print(Color.green + "# ALINK DATA Writing Successfully...")

    # 提取网页图片
    @classmethod
    def getHtml(cls, url):
        page = urllib.request.urlopen(url)
        html = page.read()
        return html.decode('UTF-8')

    @classmethod
    def getImages(cls, url):
        content = cls.getHtml(url)
        Img = re.compile(r'src="(.+?\.jpg)"')  # 正则表达式匹配图片
        imageList = re.findall(Img, content)  # 结合re正则表达式和BeautifulSoup, 仅返回超链接
        print(imageList)

        count = 0  # 计数器
        path = 'Image\\'
        for imageUrl in imageList:
            # 打开网址，下载图片保存到本地
            urllib.request.urlretrieve(imageUrl, '{}{}.jpg'.format(path, count))
            count += 1
        print(Color.green + "# Image DATA Download Successfully...")

    # 提取网址
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

    # 网页抓取测试函数 1
    @classmethod
    def test_1(cls):
        # url = 'http://www.sina.com.cn' # 新浪
        url = 'https://www.baidu.com'  # 百度
        url_list = Crawler.parser(url)
        for url in url_list:
            print(url)
        print('一共抓取%d个链接' % len(url_list))

    # 测试函数 2
    @classmethod
    def test_2(cls):
        # url = 'http://www.sina.com.cn'  # 新浪
        # url = 'https://www.baidu.com'  # 百度
        # url = 'https://www.bilibili.com/'
        # url = 'https://www.cqut.edu.cn/'
        url = 'https://www.keaitupian.cn/meinv/'

        # 图片提取
        # url = 'https://www.bilibili.com/'
        # url = 'http://www.sina.com.cn'  # 新浪
        # url = 'https://cn.bing.com/images/search?q=%E6%83%85%E7%BB%AA%E5%9B%BE%E7%89%87&qpvt=%e6%83%85%e7%bb%aa%e5%9b%be%e7%89%87&form=IGRE&first=1&cw=418&ch=652&tsc=ImageBasicHover'
        # url = 'https://www.csdn.net/?spm=1001.2101.3001.4476'
        # url = 'https://v.qq.com/'
        # url = 'https://www.cqut.edu.cn/'

        url = 'https://www.keaitupian.cn/meinv/'
        Crawler.getImages(url)
