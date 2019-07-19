---
title: Java 反射
date: 2018-06-17 17:32:40
tags: java 
categories: 编程语言
---

>  **反射**是指[计算机程序](https://www.wikiwand.com/zh/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A8%8B%E5%BA%8F)在[运行时](https://www.wikiwand.com/zh/%E8%BF%90%E8%A1%8C%E6%97%B6)（Run time）可以访问、检测和修改它本身状态或行为的一种能力。
>
> 要注意术语“反射”和“[内省](https://www.wikiwand.com/zh/%E5%86%85%E7%9C%81_(%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6))”（type introspection）的关系。内省（或称“自省”）机制仅指程序在运行时对自身信息（称为[元数据](https://www.wikiwand.com/zh/%E5%85%83%E6%95%B0%E6%8D%AE)）的检测；反射机制不仅包括要能在运行时对程序自身信息进行检测，还要求程序能进一步根据这些信息改变程序状态或结构。

“程序运行时，允许改变程序结构或变量类型，这种语言称为[动态语言](https://baike.baidu.com/item/%E5%8A%A8%E6%80%81%E8%AF%AD%E8%A8%80/797407)”。从这个观点看，Perl，Python，Ruby是动态语言，C++，Java，C# 不是动态语言。

Java 反射（Reflection）使我们可以于运行时加载、探知、使用编译期间完全未知的classes。

> 编译方式说明：
> 1. 静态编译：在编译时确定类型 & 绑定对象。如常见的使用`new`关键字创建对象
> 2. 动态编译：运行时确定类型 & 绑定对象。动态编译体现了`Java`的灵活性、多态特性 & 降低类之间的藕合性

换句话说，Java程序可以加载一个运行时的class，获悉其完整构造，并生成其对象实体、或对其fields设值、或唤起其methods。

# Class

反射机制的实现 主要通过 **操作java.lang.Class类** ， `java.lang.Class` 类是反射机制的基础

`Java` 反射机制的实现除了依靠 `Java.lang.Class` 类，还需要依靠：`Constructor`类、`Field`类、`Method`类，分别作用于类的各个组成部分：

- Class 类对象
- Constructor 类的构造对象
- Field 类的属性对象
- Method 类的方法对象

获取 Class 对象的方法

1. Object.getClass()
2. T.class
3. Class.forName
4. T.TYPE

# Field Method
获取到 Class 后，需要拿到类的属性和方法才能对 fields设值、或唤起其methods。
获取 Field 和 Method 的方法名比较规律，格式为 

```java
# 获取单个值, 根据获取的不同值，需传入不同参数
get + [Field|Annotation|Constructor] + ([String name|Class<A> annotationClass|Class...<?> parameterTypes])
# 获取所有值
get + [Fields|Annotations|Constructors]
```
默认获取的是共有的值， 加上 **Declared** 表示也获取私有值，如：

```java
getDeclaredField(String name)
```

获取到  Field 和 Method 后，可以对他进行赋值或调用

## 调用

* Field
   -  equals(Object obj)            属性与obj相等则返回true
   -  get(Object obj)               获得obj中对应的属性值  
   -  set(Object obj, Object value) 设置obj中对应属性值    
* Method
   - invoke(Object obj, Object... args)  传递object对象及参数调用该对象对应的方法 

* Constructor
   - newInstance(Object... initargs)    根据传递的参数创建类的对象   


# Referance

[Java 反射 wiki](<https://www.wikiwand.com/zh/%E5%8F%8D%E5%B0%84_(%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6)>)

[Java 反射 百度百科](<https://baike.baidu.com/item/JAVA%E5%8F%8D%E5%B0%84%E6%9C%BA%E5%88%B6/6015990?fr=aladdin>)

[https://www.jianshu.com/p/9be58ee20dee](<https://www.jianshu.com/p/9be58ee20dee>)