学习笔记


构建体系
单任务，同步→多任务，同步→多任务，异步
（1）Scrapy并发参数优化原理
settings.py  参数调优
# Configure maximum concurrent requests performed by Scrapy (default: 16)        //默认最大并发连接数
#CONCURRENT_REQUESTS = 32   

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3   //下载延时
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16   //根据域名做限制
#CONCURRENT_REQUESTS_PER_IP = 16           //根据ip做限制

基于twsited 的异步IO框架（异步：如果有多个任务，其中一个任务卡住，另一个任务也能继续进行，不需要等待前一个任务执行完才继续下一个任务。）
先构建好要做的事情，然后获取之后怎么处理返回值，再去跟reactor连接在一起。
通过reactor.run对接到循环当中，有结果就callback，没有结果就下一个请求。 

（2）多进程：进程的创建
进程之间的关系，原有的进程为父进程，新建的进程为子进程。


os.fork()          //只支持linux和mac

multiprocessing.Process()        //更高级的封装，能在win上运行

# - group：分组，实际上很少使用
# - target：表示调用对象，你可以传入方法的名字    （函数）
# - name：别名，相当于给这个进程取一个名字
# - args：表示被调用对象的位置参数元组，比如target是函数a，他有两个参数m，n，那么args就传入(m, n)即可
# - kwargs：表示调用对象的字典


from multiprocessing import Process

def f(name):
    print(f'hello {name}')

if __name__ == '__main__':
    p = Process(target=f, args=('john',))   //函数带不带()是不同，带()传递值
    p.start()
    p.join()
# join([timeout])         设置超时时间，结束父进程。 或者捕获异常
# 如果可选参数 timeout 是 None （默认值），则该方法将阻塞，
# 直到调用 join() 方法的进程终止。如果 timeout 是一个正数，
# 它最多会阻塞 timeout 秒。
# 请注意，如果进程终止或方法超时，则该方法返回 None 。
# 检查进程的 exitcode 以确定它是否终止。
# 一个进程可以合并多次。
# 进程无法并入自身，因为这会导致死锁。
# 尝试在启动进程之前合并进程是错误的。      //join在start后面

（3）多进程：多进程调试  （定位错误）
基本：增加print()的输出和利用注释 ctrl+/

通过内置函数
并不是先父后子顺序去执行，看哪个进程执行的快。
一般创建进程数跟cpu核心数相等   获取cpu核心数量multiprocessing.cpu_count()

通过类的继承来创建并调试
 __init__ 进行传参
super().__init__()  继承Process中已有的inin 不用再去初始化
def run(self):  #重写Process类中的run方法.   这是固定的写法


疑问：
通过导入包的方式，if __name__ == '__main__':下面的东西就不会被运行？
视频下的补充说明没理解 应更改为 进程 0 1 是当前进程的子进程？
都需要传参，继承指定的函数，那用函数和类，两种方式各有什么优势或各自的特点？
还是不太清楚区分父进程和子进程，以及子子进程。

挖坑 super()


（4）多进程：使用队列实现进程间的通信
实际变量赋值是在每一个进程的堆栈当中，跨进程到另一个进程当中，堆栈信息是不会传递过去，这种情况对变量赋值或操作，另一个进程是不知道的。

主要共享方式：
队列    queue  底层是管道，给管道加了线程安全和更多功能
管道
共性内存

资源抢占：
加锁机制

queue
类似排队，前面的操作结束，下一个才能操作，另一个是阻塞的状态

两个主要方法put放数据   get取数据
q.put([42, None, 'hello'])

q.get()
（建议设置最大值）
blocked（阻塞）      timeout两个参数判断队列的空和满来抛出异常

两个同时去写队列，通过加锁机制，不把队列数据搞乱，进程的安全
先进先出
# 队列是线程和进程安全的 ，使用了队列是有默认加锁的

疑问：队列是前一个操作，下一个需要进行等待，那这跟同步操作是什么区别？



（5）多进程：管道和共享内存
管道pipe 是队列的底层
管道两端分别指定成父进程和子进程

send发送数据      revc接收数据
管道两端同时读取或写入可能会造成数据损坏。

共享内存（类似变量赋值）
通过多个进程来共享某一块内存
引入value 和 array
value是一个浮点数
array是一个整数，array只能是一维的


