---
title: ElasticSearch 学习
tags: 未定义
categories: 后端技术
date: 2019-07-19 10:36:38
---

# ElasticSearch是什么

> Elasticsearch是一个基于[Apache Lucene(TM)](https://lucene.apache.org/core/)的开源搜索引擎。它目的是通过简单的`RESTful API` 来隐藏Lucene的复杂性，从而让全文搜索变得简单。

- 分布式的实时文件存储，每个字段都被索引并可被搜索
- 分布式的实时分析搜索引擎
- 可以扩展到上百台服务器，处理PB级结构化或非结构化数据

# 核心概念

- **索引(Index)** — 相当于 数据库
- **类型(Type)** — 相当于 数据表
- **文档(Document)** — 相当于数据库的一条记录
- **Field** — 相当于 列(Column)
- **分片(Shard)** — 当有大量的文档时，由于内存的限制、磁盘处理能力不足、无法足够快的响应客户端的请求等，一个节点可能不够。这种情况下，数据可以分为较小的分片。每个分片放到不同的服务器上。 
  当你查询的索引分布在多个分片上时，ES会把查询发送给每个相关的分片，并将结果组合在一起，而应用程序并不知道分片的存在。即：这个过程对用户来说是透明的。
- **副本(Replia)** — 分片的精确复制，每个分片可以有零个或多个副本。ES中可以有许多相同的分片，其中之一被选择更改索引操作，这种特殊的分片称为主分片。 
  当主分片丢失时，如：该分片所在的数据不可用时，集群将副本提升为新的主分片。

**节点(node)**是一个运行着的Elasticsearch实例。**集群(cluster)**是一组具有相同`cluster.name`的节点集合，他们协同工作，共享数据并提供故障转移和扩展功能，当然一个节点也可以组成一个集群。

# Api

ES 基于 Restful API 对 数据进行操作，请求体 为 json 格式

- GET：获取请求对象的当前状态。 
- POST：改变对象的当前状态。 
- PUT：创建一个对象。 
- DELETE：销毁对象。 
- HEAD：请求获取对象的基础信息。

例子：

```bash
http://localhost:9200/blog/ariticle/1 put
{
"title":"New version of Elasticsearch released!",
"content":"Version 1.0",
"tags":["announce","elasticsearch","release"]
}
```



# 安装 ElasticSearch

使用 `docker-compose` 安装 Es，**当前为单机运行**

```bash
version: "3.7"
services:
        
  es-master:
    image: elasticsearch:7.2.0
    container_name: es-master
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    cap_add:
      - IPC_LOCK
    volumes:
      - ./es/master/data:/usr/share/elasticsearch/data
      - ./es/master/es.yml:/usr/share/elasticsearch/config/elasticsearch.yml
    ports:
      - 9200:9200
    networks:
      - esnet

  es-node1:
    image: elasticsearch:7.2.0
    container_name: es-node1
    environment:
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    cap_add:
      - IPC_LOCK
    volumes:
      - ./es/node1/data:/usr/share/elasticsearch/data
      - ./es/node1/es.yml:/usr/share/elasticsearch/config/elasticsearch.yml
    ports:
      - 9201:9200
    links:
      - es-master
    networks:
      - esnet

  es-node2:
    image: elasticsearch:7.2.0
    container_name: es-node2
    environment:
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    cap_add:
      - IPC_LOCK
    volumes:
      - ./es/node2/data:/usr/share/elasticsearch/data
      - ./es/node2/es.yml:/usr/share/elasticsearch/config/elasticsearch.yml
    ports:
      - 9202:9200
    links:
      - es-master
    networks:
      - esnet

  es-head:
      image: mobz/elasticsearch-head:5a
      container_name: es-head
      ports:
        - '9100:9100'

networks:
  esnet:
    
```



# elasticsearch-head

`elasticsearch-head` 是针对elasticsearch的客户端工具 

start 完成后，通过浏览器 验证 `http://localhost:9100/` 是否启动正常 



![](../../images/2019-7/blog20190719111735.png)

- 绿色，最健康的状态，代表所有的分片包括备份都可用

- 黄色，基本的分片可用，但是备份不可用（也可能是没有备份）

- 红色，部分的分片可用，表明分片有一部分损坏。此时执行查询部分数据仍然可以查到，遇到这种情况，还是赶快解决比较好

- 灰色，未连接到elasticsearch服务



# 周边

**ELK=elasticsearch+Logstash+kibana **

- elasticsearch：后台分布式存储以及全文检索
- logstash: 日志加工、“搬运工” 
- kibana：数据可视化展示。 

ELK架构为数据分布式存储、可视化查询和日志解析创建了一个功能强大的管理链。 三者相互配合，取长补短，共同完成分布式大数据处理工作。