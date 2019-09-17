---
title: 证书、CA、证书信任链
date: 2018-08-29 23:31:40
categories: 基础知识
tags: 协议
---

# TLS

> 传输层安全性协定 TLS（Transport Layer Security），及其前身安全套接层 SSL（Secure Sockets Layer）是一种安全协议，目的是为网际网路通信，提供安全及数据完整性保障。

![image](http://upload-images.jianshu.io/upload_images/1633382-7b88c9aff019d41c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如图，**TLS** 在建立连接时是需要 

1. 客户端发送 ClientHello（包含支持的协议版本、加密算法和 **随机数A (Client random)**）到服务端
2. 服务端返回 ServerHello、公钥、证书、**随机数B (Server random)** 到客户端
3. 客户端使用CA证书验证返回证书无误后。生成 **随机数C (Premaster secret)**，用公钥对其加密，发送到服务端
4. 服务端用 **私钥** 解密得到 **随机数C (Premaster secret)**，随后根据已经得到的 **随机数ABC生成对称密钥（hello的时候确定的加密算法）**，并对需要发送的数据进行对称加密发送
5. 客户端使用对称密钥（客户端也用随机数ABC生成对称密钥）对数据进行解密。
6. 双方手持对称密钥 **使用对称加密算法通讯**

而这一流程 **服务端的证书** 是是至关重要的。

# 证书
> 证书用来证明公钥拥有者身份的凭证

首先我们需要知道 证书是怎么来的。

数字证书一般由数字证书认证机构签发，需要
* 申请者通过**非对称加密算法（RSA）** 生成一对**公钥**和**密钥**，然后把需要的申请信息（国家，域名等）连同公钥发送给 **证书认证机构（CA）**
* CA构确认无误后通过**消息摘要算法**（MD5，SHA) 生成整个申请信息的摘要签名M， 然后 把 **签名M和使用的摘要算法** 用 **CA自己的私钥** 进行加密

证书包含了
* 公钥
* 证书拥有者身份信息
* 数字证书认证机构（发行者）信息
* 发行者对这份文件的数字签名及使用的算法
* 有效期

证书的格式和验证方法普遍遵循[X.509](https://www.wikiwand.com/zh-hans/X.509 "X.509") 国际标准。

![image](http://upload-images.jianshu.io/upload_images/1633382-29c7f0241d541884.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 证书认证机构（CA）

> 数字证书认证机构（英语：Certificate Authority，缩写为CA），也称为电子商务认证中心、电子商务认证授权机构，是负责发放和管理数字证书的权威机构，并作为电子商务交易中受信任的第三方，承担公钥体系中公钥的合法性检验的责任。

其实任何个体/组织都可以成为CA（自签证书），但是你发发布的证书客户端是不信任的，也是就前文提及的需要权威。比如 **Symantec、Comodo、Godaddy、Digicert**。

客户端信任这些CA，就会在其本地保持这些CA的 **根证书**（**root certificate**），**根证书是CA自己的证书**，是证书验证链的开头。
根证书没有机构（已经是权威了）再为其做数字签名，所以都是自签证书。

CA会通过 **中介证书（intermediate-certificate）** 替代根证书的去做服务器端的证书签名，确保根证书密钥绝对不可访问。

Godaddy 给出了解释
[What is an intermediate certificate?](https://sg.godaddy.com/help/what-is-an-intermediate-certificate-868)

# 证书信任链

前文提到，在向CA 申请证书时是需要 **CA的私钥** 去对整个证书的签名摘要做非对称加密的，也就是证书是可以通过 **CA的公钥** 去解密得到**证书的签名摘要**的。
当我们再次用 **相同的摘要算法**（证书里面有保存所使用的算法）对整个证书做签名，如果得到的签名和证书上的签名是一致的，说明这个证书是可信任的。

同理，中介证书 也是可以被这样的方式证明其可信任。这样的一整个流程称为 **信任链**（Chain of trust）。

就是我**绝对**相信你（A>B）；你**绝对**相信他（B>C）；等于我**绝对**相信他（A>C）。

以下是整个流程：

![信任链.gif](https://upload-images.jianshu.io/upload_images/1633382-2bb24f6d04b99b77.gif?imageMogr2/auto-orient/strip)

1. 客户端得到服务端返回的证书，通过读取得到 **服务端证书的发布机构（Issuer）**
2. 客户端去操作系统查找这个发布机构的的证书，如果是不是根证书就继续递归下去 **直到拿到根证书**。
3. 用 **根证书的公钥** 去 **解密验证** 上一层证书的**合法性**，再拿上一层证书的公钥去验证更上层证书的合法性；递归回溯。
4. 最后验证服务器端的证书是 **可信任** 的。

# Reference

[https://www.wikiwand.com/zh/根证书](https://www.wikiwand.com/zh/根证书)
[https://www.wikiwand.com/zh-hans/信任鏈](https://www.wikiwand.com/zh-hans/信任鏈)
[https://www.wikiwand.com/zh-hans/证书颁发机构](https://www.wikiwand.com/zh-hans/证书颁发机构)
[http://www.cnblogs.com/JeffreySun/archive/2010/06/24/1627247.html](http://www.cnblogs.com/JeffreySun/archive/2010/06/24/1627247.html)
[http://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html](http://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html)