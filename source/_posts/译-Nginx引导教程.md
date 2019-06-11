---
title: '[译] Nginx引导教程'
date: 2019-02-11 11:49:57
tags:
---

> 本文为译文，原文来至 [http://nginx.org/en/docs/beginners_guide.html](http://nginx.org/en/docs/beginners_guide.html)

# Guide
本教程基础的介绍了nginx，以及能使用nginx完成的简单任务。
本教程建立在读者已经安装了nginx，如果并没有，请移步[Installing nginx](http://nginx.org/en/docs/install.html)。
本教程将包括以下内容：
  * nginx的开启和关闭
  * nginx重启配置
  * 配置文件结构说明
  * 配置nginx提供静态服务
  * 配置nginx作为代理服务器
  * 连接nginx与FastCGI应用

nginx拥有一个主进程和多个工作进程，主进程的主要任务是管理配置信息和调度工作进程。工作进程做真实的请求处理。
nginx基于事件的模型和操作系统平台依托的机制在工作进程间有效地分发请求。
工作进程的数量是配置文件定义的，可以通过配置文件固定，也可以根据cpu核心数自适应（[worker_processes](http://nginx.org/en/docs/ngx_core_module.html#worker_processes))。
nginx的工作方式和模块情况取决于它的配置文件 **nginx.conf** ，而它的配置文件一般在
- /usr/local/nginx/conf 或者
- /etc/nginx 或者
- /usr/local/etc/nginx

# 启动，关闭，刷新配置
运行可执行文件启动nginx,nginx启动后可以通过 -s 参数去 控制它
```
nginx -s SIGNAL
```
SIGNAL 可以是如下值
* stop —— 快速停止
* quit —— 优雅停止
* reload —— 刷新配置文件
* reopen —— 重新打开log文件

比如：你希望 等工作进程完成当前正在处理的请求后就停止 nginx 进程，可以使用
```
nginx -s quit
```
> 注意，执行这个命令的用户要和启动nginx的用户是同一个。

如果你修改了配置文件，那么你需要执行reload命令或者重启nginx才能生效
```
nginx -s reload
```
主进程在收到reload命令时，会去检查配置文件的语法并且尝试去应用配置的内容。
如果成功，主进程就会启动一个新的工作进程去发送信息命令其他工作进程关闭；否则主进程将会回滚，并应用回上一次的配置信息，工作进程继续工作着。
工作进程收到关闭的命令后将不再接受新的客户端请求，继续完成手头上的请求后关闭。

在类Unix系统平台上也可以通过类似kill的命令向nginx发送消息，这样的消息一般是直接发送给用进程ID标识的nginx进程。
nginx的主进程ID默认是写在 **/usr/local/nginx/logs** 或者 **/var/run** 目录下的 nginx.pid。
比如当前nginx主进程的进程ID是1628，可以这样
```
# 优雅的关闭nginx
* kill -s quit 1628 
# 通过 ps 可以获取到 nginx 进程号
* ps -ax | grep nginx
```
更多的信息，请求查看[Controlling nginx](http://nginx.org/en/docs/control.html)

# 配置文件

nginx由模块组成，这些模块由配置文件中指定的指令控制。
指令分为**简单指令**和**指令块**。

简单指令是由以分号结尾，空格分隔的键值对组成[　key value; ]
指令块和简单指令结构相同，但是使用一对大括号（ {} ）去包裹一组指令。
包含其他指令的指令块称为**上下文** （比如events，http, server和location）

在配置文件中，块级指令之外的区域称之为主(根)上下文（main context)。
比如：
events 和 http 指令是处在主上下文里的，
server指令是处在http上下文里中，
location指令又是处在server上下文里中。

```
主（根）上下文
http{
    server{
       location {
       }
    }
}
```
同一行内 #字符后的都是注释

# 静态资源服务
Web服务器的一项重要功能就是能充当静态服务器（如：图片，静态HTML文本)。
比如你要实现这样的情景：
【根据不同的请求，nginx会返回指定的文件资源】
**/data/images** 目录下的图片
**/data/www/** 目录下的html文件。
只需要配置nginx文件，在http配置块的server下写两个location块。
首先创建 /data/www 目录，在这个目录下建立index.html文件，里面随便写点什么内容
​    创建 /data/images 目录，里面放一些图片。
然后打开配置文件(文件中默认是配置有几个server块的，但大部分是被注释掉的)，把那些server都注释掉，在http块下重新配置一个server块。
```
http{
    server{
    }
}
```
一般来说，配置文件会根据监听端口号或者主机名分为几个server块，而nginx到底把http请求交给哪个server处理，则是根据请求的URI和server里location指令的值的匹配来处理的。
下面我们添加一个location 到 server 中

```
location / {
    root /data/www;
}
```

上述location的"/"前缀，是用来匹配http请求URI的。而它会添加到root指定的路径下，也就是/data/www,以此来形成请求资源（文件）和本地文件系统的对应。如果有多个location和URI匹配的话，那就优先选择最长匹配的location。我们写的location只提供了最短的前缀，长度为1。所以，只有其他location匹配失败的情况下才能使用这个location。现在，我们再添加一个location

```
location /images/ {
    root /data;
    }

```
上述的location将会匹配一个以/images开始的http请求（location / 也会被匹配但是它更短)。
配置好后，应该是类似下面的内容
```
http{
    server{
        location / {
            root /data/www;
            }
        location /images/ {
            root /data;
            }
    }
}
```
这样就配置了监听标准80端口的server，可以通过http://localhost验证。
当请求URI以 /image/ 开头，服务器将响应 /data/images/ 目录下的文件
-- 例如：访问http://localhost/images/example.png，Web服务器会响应 /data/images/example.png
如果该文件不存在，则返回 404 error.如果URI不是以/images/开头，那就映射到/data/www目录，
-- 例如：访问http://localhost/some/example.html，Web服务器将会把/data/www/some/example.html响应给客户端。
修改nginx配置文件之后，记得让主进程重新读取配置文件才能生效
```
nginx -s reload
```
> 如果出错的话，记得查看access.log和error.log日志文件的内容。
> 日志目录一般在/usr/local/nginx/log/或者/var/log/nginx/里。

# 配置简单代理服务器

nginx的一个常见用途是作为代理服务器，代理服务器是接受请求，转发请求的到被代理的服务器，再从被代理的服务器获取响应回传给客户端。
在下面这个例子中，我们会配置一个简单的代理服务器，直接返回静态文件，其他的则转发给被代理的服务器。
首先，编写个server块

```
server {
    listen 8080;
    root /data/up1;

    location / {
    }
}

```
这样就能提供一个简单监听8080端口的server(这里需要写listen是因为之前默认的80端口已经被占用了)，这个server映射所有请求到本地 /data/up1 目录。创建一个 index.html文件到这个目录下。
注意，当location下未指定root目录时将会使用 server的root目录（类似默认值）
然后，修改配置文件 在先前server的第一个location处放入 proxy_pass，指定 协议，域名，端口，如：

```
server {
    location / {
        proxy_pass http://localhost:8080;
    }

    location /images/ {
        root /data;
    }
}
```
修改第二个 localtion（映射 /images/开头到本地目录）成根据文件类型拓展名匹配
```
location ~ \.(gif|jpg|png)$ {
    root /data/images;
}
```
该参数是一个正则表达式，匹配以.gif，.jpg或.png结尾的所有URI。 正则表达式应该以〜开头。相应的请求将映射到
/data/images目录。

nginx在分发请求给location时，会先选出最长的匹配前缀的location，然后去检查正则表达式，如果正则表达式匹配就选择正则表达式所在的location，否则就使用之前选出最长匹配location

更多的指令请移步 [more](http://nginx.org/en/docs/http/ngx_http_proxy_module.html)

# Reference 

[http://nginx.org/en/docs/beginners_guide.html](http://nginx.org/en/docs/beginners_guide.html)
[https://juejin.im/post/5a050d7f51882578d84eeaf8](https://juejin.im/post/5a050d7f51882578d84eeaf8)