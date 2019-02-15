---
layout: post
title: Java8 简明教程
subtitle: Java8
date: 2017-12-1
categories: java
tags: 编程语言
---

# 特性

- 接口的默认方法和静态方法
- 函数式接口FunctionInterface与lambda表达式
- 方法引用
- Stream，Optional
- 
- Date/time API的改进



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

通过将集合转换为这么一种叫做 “流” 的元素序列，通过声明性方式，能够对集合中的每个元素进行一系列并行或串行的**流水线操作**。

* 元素 - 是特定类型的对象，形成一个队列。Java中的Stream并不会存储元素，而是按需计算。
* 数据源 - 流的输入，可以是集合，数组或I/O资源。
* 聚合操作 - 如filter, map, limit, reduced, find, match等处理元素的操作。
* 管道传输 - 大多数流操作的返回流本身使他们的结果可以被管道传输。这些操作被称为中间操作以及它们的功能是利用输入，处理输入和输出返回到目标。collect()方法是终端操作，这是通常出现在管道传输操作结束标记流的结束。
* 自动迭代 - 流操作内部做了反复对比，其中明确迭代需要集合提供源元素。



流和迭代器类似，只能迭代一次。



### stream() / parallelStream()  将集合转换成流

filter（T -> boolean）剔除返回值为false的元素

distinct 剔除重复元素，通过equals判断两元素是否相同

sorted/sorted((T,T)-> int) 对元素进行排序，通过Comparable接口实现排序规则

limit(long n) 返回前n个元素

skip(long n) 剔除前n个元素

map(T -> R) 流中的元素类型转化为R

flatMap(T -> Stream<R>)  汇聚水流

anyMatch(T -> boolean) 检查流中是否有元素满足条件规则

allMatch(T -> boolean) 检查流中所有元素是否都满足条件规则

noneMatch(T -> boolean) 检查流中所有元素是否都不满足条件规则

findAny() 找到其中一个元素

findFirst 找到第一个元素

reduce((T,T) -> T)  对流中元素进行组合操作，如：求和，求积

reduce(T,(T,T) -> T)   对流中元素进行组合操作，第一个参数是起始值

count() 返回流中元素的个数

collect() 收集器，

forEach()  遍历流中元素

--------------



### 数值流

#### 流转换为数值流

- mapToInt(T -> int) : return IntStream
- mapToDouble(T -> double) : return DoubleStream
- mapToLong(T -> long) : return LongStream



数值流转换为流

```
intStream.boxed();
DoubleStream.boxed();
```

- sum()
- max()
- min()
- average() 等...
- range(x,y) 生成x到y开区间内的元素数值流，(1,100)    x<= int <=y  
- rangeClosed(x,y) 生成x到y范围内的元素数值流  [1,100)   x< int <=y

## Optional
Optional是一个容器类，可以代表一个值存在或不存在
- isPresent() ：值存在时返回 true，反之 flase
- get() ：返回当前值，若值不存在会抛出异常
- orElse(T) ：值存在时返回该值，否则返回 T 的值
其还有三个类似版本 OptionalInt，OptionalLong，OptionalDouble

### collect
coollect 方法作为终端操作，接受的是一个 Collector 接口参数，能对数据进行一些收集归总操作

- toList
- toSet
- toCollection
- toMap
- counting
- summingInt
- summingLong
- averagingInt
- averagingLong
- summarizingInt  返回 平均数，和，最值操作
- max
- Joining 连接字符串



