---
layout: post
title: 'okHttp 源码介绍'
subtitle: 'okhttp源码'
date: 2017-11-24
categories: 框架技术
tags: okhttp
---


[TOC]

# Sample

下面的是官方Get请求的sample，我们从它开始说明OkHttp完成网络交互的整个流程。

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