（6）多进程：锁机制

for _ in range(5):     in后面跟着一个容器  下划线是占用一个位置，纯粹是为了循环
与期望结果不符，是不安全的

加锁
引入 mp.lock

def job(v, num, l):            //执行的时候带着锁
    l.acquire() # 锁住
    for _ in range(5):
        time.sleep(0.1) 
        v.value += num # 获取共享内存
        print(v.value, end="|")
    l.release() # 释放

def multicore():
    l = mp.Lock() # 定义一个进程锁   引入lock函数

进程之间去争抢锁，然后执行操作。
疑问：在例子里有定义共享内存，在导入的时候只是multiprocessing，并没有特别指定到value，是已经包含在multiprocessing里面了吗，之前介绍共享内存的时候是有特地导入value（from multiprocessing import Process, Value, Array）

（7）多进程：进程池
from multiprocessing.pool import Pool
通过进程池来管理，创建进程，启动进程数量等。

p = Pool(4) 	//可以同时执行的进程数量，默认为CPU核心数
for i in range(10):
        # 创建进程，放入进程池统一管理
        p.apply_async(run, args=(i,))  //通过异步方式执行，传进来函数对象，args必须是元组

进程池结束功能
p.close()
p.join()
p.terminate()

close  温柔的结束 会等待任务结束再去关闭  close之后不能再添加新的进程
terminate  强制结束  不管任务是否完成
join 会等待进程池中所有的子进程结束完毕再去结束父进程 （在join之前必须要有close 或者terminate，否则会死锁）

扩展
超时处理
支持with 描述符
with Pool(processes=4) as pool:    //加了关键字参数processes更易读懂
        result = pool.apply_async(f, (10,)) # 执行一个子进程     得到的结果是pool对象
        print(result.get(timeout=1))     //显示结果用get 获取结果，转换成可以看到的对象 同时添加超速处理timeout。
超时了抛出raises multiprocessing.TimeoutError 异常

引入Map创建多进程（Map 是单进程并发的功能）
 with Pool(processes=4) as pool:         # 进程池包含4个进程

        print(pool.map(f, range(10)))       # 输出 "[0, 1, 4,..., 81]"      后面的参数必须是一个参数，要多个参数可以转换成元组或者列表
                    
        it = pool.imap(f, range(10))          # map输出列表，imap输出迭代器
        print(next(it))                           //使用next对参数做迭代，调用一次next就取一个值
        print(it.next(timeout=1))        //也可使用timeout
迭代器不取，就不会输出
列表必须知道传出什么对象，只能使用列表支持的方法对它操作
用迭代器，取出来是一个值，不用关心输出的是什么类型

挖坑 关于迭代器和列表元组，字符串的区别

（8）多线程：创建线程
进程线程区别：
进程是一个比较重的概念，如果是多进程并发完成多任务，会对计算机产生很重的资源开销 
多线程编程，多个线程跑在一个进程当中，同步数据更方便。

阻塞，非阻塞（发起方是否在等待）；同步，异步（被发起方是否及时响应）

多进程加多线程：多进程来占用更多的CPU，多线程来方便通信
多线程只能在一个CPU或者一个核心上运行。

协程：多进程和多线程的调度都是由系统来控制，（控制进程启动停止，执行完后开启下一个都是由系统来控制的），为的是在进程切换的时候更轻量级，而且能由用户来进行把控，产生的代码程序就产生了协程。

并发和并行
并发：一个核心，同一时刻只能运行一个进程。  并发是一种现象：同时运行多个程序或多个任务需要被处理的现象
并行：两个核心（多核心） 可以同时通过多进程/多线程的方式取得多个任务，并以多进程或多线程的方式同时执行这些任务

并行的"同时"是同一时刻可以多个进程在运行(处于running)，并发的"同时"是经过上下文快速切换，使得看上去多个进程同时都在运行的现象，是一种OS欺骗用户的现象。

创建
函数方式：threading.Thread(target=run, args=("thread 1",))
类方式：class MyThread(threading.Thread):

调试
thread1.is_alive()  检查线程是否在活动 True在运行 False没有运行

name也是可以修改的

（9）多线程：线程锁
 
mutex = threading.Lock()

        if mutex.acquire(1):    # 加锁 
            num = num + 1
            print(f'{self.name} : num value is  {num}')
        mutex.release()   #解锁

