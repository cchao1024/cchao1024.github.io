---
layout: post
title: Java8 简明教程
subtitle: Java8
date: 2017-12-1
categories: java
tags: 编程语言
---

# Lambda

## 语法

**parameter -> expression body**

- 可选的参数类型声明 - 无需声明参数的类型
- 可选的参数圆括号 - 只有一个参数可以不要括号包裹（零个或多个必须）
- 可选的大括号 - 只有一条语句可以不要大括号包裹（多条必须）
- 可选的retrun语句 - 如果只有一条语句默认实现了return

只具有一个方法的接口称为 **函数式接口**。函数式接口，可以被隐式转换为lambda表达式。如：java.lang.Runnable 。 为防止函数式新增方法导致编译失败（因为增加了方法接口就不止一个方法了），Java 8增加了注解 **@FunctionalInterface** 声明该接口为函数式接口。

特别的：默认方法与静态方法并不影响函数式接口，可以任意使用：

## 实例

```java
public class JavaTest {
    public static void main(String[] args) {
        IMathOp mathOp = (x, y) -> x + y;
        System.out.println(mathOp.add(43, 5));
        // Runnable
        new Thread(() -> System.out.print(mathOp.add(24, 2)))
            .start();
    }

    @FunctionalInterface
    interface IMathOp {
        int add(int x, int y);
        default int say(int y){
            return y;
        }
    }
}
```
## 方法引用

# 接口的默认方法与静态方法

接口方法可以通过 default 关键字声明默认实现。
接口方法可以通过 static 关键字声明静态方法。

如果有多重默认（类实现的接口里有相同的默认方法），则必须重写该接口方法，通过 interface.super.method() 调用特定接口方法。
```JAVA
public class Java8Tester {
    public static void main(String args[]){
        Vehicle vehicle = new Car();
        vehicle.print();
    }
}
interface Vehicle {
    default void print(){
        System.out.println("I am a vehicle!");
    }
    static void blowHorn(){
        System.out.println("Blowing horn!!!");
    }
}
interface FourWheeler {
    default void print(){
        System.out.println("I am a four wheeler!");
    }
}
class Car implements Vehicle, FourWheeler {
    /*
    @Override
    public void print() {
        // 覆盖默认实现
    }
    */
    @Override
    public void print(){
        Vehicle.super.print();
        FourWheeler.super.print();
        Vehicle.blowHorn();
        System.out.println("I am a car!");
    }
}

```

# Optional 类
Optional 类是一个可以为null的容器对象。如果值存在则isPresent()方法会返回true，调用get()方法会返回该对象。
Optional 是个容器：它可以保存类型T的值，或者仅仅保存null。Optional提供很多有用的方法，这样我们就不用显式进行空值检测。
Optional 类的引入很好的解决空指针异常。

|方法及说明|
--|--
static < T> Optional< T> empty() |返回一个空的 Optional 实例。
boolean equals(Object obj)|表示某个其他对象是否“等于”此Optional。
Optional< T> filter(Predicate<? super T> predicate)| 如果值存在，并且该值给定的谓词匹配，返回一个可选描述值，否则返回一个空Optional。
< U> Optional< U> flatMap(Function<? super T,Optional<U>> mapper)|如果值存在，应用提供的可选承载映射功能到它，返回结果，否则返回一个空Optional。
T get()|如果值是出现在这个 Optional 中，返回这个值，否则抛出NoSuchElementException异常。
int hashCode()|返回当前值，哈希码值（如有）或0（零），如果值不存在。
void ifPresent(Consumer<? super T> consumer)|如果值存在，调用指定的使用方提供值，否则什么都不做。
boolean isPresent()|返回true，如果有一个值存在，否则为false。
<U> Optional<U> map(Function<? super T,? extends U> mapper)|如果值存在，应用提供的映射函数，如果结果非空，返回一个Optional描述结果。
static < T> Optional< T> of(T value)|返回一个Optional具有指定当前非空值。
static < T> Optional< T> ofNullable(T value)|返回一个Optional描述指定的值，如果非空，否则返回一个空的Optional。
T orElse(T other)|返回值（如果存在），否则返回other。
T orElseGet(Supplier<? extends T> other)|如果存在，返回值，否则调用其他并返回调用的结果。
<X extends Throwable> T orElseThrow(Supplier<? extends X> exceptionSupplier)|返回所含值，如果存在的话，否则抛出将由提供者创建的一个例外。
String toString()|返回此Optional 适合调试一个非空字符串表示。

code

```java
public class Java8Tester {
   public static void main(String args[]){

      Java8Tester java8Tester = new Java8Tester();
      Integer value1 = null;
      Integer value2 = new Integer(10);

      // Optional.ofNullable - 允许传递为 null 参数
      Optional<Integer> a = Optional.ofNullable(value1);

      // Optional.of - 如果传递的参数是 null，抛出异常 NullPointerException
      Optional<Integer> b = Optional.of(value2);
      System.out.println(java8Tester.sum(a,b));
   }

   public Integer sum(Optional<Integer> a, Optional<Integer> b){

      // Optional.isPresent - 判断值是否存在

      System.out.println("第一个参数值存在: " + a.isPresent());
      System.out.println("第二个参数值存在: " + b.isPresent());

      // Optional.orElse - 如果值存在，返回它，否则返回默认值
      Integer value1 = a.orElse(new Integer(0));

      //Optional.get - 获取值，值需要存在
      Integer value2 = b.get();
      return value1 + value2;
   }
}
```

# Stream

Stream（流）是来自数据源的元素队列，支持聚合操作。
* 元素 - 是特定类型的对象，形成一个队列。Java中的Stream并不会存储元素，而是按需计算。

* 数据源 - 流的输入，可以是集合，数组或I/O资源。

* 聚合操作 - 如filter, map, limit, reduced, find, match等处理元素的操作。

* 管道传输 - 大多数流操作的返回流本身使他们的结果可以被管道传输。这些操作被称为中间操作以及它们的功能是利用输入，处理输入和输出返回到目标。collect()方法是终端操作，这是通常出现在管道传输操作结束标记流的结束。

* 自动迭代 - 流操作内部做了反复对比，其中明确迭代需要集合提供源元素。
