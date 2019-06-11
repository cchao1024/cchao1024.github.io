---
title: Next博客主题优化
date: 2019-06-11 10:37:00
tags: 
---

# 阅读更多

首页显示的文章会显示全部的内容，我们通过修改 **auto_excerpt** 配置默认显示的字数，超出就显示 **阅读更多**

在 **主题配置文件（themes/next/_config.yml）**中查找并修改为：

```c
auto_excerpt:
  enable: true
  length: 150
```

# 添加About

1 创建about页

```
hexo new page "about"
```

执行完成会生成 **source/about** 及**index.md** 文件，通过

2 编辑 index.md 文件展示个人信息

3 在 **主题配置文件（themes/next/_config.yml）** 中查找并取消 **menu下的about注释**

```
menu:
  home: / || home
  about: /about/ || user
  #tags: /tags/ || tags
  categories: /categories/ || th
  archives: /archives/ || archive
  #schedule: /schedule/ || calendar
  #sitemap: /sitemap.xml || sitemap
  #commonweal: /404/ || heartbeat
```



# 网易云音乐

1 前往[网易云音乐](<https://music.163.com/>)找到自己希望的背景音乐，点击**生成外链播放器** ![](../images/2019-6/next_1.png)

2 进入预览页，复制内嵌代码

![](../images/2019-6/next_2.jpg)



3 进入目录 **themes/next/layout/_custom**，编辑文件 **sidebar.swig** 放入复制的内嵌代码

```
<!--网易云音乐-->
<div id="music163player">
    <iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&id=36664503&auto=1&height=66"></iframe>
</div>
```



# 添加背景图

去找一张自己喜欢的背景图命名为 background.jpg

1 将背景图放入目录 **/themes/next/source/images** 下

2 进入目录 themes/next/source/css/_custom，编辑文件 **custom.styl**

// Custom styles.
 body {
​    background-image:url(/images/background.jpg);
​    background-repeat: no-repeat;
​    background-attachment:fixed;
​    background-position:50% 50%;
​	background-size: 100% 100%;
​    }



# 添加萌妹

![image-20190611110544118](../images/2019-6/next_3.png)

1 安装module

```
npm install --save hexo-helper-live2d
```

2 在 **主题配置文件（themes/next/_config.yml）**新增

```
live2d:
  enable: true
  scriptFrom: local
  pluginRootPath: live2dw/
  pluginJsPath: lib/
  pluginModelPath: assets/
  tagMode: false
  log: false
  model:
    use: live2d-widget-model-wanko
  display:
    position: right
    width: 150
    height: 300
  mobile:
    show: true
  react:
    opacity: 0.7
```

# Result

![image-20190611110544118](../images/2019-6/next_4.png)

# Referer

[https://github.com/EYHN/hexo-helper-live2d](https://github.com/EYHN/hexo-helper-live2d)

[https://hexo.io/zh-cn/docs/](https://hexo.io/zh-cn/docs/)

[hexo-theme-next](https://github.com/theme-next/hexo-theme-next)