---
title: Java 注解
date: 2019-06-17 16:59:30
tags:
---

> **Java 注解**又称**Java 标注**，是 [Java](https://www.wikiwand.com/zh/Java) 语言5.0版本开始支持加入[源代码](https://www.wikiwand.com/zh/%E6%BA%90%E4%BB%A3%E7%A0%81)的特殊语法[元数据](https://www.wikiwand.com/zh/%E5%85%83%E6%95%B0%E6%8D%AE)[[1\]](https://www.wikiwand.com/zh/Java%E6%B3%A8%E8%A7%A3#citenote1)。


Java语言中的类、方法、变量、参数和包等都可以被标注。

Java 注解可以通过反射获取标注内容。在编译器生成类文件时，注解可以被嵌入到字节码中。Java 虚拟机可以保留注解内容，在运行时可以获取到注解内容。 也支持自定义Java注解

# 注解分类

## 按运行机制分

1. 源码注解  注解只在源码中存在，编译成 .class文件就不存在了。

2. 编译时注解   注解在源码和 .class文件中都存在。如： @override

3. 运行时注解   在运行阶段还起作用，甚至会影响运行逻辑的注解。如： @Autowired

元注解 给注解的注解


# 自定义注解

## 语法要求
- 使用@interface关键字定义注解
- 成员以无参无异常方式声明
- 可以用default为成员指定一个默认值
- 如果注解只有一个成员，则成员名必须取名value()，在使用时可以忽略成员名和赋值
  号(=)；
- 成员类型是受限的，合法的类型包括原始类型 **String, Class, Annotation, Enumeration**
- 注解类可以没有成员，没有成员的注解称为标识注解


## Sample
```java
@Target({ElementType.CONSTRUCTOR,ElementType.FIELD,ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
@Documented
public @interface javen{
	String name();
	String author();
	int age() default 19;
}
```

## 元注解
- @Target({ElementType.FIELD,ElementType.METHOD})      Target 注解的作用域  
  - CONSTRUCTOR — 构造方法声明，
  - FIELD — 字段声明，
  - LOCAL_VARIABLE — 局部变量声明 ，
  - METHOD — 方法声明，
  - PACKAGE — 包声明，
  - PARAMETER — 参数声明，
  - TYPE — 类接口。
- @Retention(RetentionPolicy.RUNTIME)      Retention 生命周期 
  - SOURCE — 只在源码显示，编译时会丢弃，
  - CLASS — 编译时会记录到class中，运行时忽略，
  - RUNTIME — 运行时存在，可以通过反射读取。
- @Inherited      Inherited 允许子类继承
- @Documented    生成javadoc的时候包含注解


# Referance

[Java 注解 wiki](<https://www.wikiwand.com/zh/Java%E6%B3%A8%E8%A7%A3>)