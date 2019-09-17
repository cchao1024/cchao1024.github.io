---
layout: post
title: 'okHttp 请求与响应'
subtitle: 'okhttp源码'
date: 2017-09-12
categories: 框架技术
tags: okhttp
---


[TOC]

# Sample

下面的是官方Get请求的sample，代码先**创建 OkHttpClient 实例**（建议全局只维持一个实例，避免多个连接池和线程池的浪费），然后在子线程通过建造器创建出 **Request** ，之后通过 **Call接口** 的工场方法 **newCall** 创建出一个RealCall对象，使用 **execute** 方法执行同步请求，完成后返回 **Response** 对象，最后return出响应的 body 内容。

```
OkHttpClient client = new OkHttpClient();

String run(String url) throws IOException {
  Request request = new Request.Builder()
      .url(url)
      .build();

  Response response = client.newCall(request).execute();
  return response.body().string();
}

```

# [Requests](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Request.html)

`Request` 是一个**不可变类**，它就是我们每天都接触的**Http请求**，通过它的Builder可以设置我们Http请求的目标`Url`、`head`、`body`以及`method（GET、POST...）`，还有它提供了一个**Object类型tag**属性，我们可以拿它标识不同的Request，比如**通过页面唯一tag标识请求**，如果用户主动关闭页面，我们可以`cancel`掉相应的`Request`。

### 缺省填充

我们再建造Request对象时，省略了许多正常Http请求需要的字段，但是OkHttp会默认给我添加这些字段，比如：：`Content-Length`, `Transfer-Encoding`, `User-Agent`, `Host`, `Connection`, `Content-Type`，`Accept-Encoding`以及`cookie`等。

### 重定向及重试

如果请求的URL返回了302重定向，Request会重新指向重定向地址，拿到最终的Respond。有时连接会失败（池连接失效、断开连接），或者无法连接到对应web服务器。OkHttp将以不同的方式重新尝试请求。

### 方法及实现

- `url:HttpUrl`[^HttpUrl] --- 可以理解为请求的URL，但它不止于此
- `header:Headers` --- 有序的首部字段，由一个不可变的字符串数组保存，okHttp会自动添加一些通用字段)
- `cacheControl:CacheControl` --- 对应着Http的通用首部字段 Cache-Control[^Cache-Control]
- `body:RequestBoy` --- 请求体，RequestBoy[^RequestBody]是一个抽象类，有以下子类分别对应不同的**Content-Type**字段

    - HttpEntityBody --- 二进制流 对应 Content-Type：application/octet-stream
    - FormBody --- 键值对表单 对应 Content-Type：application/x-www-form-urlencoded
    - MultipartBody 多部分的body 对应 Content-Type：multipart/... 需要boundary分割多个部分
    - ....

下图是Request.Builder的结构图

