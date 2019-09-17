---
layout: post
title: 'Python3爬虫 多线程爬取美女图片保存到本地'
subtitle: '多线程爬取美女图片'
date: 2017-01-18
categories: 脚本实现
tags: python3
---

# Wanning
> 我们不是生产者,我们只是搬运工

资源来至于**[qiubaichengren](www.qiubaichengren.com)** ，代码基于**Python 3.5.2**
友情提醒：血气方刚的骚年。
**请**

**谨慎** 阅图 ！！！
**谨慎** 阅图 ！！！
**谨慎** 阅图 ！！！

# code：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib
import urllib.request
import re
import threading
from urllib.error import URLError


class QsSpider:
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.header = {'User-Agent': self.user_agent}
        self.save_dir = './pic'
        # 网址
        self.url = 'http://www.qiubaichengren.com/%s.html'
        # 需要爬取的页面数
        self.page_num = 10

    def start(self):
        for i in range(1, self.page_num):
            # 每个页面创建一个线程去下载
            thread = threading.Thread(target=self.load_html, args=str(i))
            thread.start()

    def load_html(self, page):
        # 获取网站的html页面
        try:
            web_path = self.url % page
            request = urllib.request.Request(web_path, headers=self.header)
            with urllib.request.urlopen(request) as f:
                html_content = f.read().decode('gb2312')
                # print(html_content)
                self.pick_pic(html_content)
        except URLError as e:
            print(e.reason)
        return

    def save_pic(self, img):
        # 保存图片到执行路径的pic目录下，替换不能作为文件名的特殊字符
        save_path = self.save_dir + "/" + img.replace(':', '@').replace('/', '_')
        # 如果目录不存在就创建
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        # 打印路径及执行的线程
        print(save_path + '---%s' % threading.current_thread())
        # 取回图片已路径名作文件名保存到指定目录下
        urllib.request.urlretrieve(img, save_path)
        pass

    def pick_pic(self, html_content):
        # 正则匹配出图片链接
        regex = r'src="(http:.*?\.(?:jpg|png|gif))'
        patten = re.compile(regex)
        pic_path_list = patten.findall(html_content)
        for i in pic_path_list:
            self.save_pic(str(i))

spider = QsSpider()
spider.start()

```
