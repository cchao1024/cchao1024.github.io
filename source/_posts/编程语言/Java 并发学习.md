---
title: Java 并发学习
date: 2018-06-19 11:45:51
tags: java 
categories: 编程语言
---



# 状态

![](https://github.com/CyC2018/CS-Notes/raw/master/notes/pics/adfb427d-3b21-40d7-a142-757f4ed73079.png)



阻塞和等待的区别在于，阻塞是被动的，它是在等待获取一个排它锁。而等待是主动的，通过调用 Thread.sleep() 和 Object.wait() 等方法进入。

| 进入方法                                 | 退出方法                                        |
| ---------------------------------------- | ----------------------------------------------- |
| Thread.sleep() 方法                      | 时间结束                                        |
| 设置了 Timeout 参数的 Object.wait() 方法 | 时间结束 / Object.notify() / Object.notifyAll() |
| 设置了 Timeout 参数的 Thread.join() 方法 | 时间结束 / 被调用的线程执行完毕                 |
| LockSupport.parkNanos() 方法             | LockSupport.unpark(Thread)                      |
| LockSupport.parkUntil() 方法             | LockSupport.unpark(Thread)                      |



# 基础

- SingleThreadExecutor：相当于大小为 1 的 FixedThreadPool。
- 守护线程是程序运行时在后台提供服务的线程，不属于程序中不可或缺的部分。main() 属于非守护线程。
- 对静态方法 Thread.yield() 的调用声明了当前线程已经完成了生命周期中最重要的部分，可以切换给其它线程来执行。该方法只是对线程调度器的一个建议，而且也只是建议具有相同优先级的其它线程可以运行。

# 中断

通过调用一个线程的 interrupt() 来中断该线程，如果该线程处于阻塞、限期等待或者无限期等待状态，那么就会抛出 InterruptedException，从而提前结束该线程。

但是 **不能中断 I/O 阻塞和 synchronized 锁阻塞**

调用 Executor 的 shutdown() 方法会等待线程都执行完毕之后再关闭，但是如果调用的是 shutdownNow() 方法，则相当于调用每个线程的 interrupt() 方法。

如果只想中断 Executor 中的一个线程，可以通过使用 submit() 方法来提交一个线程，它会返回一个 Future<?> 对象，通过调用该对象的 cancel(true) 方法就可以中断线程。

# ReentrantLock

可重入性：一个线程在持有一个锁的时候，它内部能否再次（多次）申请该锁。如果一个线程已经获得了锁，其内部还可以多次申请该锁成功。那么我们就称该锁为可重入锁。

ReentrantLock是Lock接口的一个实现类

- lock, unlock 获取释放锁
- lockInterruptibly 线程未中断则获取锁
- tryLock，tryLock(long, TimeUnit)  线程空闲，或给定时间内空闲获取锁
- newCondition  返回绑定到此Lock实例的新Condition实例

Condition 的作用是对锁进行更精确的控制。

Condition中的await()方法相当于Object的wait()方法，

Condition中的signal()方法相当于Object的notify()方法，

Condition中的signalAll()相当于Object的notifyAll()方法。

不同的是，Object中的wait(),notify(),notifyAll()方法是和”同步锁”(synchronized关键字)捆绑使用的；而Condition是需要与”互斥锁”/”共享锁”捆绑使用的

# AQS

java.util.concurrent（J.U.C）大大提高了并发性能，AQS 被认为是 J.U.C 的核心。

## CountDownLatch

用来控制一个线程等待多个线程。

维护了一个计数器 cnt，每次调用 countDown() 方法会让计数器的值减 1，减到 0 的时候，那些因为调用 await() 方法而在等待的线程就会被唤醒。

```JAVA
public class CountdownLatchExample {

    public static void main(String[] args) throws InterruptedException {
        final int totalThread = 10;
        CountDownLatch countDownLatch = new CountDownLatch(totalThread);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalThread; i++) {
            executorService.execute(() -> {
                System.out.print("run..");
                countDownLatch.countDown();
            });
        }
        countDownLatch.await();
        System.out.println("end");
        executorService.shutdown();
    }
}
```



### CyclicBarrier

```JAVA
public class CyclicBarrierExample {

    public static void main(String[] args) {
        final int totalThread = 10;
        CyclicBarrier cyclicBarrier = new CyclicBarrier(totalThread);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalThread; i++) {
            executorService.execute(() -> {
                System.out.print("before..");
                try {
                    cyclicBarrier.await();
                } catch (InterruptedException | BrokenBarrierException e) {
                    e.printStackTrace();
                }
                System.out.print("after..");
            });
        }
        executorService.shutdown();
    }
}
```

两个类都含有这一个意思：对应的线程都完成工作之后再进行下一步动作

CountDownLatch不可复用，cyclicBarrier 可复用 （cyclic）, CyclicBarrier 的计数器通过调用 reset() 方法可以循环使用，所以它才叫做循环屏障。

```JAVA
// CyclicBarrier 有两个构造函数，其中 parties 指示计数器的初始值，barrierAction 在所有线程都到达屏障的时候会执行一次。
public CyclicBarrier(int parties, Runnable barrierAction)
public CyclicBarrier(int parties)
```

对于CountDownLatch，当计数为0的时候，下一步的动作实施者是main函数。如：lol游戏，10个玩家准备好，由主线程开启游戏

对于CyclicBarrier，下一步动作实施者是“其他线程”。如：有一张门需要N把钥匙组合才能开门，大家商量好同时从不同地方向那张门赶去，必须要等待所有人都到达后才能打开门并进入。

## Semaphore

Semaphore 类似于操作系统中的信号量，可以控制对互斥资源的访问线程数。

```JAVA
public class SemaphoreExample {

    public static void main(String[] args) {
        final int clientCount = 3;
        final int totalRequestCount = 10;
        Semaphore semaphore = new Semaphore(clientCount);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalRequestCount; i++) {
            executorService.execute(()->{
                try {
                    semaphore.acquire();
                    System.out.print(semaphore.availablePermits() + " ");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    semaphore.release();
                }
            });
        }
        executorService.shutdown();
    }
}
```



## FutureTask

FutureTask 可用于异步获取执行结果或取消执行任务的场景。当一个计算任务需要执行很长时间，那么就可以用 FutureTask 来封装这个任务，主线程在完成自己的任务之后再去获取结果。

## BlockingQueue

java.util.concurrent.BlockingQueue 接口有以下阻塞队列的实现：

- **FIFO 队列** ：LinkedBlockingQueue、ArrayBlockingQueue（固定长度）
- **优先级队列** ：PriorityBlockingQueue

提供了阻塞的 take() 和 put() 方法：如果队列为空 take() 将阻塞，直到队列中有内容；如果队列为满 put() 将阻塞，直到队列有空闲位置。

**使用 BlockingQueue 实现生产者消费者问题**

```java
public class ProducerConsumer {

    private static BlockingQueue<String> queue = new ArrayBlockingQueue<>(5);

    private static class Producer extends Thread {
        @Override
        public void run() {
            try {
                queue.put("product");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.print("produce..");
        }
    }

    private static class Consumer extends Thread {

        @Override
        public void run() {
            try {
                String product = queue.take();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.print("consume..");
        }
    }
}
```

## ForkJoin

主要用于并行计算中，和 MapReduce 原理类似，都是把大的计算任务拆分成多个小任务并行计算

ForkJoin 使用 ForkJoinPool 来启动，它是一个特殊的线程池，线程数量取决于 CPU 核数。



# 内存模型

处理器上的寄存器的读写的速度比内存快几个数量级，为了解决这种速度矛盾，在它们之间加入了高速缓存。

所有的变量都存储在主内存中，每个线程还有自己的工作内存，工作内存存储在高速缓存或者寄存器中，保存了该线程使用的变量的主内存副本拷贝。

线程只能直接操作工作内存中的变量，不同线程之间的变量值传递需要通过主内存来完成。

在多处理器下，为了保证各个处理器的缓存是一致的，就会 **实现缓存一致性协议** ，每个处理器通过嗅探在总线上传播的数据来检查自己缓存的值是不是过期了，当处理器发现自己缓存行对应的内存地址被修改，就会将当前处理器的缓存行设置成无效状态，当处理器对这个数据进行修改操作的时候，会重新从系统内存中把数据读到处理器缓存里。

## 三大特性

- 原子性
  * 原子类（AtomicInteger）
  * 互斥锁 synchronized
- 可见性： 当一个线程修改了共享变量的值，其它线程能够立即得知这个修改
  - volatile
  - synchronized，对一个变量执行 unlock 操作之前，必须把变量值同步回主内存。
  - final
- 有序性：在 Java 内存模型中，允许编译器和处理器对指令进行重排序，重排序过程不会影响到单线程程序的执行，却会影响到多线程并发执行的正确性。
  * volatile 关键字通过添加内存屏障的方式来禁止指令重排
  * synchronized 来保证有序性，它保证每个时刻只有一个线程执行同步代码
### volatile 为什么不能保证原子性

使用volatile关键字会强制将修改的值立即写入主存；根据上文 缓存一致，其他线程想要 **读取** （注意，仅是读取时）时 会得到新的值

线程A和线程B 分别对 `volatile i`  进行 i++ 操作。

注意 i++ 不是原子性操作，它可以变成3个操作 :   1. 读取，2. i+1，3. 写入值

1. 线程 A 先读取到 i 的值等于 100，然后阻塞了
2. 线程 B 也读取到 i=100, 然后完成 i++。此时，内存中的 i = 101。
3. 线程 A 继续，使用之前读取到的 100 自加（这里并非101，因为线程 A 并没有执行读取操作），写入内存 i=101;

# 保证线程安全

## 不可变

不可变（Immutable）的对象一定是线程安全的

不可变的类型：

- final 关键字修饰的基本数据类型
- String
- 枚举类型
- Number 部分子类，如 Long 和 Double 等数值包装类型，BigInteger 和 BigDecimal 等大数据类型。但同为 Number 的原子类 AtomicInteger 和 AtomicLong 则是可变的。

对于集合类型，可以使用 Collections.unmodifiableXXX() 方法来获取一个不可变的集合。

## 同步

### 互斥同步

互斥同步最主要的问题就是线程阻塞和唤醒所带来的性能问题，因此这种同步也称为阻塞同步。

互斥同步属于一种悲观的并发策略

synchronized 和 ReentrantLock。

### 非阻塞同步

#### CAS

比较并交换（Compare-and-Swap，CAS）。CAS 指令需要有 3 个操作数，分别是内存地址 V、旧的预期值 A 和新值 B。当执行操作时，只有当 V 的值等于 A，才将 V 的值更新为 B。

#### 原子类

AtomicInteger

J.U.C 包里面的整数原子类 AtomicInteger 的方法调用了 Unsafe 类的 CAS 操作。

#### ABA问题

如果一个变量初次读取的时候是 A 值，它的值被改成了 B，后来又被改回为 A，那 CAS 操作就会误认为它从来没有被改变过。

通过 带有标记的原子引用类 AtomicStampedReference 它可以通过控制变量值的版本来保证 CAS 的正确性。

如果需要解决 ABA 问题，改用传统的互斥同步可能会比原子类更高效。

### 无同步方案

如果一个方法本来就不涉及共享数据，那它自然就无须任何同步措施去保证正确性。

比如，方法内的局部变量，因为它存放在 JVM 栈中，是私有的

#### 可重入代码

这种代码也叫做纯代码（Pure Code），可以在代码执行的任何时刻中断它，转而去执行另外一段代码（包括递归调用它本身），而在控制权返回后，原来的程序不会出现任何错误。

可重入代码有一些共同的特征，例如不依赖存储在堆上的数据和公用的系统资源、用到的状态量都由参数中传入、不调用非可重入的方法等。



# 锁的优化

这里的锁优化主要是指 JVM 对 synchronized 的优化。

- **自旋锁** 让一个线程在请求一个共享数据的锁时执行忙循环（自旋）一段时间，如果在这段时间内能获得锁，就可以避免进入阻塞状态。
- **锁清除** 被检测出不可能存在竞争的共享数据的锁进行消除。
- **锁粗化** 虚拟机探测到由一串零碎的操作都对同一个对象加锁，将会把加锁的范围扩展（粗化）到整个操作序列的外部。如： StringBuffer 的 一连串 append
- **轻量级锁** 相对于传统的重量级锁而言，它使用 CAS 操作来避免重量级锁使用互斥量的开销
- **偏向锁**  偏向于让第一个获取锁对象的线程，这个线程在之后获取该锁就不再需要进行同步操作，甚至连 CAS 操作也不再需要。


# 线程池

```
//基础参数
int corePoolSize=2;//最小活跃线程数
int maximumPoolSize=5;//最大活跃线程数
int keepAliveTime=5;//指定线程池中线程空闲超过 5s 后将被回收
TimeUnit unit = TimeUnit.SECONDS;//keepAliveTime 单位
//阻塞队列
BlockingQueue<Runnable> workQueue = null;
workQueue = new ArrayBlockingQueue<>(5);//基于数组的先进先出队列，有界
workQueue = new LinkedBlockingQueue<>();//基于链表的先进先出队列，无界
workQueue = new SynchronousQueue<>();//无缓冲的等待队列，无界
//拒绝策略
RejectedExecutionHandler rejected = null;
rejected = new ThreadPoolExecutor.AbortPolicy();//默认，队列满了丢任务抛出异常
rejected = new ThreadPoolExecutor.DiscardPolicy();//队列满了丢任务不异常
rejected = new ThreadPoolExecutor.DiscardOldestPolicy();//将最早进入队列的任务删，之后再尝试加入队列
rejected = new ThreadPoolExecutor.CallerRunsPolicy();//如果添加到线程池失败，那么主线程会自己去执行该任务
//使用的线程池
ExecutorService threadPool = null;
threadPool = Executors.newCachedThreadPool();//有缓冲的线程池，线程数 JVM 控制
threadPool = Executors.newFixedThreadPool(3);//固定大小的线程池
threadPool = Executors.newScheduledThreadPool(2);
threadPool = Executors.newSingleThreadExecutor();//单线程的线程池，只有一个线程在工作
threadPool = new ThreadPoolExecutor(
        corePoolSize,
        maximumPoolSize,
        keepAliveTime,
        unit,
        workQueue,
        rejected);//默认线程池，可控制参数比较多
//执行无返回值线程
TaskRunnable taskRunnable = new TaskRunnable();
threadPool.execute(taskRunnable);
List<Future<String>> futres = new ArrayList<>();
for(int i=0;i<10;i++) {
    //执行有返回值线程
    TaskCallable taskCallable = new TaskCallable(i);
    Future<String> future = threadPool.submit(taskCallable);
    futres.add(future);
}
for(int i=0;i<futres.size();i++){
    String result = futres.get(i).get();
    System.out.println(i+" result = "+result);
}
```

# 线程任务按顺序执行

假设有三个线程，分别打印a, b, c。要求  abc,abc,abc,abc 打印十次，而后输出end。

[参考来至](<https://www.jianshu.com/p/2846b5d054c9>)

1. **Join**  Thread的join()方法可以使线程停下来等待另外一个线程执行完毕。

​       Join 的原理是，线程b调用a.join()则线程b进入wait，循环询问，知道a执行完毕，线程b继续执行

2. **Semaphore**   Semaphore是 synchronized 的加强版，作用是控制线程的并发数量
   在 semaphore.acquire() 和 semaphore.release()之间的代码，同一时刻只允许制定个数的线程进入，
3. **notify和wait** 
4. **CountDownLatch(1)**
5. **ReentrantLock和Condition**
6. **阻塞队列**  将问题看做是一个生产者-消费者模型。相当于线程1生产了a之后，线程2取出a，同时生产出来一个b。



# 实践建议

- 给线程起个有意义的名字，这样可以方便找 Bug。
- 缩小同步范围，从而减少锁争用。例如对于 synchronized，应该尽量使用同步块而不是同步方法。
- 多用同步工具少用 wait() 和 notify()。首先，CountDownLatch, CyclicBarrier, Semaphore 和 Exchanger 这些同步类简化了编码操作，而用 wait() 和 notify() 很难实现复杂控制流；其次，这些同步类是由最好的企业编写和维护，在后续的 JDK 中还会不断优化和完善。
- 使用 BlockingQueue 实现生产者消费者问题。
- 多用并发集合少用同步集合，例如应该使用 ConcurrentHashMap 而不是 Hashtable。
- 使用本地变量和不可变类来保证线程安全。
- 使用线程池而不是直接创建线程，这是因为创建线程代价很高，线程池可以有效地利用有限的线程来启动任务。