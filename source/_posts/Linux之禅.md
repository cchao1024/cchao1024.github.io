---
title: Linux之禅
date: 2019-03-06 09:57:47
tags: Linux
---

xargs与管道有什么不同呢



xargs 将标准输入作为参数输入给命令           echo -l|xargs ls     等于  ls -l

管道 将标准输入作为标准输入传给命令     



# du 查看目录大小

du -h --max-depth=2  查看目录大小

du -h -d2 



<https://www.jianshu.com/p/1dcb1e2acff1>



## lsof

lsof(list open files)是一个列出当前系统打开文件的工具。

在linux环境下，任何事物都以文件的形式存在，通过文件不仅仅可以访问常规数据，还可以访问网络连接和硬件。所以如传输控制协议 (TCP) 和用户数据报协议 (UDP) 套接字等，系统在后台都为该应用程序分配了一个文件描述符，无论这个文件的本质如何，该文件描述符为应用程序与基础操作系统之间的交互提供了通用接口。因为应用程序打开文件的描述符列表提供了大量关于这个应用程序本身的信息，因此通过lsof工具能够查看这个列表对系统监测以及排错将是很有帮助的。



# ps

Linux中的ps命令是Process Status的缩写

**ps工具标识进程的5种状态码:** 

D 不可中断 uninterruptible sleep (usually IO) 

R 运行 runnable (on run queue) 

S 中断 sleeping 

T 停止 traced or stopped 

Z 僵死 a defunct (”zombie”) process 