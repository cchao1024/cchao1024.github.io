---
title: java-函数式编程
date: 2018-06-24 14:58:21
tags: java 
categories: 编程语言
---

# 函数式接口

1. 只包含一个抽象方法的接口，称为**函数式接口**。
2. 你可以通过Lambda表达式来创建该接口的对象。（若Lambda表达式抛出一个受检异常，那么该异常需要在目标接口的抽象方法上进行声明）
3. 我们可以在任意函数式接口上使用@FunctionalInterface注解，这样做可以检查它是否是一个函数式接口，同时javadoc也会包含一条声明，说明这个接口是一个函数式接口。

- 消费型接口: Consumer<T>

  * accept(T t)  接受参数，执行方法
  * andThen：执行完方法后，继续执行 andThen 参数方法 `print.andThen(printPlusSelf).accept(10);`

- 供给型接口:  Supplier<T>   `T get()`

- 函数型接口:  Function<T, R>   `R apply(T t)`

  * apply:  传入一个T类型的参数，返回一个R类型的值

  * compose:  accept获取到的参数，先执行compose里面的Function，再执行原Function
     `toString.compose(plusSelf).apply(10);`
  * andThen：与compose相反。先执行原Function，在执行andThen里面的Function。

- 断言型接口: Predicate<T> `boolean test(T t)`

  * test 测试test方法中输入参数是否满足接口中定义的lambda表达式

  * and 与逻辑运算符 && 一致。

  * negate：对结果取反后再输出

  * or: 与逻辑运算符 || 一致。


Function、Consumer、Supplier、Predicate 四个接口是一切函数式编程的基础。

# 其他进阶接口
> todo

