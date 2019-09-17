---
title: Android网络安全配置
date: 2018-09-01 23:33:30
categories: 基础知识
tags: 协议
---

# 基础概念
### HTTP

HTTP协议工作于 **客户端-服务端架构**上。通常，由HTTP客户端发起一个**请求**，建立一个到服务器指定端口（默认是80端口）的**TCP连接**。HTTP服务器则在那个端口**监听客户端的请求**。一旦收到请求，服务器会向客户端**响应**返回一个状态，比如"HTTP/1.1 200 OK"，以及返回的内容，如请求的文件、错误消息、或者其它信息。

### HTTPS

HTTPS 全称 HTTP over TLS，是对工作在一加密连接（TLS 或 SSL）上的常规HTTP协议的称呼。

![image.jpeg](https://upload-images.jianshu.io/upload_images/1633382-32f9bdee2e6bfbd2.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

TLS 是在传输层上层的协议，应用层的下层，作为一个安全层而存在，翻译过来一般叫做传输层安全协议。

![](https://upload-images.jianshu.io/upload_images/1633382-7b88c9aff019d41c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/600/format/webp)

TLS 协议请查看 [还没写](==)

证书及认证过程请查看 [证书、CA、证书信任链](https://www.jianshu.com/p/6bf2f9a37feb)

对 HTTP 而言，安全传输层是透明不可见的，应用层仅仅当做使用普通的 Socket 一样使用 SSLSocket 。

TLS是基于 X.509 认证，他假定所有的数字证书都是由一个层次化的数字证书认证机构发出，即 CA。
TLS 是独立于 HTTP 的，任何应用层的协议都可以基于 TLS 建立安全的传输通道，如 SSH 协议。

# 从抓包说起

我们知道使用使用 **HTTP网络监听工具**（Fiddler，Charles等），都是需要在客户端安装根证书的（这里涉及证书的信任链，请查看  [证书、CA、证书信任链](https://www.jianshu.com/p/6bf2f9a37feb)）

而Android系统对于证书是分为，**系统预装证书** 和 **用户安装证书**。

![image](https://upload-images.jianshu.io/upload_images/1633382-c4d0ce022668c216.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**Android 6.0（API 级别 23）** 及更低版本，应用默认信任 **系统预装证书和用户安装证书**
```
<base-config cleartextTrafficPermitted="true">
    <trust-anchors>
        <certificates src="system" />
        <certificates src="user" />
    </trust-anchors>
</base-config>
```
**Android 7.0（API 级别 24）** 以后则默认仅信任 **系统预装证书**
```
<base-config cleartextTrafficPermitted="true">
    <trust-anchors>
        <certificates src="system" />
    </trust-anchors>
</base-config>
```
**cleartextTrafficPermitted** 标识是否允许明文传输

[https://developer.android.com/training/articles/security-config#CustomTrust](https://developer.android.com/training/articles/security-config#CustomTrust)
所以如果应用没有做特殊的配置，在 7.0 以上设备是无法监听到网络请求的。

# 证书配置

我们可以通过编辑配置文件来修改app的默认网络安全配置

首先，需要 在 **manifest** 处声明配置文件
```
<?xml version="1.0" encoding="utf-8"?>
<manifest ... >
    <application android:networkSecurityConfig="@xml/network_security_config"
                    ... >
        ...
    </application>
</manifest>
```

然后就是编辑配置文件，是个xml文件，数据结构格式如下：
```
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config>
        <trust-anchors>
            <certificates src="..."/>
            ...
        </trust-anchors>
    </base-config>

    <domain-config>
        <domain>android.com</domain>
        ...
        <trust-anchors>
            <certificates src="..."/>
            ...
        </trust-anchors>
        <pin-set>
            <pin digest="...">...</pin>
            ...
        </pin-set>
    </domain-config>
    ...
    <debug-overrides>
        <trust-anchors>
            <certificates src="..."/>
            ...
        </trust-anchors>
    </debug-overrides>
</network-security-config>
```

* **base-config**，默认的配置，不在 domain-config 范围内的所有连接所使用的配置。
  * <trust-anchors> 证书集合，可包裹多个 **<certificates>** 证书
* **domain-config**。满足domain规则所使用的配置，可配置任意多个，domain-config的嵌套表示继承外层的配置规则。
  * <trust-anchors> 证书集合
  * <pin-set> 固定的证书，通过 **expiration** 配置过期时间，可包裹多个 **<pin>** 证书
  * <domain> 域名规则，通过 **includeSubdomains** 配置是否支持子域名
  * <domain-config> 嵌套规则
* **debug-overrides**。android:debuggable = true使用，会将这个节点下的证书添加到其他配置上。
  *  <trust-anchors> 证书集合

以上比较重要的是 **<certificates>** 和 **<pin>** 这里特别提下他们的结构

* <certificates>
  // src 标识证书（如果是raw资源则必须以 DER 或 PEM 格式编码）
  [具体转化请点击查看](https://support.ssl.com/index.php?/Knowledgebase/Article/View/19/0/der-vs-crt-vs-cer-vs-pem-certificates-and-how-to-convert-them)
  // overridePins 标识是否绕过证书固定，默认值为 "false"，除非在 debug-overrides 有特别指定
``` xml
<certificates src=["system" | "user" | "raw resource"]
              overridePins=["true" | "false"] />
```
* <pin>
  证书固定，需要 Base64编码的公钥SHA256摘要 Base64(SHA256(SubjectPublicKeyInfo))
  此处懵逼，详情请查阅 [https://stackoverflow.com/questions/40404963/how-do-i-get-public-key-hash-for-ssl-pinning]
```
<pin digest=["SHA-256"]>base64 encoded digest of X.509
    SubjectPublicKeyInfo (SPKI)</pin>
```

通过命令可以获取到 pin
```
openssl s_client -connect xxx.com:443 -servername xxx.com | openssl x509 -pubkey -noout | openssl rsa -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64
```

举个栗子，我想debug 模式信任所有证书，但release仅信任系统和特定的证书
```
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config>
        <trust-anchors>
            <certificates src="system"/>
            <certificates src="@raw/ca_debug_charles"/>
        </trust-anchors>
    </base-config>
    <debug-overrides>
        <trust-anchors>
            <certificates src="system"/>
            <certificates src="user"/>
        </trust-anchors>
    </debug-overrides>
</network-security-config>

```
具体请查阅官网验证
[https://developer.android.google.cn/training/articles/security-ssl](https://developer.android.google.cn/training/articles/security-ssl)

# 开发者设置

这个时候我就有需求，我想要release的包是不信任用户证书的，但是又需要留个后门给自己调试。

比如：输入框输入特定代码证明我是开发者后，网络框架就取消对证书的验证，这样就可以通过安装用户证书来 **监控调试** release包的https网络请求。

代码使用OkHttp实现，其他网络框架请自行google。

```
 
/**
 * 默认信任所有的证书
 */
@SuppressLint("TrulyRandom")
private static SSLSocketFactory createSSLSocketFactory() {
    SSLSocketFactory sSLSocketFactory = null;
    try {
        SSLContext sc = SSLContext.getInstance("TLS");
        sc.init(null, new TrustManager[]{new TrustAllManager()},
                new SecureRandom());
        sSLSocketFactory = sc.getSocketFactory();
    } catch (Exception e) {
    }
    return sSLSocketFactory;
}

private static class TrustAllManager implements X509TrustManager {
    @Override
    public void checkClientTrusted(X509Certificate[] chain, String authType)
            throws CertificateException {
    }

    @Override
    public void checkServerTrusted(X509Certificate[] chain, String authType)
            throws CertificateException {
    }

    @Override
    public X509Certificate[] getAcceptedIssuers() {
        return new X509Certificate[0];
    }
}

private static class TrustAllHostnameVerifier implements HostnameVerifier {
    @Override
    public boolean verify(String hostname, SSLSession session) {
        return true;
    }
}

  OkHttpClient client = new OkHttpClient.Builder()
          .sslSocketFactory(createSSLSocketFactory())
          .hostnameVerifier(new TrustAllHostnameVerifier())
          .build();
```

# Reference

[https://developer.android.com/training/articles/security-config](https://developer.android.com/training/articles/security-config)
[https://medium.com/@appmattus/android-security-ssl-pinning-1db8acb6621e](https://medium.com/@appmattus/android-security-ssl-pinning-1db8acb6621e)
[https://stackoverflow.com/questions/40404963/how-do-i-get-public-key-hash-for-ssl-pinning](https://stackoverflow.com/questions/40404963/how-do-i-get-public-key-hash-for-ssl-pinning)
[https://www.jianshu.com/p/59a102f150aa](https://www.jianshu.com/p/59a102f150aa)
