---
layout: 传输层安全协定
title: SSL/TLS
date: 2018-09-02 23:34:49
categories: 基础知识
tags: 协议
---

> **传输层安全性协定 TLS**（Transport Layer Security），及其前身**安全套接层 SSL**（Secure Sockets Layer）是一种 安全协议，目的是为网际网路通信，提供安全及数据完整性保障。

网景在1994年推出首版网页浏览器时，推出[HTTPS](https://www.wikiwand.com/zh-hans/HTTPS "HTTPS")协定，以SSL进行加密，这是SSL的起源。[IETF](https://www.wikiwand.com/zh-hans/IETF "IETF")将SSL进行标准化，1999年公布第一版TLS标准文件。随后又公布 [RFC 5246](https://tools.ietf.org/html/rfc5246)（2008年8月）与 [RFC 6176](https://tools.ietf.org/html/rfc6176)（2011年3月）。

### SSL

安全套接字层利用数据加密技术，可确保数据在网络上之传输过程中不会被截取。当前版本为3.0。它已被广泛地用于Web浏览器与服务器之间的身份认证和加密数据传输。
SSL协议位于TCP/IP协议与各种应用层协议之间，为数据通讯提供安全支持。它建立在可靠的传输协议（如TCP）之上，为高层协议提供数据封装、压缩、加密等基本功能的支持。

### TLS
传输层安全协议，用于两个应用程序之间提供保密性和数据完整性。
TLS 1.0是IETF（Internet Engineering Task Force，Internet工程任务组）制定的一种新的协议，它建立在SSL 3.0协议规范之上，是SSL 3.0的后续版本。

该协议由两层组成： TLS 记录协议（TLS Record）和 TLS 握手协议（TLS Handshake）。较低的层为 TLS 记录协议，位于某个可靠的传输协议（例如 TCP）上面。

* TLS记录协议（TLS Record），对数据进行压缩、加密等；
* TLS握手协议（TLS Handshake），在实际传输数据之前进行身份认证、协商加密算法和交换密钥；

TLS 有两种握手类型：一种是 [RSA](https://www.wikiwand.com/zh-hans/RSA加密演算法)，一种是 [Diffie-Hellman](https://www.wikiwand.com/zh-hans/迪菲-赫爾曼密鑰交換)。下文先对 RSA握手过程 作说明，DH 是类似的。


# 握手简明过程

``` python
      Client                                               Server

      ClientHello                  -------->
                                                      ServerHello
                                                     Certificate*
                                               ServerKeyExchange*
                                              CertificateRequest*
                                   <--------      ServerHelloDone
      Certificate*
      ClientKeyExchange
      CertificateVerify*
      [ChangeCipherSpec]
      Finished                     -------->
                                               [ChangeCipherSpec]
                                   <--------             Finished
      Application Data             <------->     Application Data

             Figure 1.  Message flow for a full handshake

   * Indicates optional or situation-dependent messages that are not
   always sent.
```

![image](http://upload-images.jianshu.io/upload_images/1633382-7b88c9aff019d41c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](http://upload-images.jianshu.io/upload_images/1633382-59aaac879b3a8f2e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. 客户端发送 ClientHello（包含支持的协议版本、加密算法和 **随机数A (Client random)**）到服务端
2. 服务端返回 ServerHello、公钥、证书、**随机数B (Server random)** 到客户端
3. 客户端使用CA证书验证返回证书无误后。生成 **随机数C (Premaster secret)**，用公钥对其加密，发送到服务端
4. 服务端用 **私钥** 解密得到 **随机数C (Premaster secret)**，随后根据得到的 **随机数ABC生成对称密钥** 对需要发送的数据进行对称加密
5. 客户端使用对称密钥（客户端也用随机数ABC生成对称密钥）对数据进行解密。
6. 双方手持对称密钥使用对称加密算法通讯

# session ID的复用

client在向server发送ClientHello消息的时候，会传送Session ID给server端，server端收到session Id后会去session缓存中查找是否有相同值。如果找到相同值，则server直接发送一个具有相同session ID的ServerHello消息给client端（此时不必新建Session ID），然后双方各发一次ChangeCipherSpec消息后直接进入Finished消息互发阶段，具体如下图所示：
```
      Client                                                Server

      ClientHello                   -------->
                                                       ServerHello
                                                [ChangeCipherSpec]
                                    <--------             Finished
      [ChangeCipherSpec]
      Finished                      -------->
      Application Data              <------->     Application Data

          Figure 2.  Message flow for an abbreviated handshake

```
client和server通过缓存Session ID可以快速建立TLS握手，但是这么做也有一些弊端，例如：1）负载均衡中，多机之间往往没有同步 Session 信息，如果客户端两次请求没有落在同一台机器上就无法找到匹配的信息；2）服务端存储 Session ID 对应的信息不好控制失效时间，太短起不到作用，太长又占用服务端大量资源。而 Session Ticket（会话记录单）可以解决这些问题，Session Ticket 是用只有服务端知道的安全密钥加密过的会话信息，最终保存在浏览器端。浏览器如果在 ClientHello 时带上了 Session Ticket，只要服务器能成功解密就可以完成快速握手。

----
# DH算法的握手过程

TLS 整个握手阶段是明文。因此，如果有人窃听了握手过程的通信。他就可以知道双方选择的加密方法，以及三个随机数中的两个。那么整个通话的安全，就只能 **取决于** 第三个随机数（Premaster secret）能不能被破解。

虽然理论上，只要服务器的公钥足够长（比如2048位），那么Premaster secret 就可以保证不被破解。
但为了足够安全，我们可以考虑把握手阶段的算法从默认的 [RSA 算法](https://www.wikiwand.com/zh-hans/RSA加密演算法)，改为 [Diffie-Hellman 算法](https://www.wikiwand.com/zh-hans/迪菲-赫爾曼密鑰交換)（简称DH算法）。

采用DH算法后，握手过程不再传递 Premaster secret，双方只要交换各自的参数，就可以算出这个随机数。

 [![image](http://upload-images.jianshu.io/upload_images/1633382-5327d695ec40fce2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)](http://www.ruanyifeng.com/blogimg/asset/2014/bg2014092007.png) 

上图中，第三步和第四步由传递Premaster secret变成了传递DH算法所需的参数，然后双方各自算出Premaster secret。这样就提高了安全性。

![image](http://upload-images.jianshu.io/upload_images/1633382-9f2351c97d50871f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# Reference
[https://tools.ietf.org/html/rfc5246](https://tools.ietf.org/html/rfc5246)
[https://www.wikiwand.com/en/Transport_Layer_Security](https://www.wikiwand.com/en/Transport_Layer_Security)
[https://www.wikiwand.com/zh-hans/证书颁发机构](https://www.wikiwand.com/zh-hans/证书颁发机构)
[http://www.ruanyifeng.com/blog/2014/09/illustration-ssl.html](http://www.ruanyifeng.com/blog/2014/09/illustration-ssl.html)
[https://segmentfault.com/a/1190000002554673](https://segmentfault.com/a/1190000002554673)
[https://www.cnblogs.com/snowater/p/7804889.html](https://www.cnblogs.com/snowater/p/7804889.html)
[https://razeen.me/post/ssl-handshake-detail.html](https://razeen.me/post/ssl-handshake-detail.html)