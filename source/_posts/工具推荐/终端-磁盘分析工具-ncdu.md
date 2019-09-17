---

title: 终端-磁盘分析工具-ncdu
tags: 未定义
categories: 工具推荐
date: 2019-09-12 10:14:55
---

> Ncdu(NCursesDiskUsage)是一个基于Ncurses库的du命令的界面。它通过大家熟知的du命令,为用户提供一个快速且容易被使用的界面。它可以显示磁盘使用的百分比,且允许你使用ncurses库的方式在目录之间导航。

在工作中，经常会遇到磁盘空间被写满的情况，大部分情况是根分区。这种情况需要尽快处理以免影响系统上其它服务。这时候就需要去定位是哪些文件、目录占用了较大空间，以此判断是哪个服务异常，进而解决问题。在文件系统中找出大文件是一件非常耗时的事情。

**ncdu** 能高效地完成了扫描文件系统各文件、目录占用的工作。

# 安装

我们通过包管理工具可以方便的安装它

- mac - brew install ncdu
- debian系列 - apt install ncdu

# 使用

首先，在目录下 执行 `ncdu` 等待其进行进行文件扫描，

![image-20190912141154896](https://cchao1024.github.io/images/2019-8/image-20190912141154896.png)



扫描完成后，就可以看到当前目录通过文字样式展示的信息了，通过 **方向键** 去进出各级目录，底部有目录的信息说明

- `Total disk usage` 标识了 当前目录占用的硬盘空间
- `Apparent size` 显示文件或目录自身大小，而不是它们占用的磁盘空间大小
- `Items` 文件数量

![image-20190912165727439](https://cchao1024.github.io/images/2019-8/image-20190912165727439.png)



# 其他功能

-  `i` 查看项目详细
-  `d` 删除项目
-  `?` 查看更多使用技巧
-  `e` 开关显示隐藏文件或目录（以 **.** 开头的文件）
-  `g` 百分比或图像显示子目录大小的占比
-  `r` 重新扫描目录
-  `q` 退出

-----

**通过 `i` 查看项目详细**

![image-20190912170651622](https://cchao1024.github.io/images/2019-8/image-20190912170651622.png)

**通过 `d` 删除项目**

![image-20190912170759188](https://cchao1024.github.io/images/2019-8/image-20190912170759188.png)

**通过 `?` 查看更多使用技巧**

![image-2019091217091106](https://cchao1024.github.io/images/2019-8/image-2019091217091106.png)



>  更多的使用技巧，请通过输入 `?` 获取



# Reference

[官网]:<https://dev.yorhel.nl/ncdu>
[参考文章]:https://www.jianshu.com/p/b074dc7f83f8
[同类应用]:du命令



# 更多

> **想了解更多的优秀工具，请关注 微信公众号/微博/简书**



![logo](https://cchao1024.github.io/images/2000/global/wx_qr_code.png)

