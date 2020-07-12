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