![Request](http://upload-images.jianshu.io/upload_images/1633382-1cf36dac6536235c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# [Responses](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Response.html)

`Respond` 也是个final类，它的内容就比Request丰富多了，首先它是持有对应的`Request`对象的，再者它还有`Handshake`（TLS握手，也就是HTTPS请求需要的TLS/SSL层支持）对象，还有就是我们熟悉的响应行，响应首部，ResponseBody等。同样的，Respond也提供了缺省填充，如：

### 方法及实现

- protocol:Protocol --- 枚举http版本 Http1.0、Http1.1、Http2.0（h2）以及spdy/3.1（弃用）
- body:ResponseBody --- 响应body，抽象类，对应着一下具体实现RealResponseBody（普通impl）、ProgressResponseBody（能更新进度）、CacheResponseBody（读取缓存）
-

![Respond_Builder.png](http://upload-images.jianshu.io/upload_images/1633382-6285751ff48a0a86.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



# Call

Call 是一个接口，它的实现类是RealCall。Call是一次Request和Respond对，它不能被执行两次，但是可以取消请求（cancel方法）

![Call](http://upload-images.jianshu.io/upload_images/1633382-e3b35f6c299afa72.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

方法execute和enqueue分别是同步和异步请求。

### execute

excute方法将Call放进okHttpClient的`Dispatcher`(分发器)的`队列runningSyncCalls`（下文有说明）。并且加入一堆`Interceptor(拦截器)`：

- 用户定义的拦截器（通过`OkHttpClient#addInterceptor(Interceptor)`)加入的拦截器）
- `RetryAndFollowUpInterceptor`
- `BridgeInterceptor`
- `CacheInterceptor`
- `ConnectInterceptor`
- `CallServerInterceptor` 最后一个拦截器，对服务器发起网络请求

然后执行getResponseWithInterceptorChain进入了一堆痛苦的拦截，在逐层向下后在某一层得到需要的Response，检测无疑就return了，有问题就捕获并finish掉这个Call

```
@Override public Response execute() throws IOException {
    synchronized (this) {
      if (executed) throw new IllegalStateException("Already Executed");
      executed = true;
    }
    captureCallStackTrace();
    eventListener.fetchStart(this);
    try {
      client.dispatcher().executed(this);
      Response result = getResponseWithInterceptorChain();
      if (result == null) throw new IOException("Canceled");
      eventListener.fetchEnd(this, null);
      return result;
    } catch (IOException e) {
      eventListener.fetchEnd(this, e);
      throw e;
    } finally {
      client.dispatcher().finished(this);
    }
  }
Response getResponseWithInterceptorChain() throws IOException {
    // Build a full stack of interceptors.
    List<Interceptor> interceptors = new ArrayList<>();
    interceptors.addAll(client.interceptors());
    interceptors.add(retryAndFollowUpInterceptor);
    interceptors.add(new BridgeInterceptor(client.cookieJar()));
    interceptors.add(new CacheInterceptor(client.internalCache()));
    interceptors.add(new ConnectInterceptor(client));
    if (!forWebSocket) {
      interceptors.addAll(client.networkInterceptors());
    }
    interceptors.add(new CallServerInterceptor(forWebSocket));

    Interceptor.Chain chain = new RealInterceptorChain(interceptors, null, null, null, 0,
        originalRequest, this, eventListener, client.connectTimeoutMillis(),
        client.readTimeoutMillis(), client.writeTimeoutMillis());
    return chain.proceed(originalRequest);
  }

```

RealInterceptorChain ＋ Interceptor实现了职责链模式(Chain of Responsibility)，对请求/响应进行串式（流式）处理。

1. 将这堆拦截器、request、call等封装成`RealInterceptorChain`(拦截链Chain对象)
2. 迭代（index）取出一个拦截器，拦截器在实现`intercept(Chain)方法`时如果自己不能处理和返回Response（比如CacheInterceptor没有缓存），就会`Return Chain#Proceed(Request)`交给拦截链继续传递获取到Response。
3. RealInterceptorChain的proceed方法内部将自己（RealInterceptorChain）持有的成员变量通过构造器再new出来一个新的`RealInterceptorChain(interceptors, request, index +=1 ...)`对象
4. 如果执行到最后一个拦截器`CallServerInterceptor`,就对服务器发起网络请求，等待数据返回并`Return Response`。否则就继续第二步。

代码有删减

```
  /** Constructor*/
  public RealInterceptorChain(List<Interceptor> interceptors,  StreamAllocation streamAllocation,
      HttpCodec httpCodec, RealConnection connection, int index, Request request, Call call,
      EventListener eventListener, int connectTimeout, int readTimeout, int writeTimeout) {
    this.interceptors = interceptors;
    this.connection = connection;
    this.streamAllocation = streamAllocation;
    this.httpCodec = httpCodec;
    this.index = index;
    this.request = request;
    this.call = call;
    this.eventListener = eventListener;
    this.connectTimeout = connectTimeout;
    this.readTimeout = readTimeout;
    this.writeTimeout = writeTimeout;
  }
  @Override
  public Response proceed(Request request) throws IOException {
    return proceed(request, streamAllocation, httpCodec, connection);
  }

  public Response proceed(Request request, StreamAllocation streamAllocation, HttpCodec httpCodec,
      RealConnection connection) throws IOException {

    // Call the next interceptor in the chain.
    RealInterceptorChain next = new RealInterceptorChain(interceptors, streamAllocation, httpCodec,
        connection, index + 1, request, call, eventListener, connectTimeout, readTimeout,
        writeTimeout);
    Interceptor interceptor = interceptors.get(index);
    Response response = interceptor.intercept(next);

    // Confirm that the next interceptor made its required call to chain.proceed().
    if (httpCodec != null && index + 1 < interceptors.size() && next.calls != 1) {
      throw new IllegalStateException("network interceptor " + interceptor
          + " must call proceed() exactly once");
    }

    if (response.body() == null) {
      throw new IllegalStateException(
          "interceptor " + interceptor + " returned a response with no body");
    }

    return response;
  }

```

### enqueue

enqueue是Call的异步实现，需要传入一个`Callback`回调方法，其内部是将callback封装成`AsyncCall`对象

AsyncCall继承于`NamedRunnable`，NamedRunnable是个实现Runnable接口的，能对执行线程的命名的抽象类，是装饰模式对Runnable接口添加Name功能。其实现是，（AsyncCall构造方法通过super把name赋值给成员变量name）当线程在线程队列排队完成开始执行`run`方法时调起`Thread#setName（name）`为自己命名并执行抽象方法`execute`。

在AsyncCall的execute方法里（这个方法被调起就意味着这个等待线程在被执行），我们可以看到，其实enqueue在排队完成后做的事情和excute是类似的，都调起了`getResponseWithInterceptorChain`,开始了一堆拦截器的层层拦截和过滤。

```
final class AsyncCall extends NamedRunnable {
    private final Callback responseCallback;

    AsyncCall(Callback responseCallback) {
      super("OkHttp %s", redactedUrl());
      this.responseCallback = responseCallback;
    }

    String host() {
      return originalRequest.url().host();
    }

    Request request() {
      return originalRequest;
    }

    RealCall get() {
      return RealCall.this;
    }

    @Override protected void execute() {
      boolean signalledCallback = false;
      try {
        Response response = getResponseWithInterceptorChain();
        if (retryAndFollowUpInterceptor.isCanceled()) {
          signalledCallback = true;
          responseCallback.onFailure(RealCall.this, new IOException("Canceled"));
        } else {
          signalledCallback = true;
          responseCallback.onResponse(RealCall.this, response);
        }
        eventListener.fetchEnd(RealCall.this, null);
      } catch (IOException e) {
        if (signalledCallback) {
          // Do not signal the callback twice!
          Platform.get().log(INFO, "Callback failure for " + toLoggableString(), e);
        } else {
          eventListener.fetchEnd(RealCall.this, e);
          responseCallback.onFailure(RealCall.this, e);
        }
      } finally {
        client.dispatcher().finished(this);
      }
    }
  }
```

交给okHttpClient的`dispatcher（分发器）`放入恰当的双端队列。

```
if (runningAsyncCalls 队列里的AsyncCall对象数 < 64（默认）
  && 与同一Web服务器通讯的并行数 < 5（默认））{
   放入`runningAsyncCalls`队列
 }else{
   放入`readyAsyncCalls`队列
 }

```

### Dispatcher

这里需要提一下Dispatcher分发器的实现，分发器里面维持着三个双端队列（readyAsyncCalls、runningAsyncCalls、runningSyncCalls）和一个线程池

- `readyAsyncCalls` 等待的AsyncCall队列，等待runningAsyncCalls里的线程执行完成被放入线程池执行
- `runningAsyncCalls` 正在执行的AsyncCall队列，队列中线程finish时会调promoteCalls从readyAsyncCalls取出队首线程add并执行
- `runningSyncCalls` 正在执行的RealCall队列，他没用线程池，执行他的就是调用run它的线程
- `executorService` 一个可重用之前60秒内使用过的创建的线程对象的线程池（maxRequests设置了池里最多只能有64个线程体）

另外，两个running队列的线程在finish时都会判断是不是还有运行的Call，如果没有就调起`idleCallback`