执行多线程的时候，线程并不是从1开始按顺序启动

# Lock普通锁不可嵌套，RLock普通锁可嵌套

mutex = threading.RLock()

class MyThread(threading.Thread):
    def run(self):
        if mutex.acquire(1):
            print("thread " + self.name + " get mutex")
            time.sleep(1)
            mutex.acquire()             //进行嵌套
            mutex.release()
        mutex.release()

高级锁
条件锁  该机制会使线程等待，只有满足某条件时，才释放n个线程  跟设计模式中的生产者／消费者（Producer/Consumer）模式类似
c = threading.Condition()

信号量   内部实现一个计数器，占用信号量的线程数超过指定值时阻塞
semaphore = threading.BoundedSemaphore(5)  # 最多允许5个线程同时运行

事件   定义一个flag，set设置flag为True ，clear设置flag为False
event = threading.Event()

定时器  指定n秒后执行
t = Timer(1,hello)  # 表示1秒后执行hello函数

（10）多线程：队列 Queue
不作为数据通信的工具，作为常用的数据结构。
基本队列
import queue
q = queue.Queue(5)
q.put(111)        # 存队列
q.put(222)
q.put(333)
 
print(q.get())    # 取队列
print(q.get())
q.task_done()# 每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，
                  # 以提示q.join()是否停止阻塞，让线程继续执行或者退出
print(q.qsize())  # 队列中元素的个数， 队列的大小
print(q.empty())  # 队列是否为空
print(q.full())   # 队列是否满了
以生产者消费者为例。
队列其实是线程安全的，可以把锁去掉。

优先级队列
q = queue.PriorityQueue()
# 每个元素都是元组  第一个是优先级，第二个是值
# 数字越小优先级越高
# 同优先级先进先出
q.put((1,"work"))
q.put((-1,"life"))
q.put((1,"drink"))
q.put((-2,"sleep"))

后进先出队列
queue.LifoQueue 后进先出队列,类似堆栈

双向队列（不简洁）
q.deque 双向队列

requests结合队列



疑问：关于self.con.notify() 通知的使用


（11）多线程：线程池
一般的 （复杂）
from multiprocessing.dummy import Pool as ThreadPool

urls = [    ......     ]

# 开启线程池
pool = ThreadPool(4)
# 获取urls的结果
results = pool.map(requests.get, urls)      //map  逐一映射 会把列表拆开
# 关闭线程池等待任务完成退出
pool.close()
pool.join()


# Python3.2 中引入了 concurrent.futures 库，利用这个库可以非常方便的使用多线程、多进程，并行任务的高级封装，更关注业务
from concurrent.futures import ThreadPoolExecutor

if __name__ == "__main__":
    seed = ['a', 'b', 'c', 'd']
    with ThreadPoolExecutor(3) as executor:  //把最大数简写为3
        executor.submit(func, seed)         //submit把参数原样的传入  同样可以用map

    with ThreadPoolExecutor(max_workers=1) as executor:   //max_workers最大数
        future = executor.submit(pow, 2, 3)
        print(future.result())
 
也需要注意避免语法错误或互相等待造成死锁
尽量避免编写多进程多线程的，因为调试更加复杂，尽量编写单任务同步的

疑问：不太明白一般的线程池怎么比高级的线程池复杂，是一般的不支持with描述符吗，因为视频里两种进程池使用的方法不一样，没有对比出两个具体的区别是什么。


（12）多线程：GIL锁与多线程的性能瓶颈

普通      一个CPU核心做计算，一个进程时间
多进程   两个CPU核心，独立计算再做累加，所以时间上几乎是普通的时间的一半
多线程  因为GIL的存在，运行的时候同一时间只能有一个线程运行，所以时间会接近于单独的一个进程

Python解释器中的CPython底层中有一个全局解释锁，让多线程变成伪并发多线程，同一时间只能运行一次。
GIL全局解释锁
  每个进程只有一个GIL
  拿到GIL锁可以使用CPU
  CPython解释器不是真正意义的多线程，属于伪并发

多线程适用于I/O密集型任务（如爬虫），GIL遇到I/O操作就会释放GIl

要根据实际的场景去选择相应的模型。

疑问：为什么要有GIL




