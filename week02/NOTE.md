学习笔记

（1）异常捕获与处理
异常不等于错误
错误：代码编写导致语法上的错误，或者对需求理解错误，编码实现功能出错
异常：一种是用户的输入在系统中产生意想不到的结果，另外是系统代码中的输入输出产生意想不到的结果，导致程序终止或运行异常。发现异常的时候第一时间通知开发者并且让程序停止。
 
异常也是一个类
异常捕获过程：
  1.异常类把错误消息打包到一个对象。
  2.然后该对象会自动查找到调用栈。
  3.直到运行系统找到明确声明如何处理这些类异常的位置。
所有异常继承自BaseException
Traceback显示了出错的位置，显示的顺序和异常信息对象传播的方向是相反的（从下向上看） 
*异常信息在Traceback信息的最后一行，有不同类型
*捕获异常可以使用try...except语法
*try...except支持多重异常处理（嵌套。通过缩进区分）
常见的异常类型主要有：
  1.LookupError 下的IndexError 和KeyError
  2.IOError
  3.NameError
  4.TypeError
  5.AttributeError
  6.ZeroDivisionError

自定义异常
class UserInputError(Exception):     //自定义名为UserInputError的异常
    def __init__(self, ErrorInfo):           //其他先记为固定写法      
        super().__init__(self, ErrorInfo)  //双下划线统称为魔术方法
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo
try:         
    if (not userinput.isdigit()):
        raise UserInputError('用户输入错误')
except UserInputError as ue:
    print(ue)
finally:    //不论是否抛出异常都会进行的操作
    del userinput

import pretty_errors   导入pertty_errors来对异常结果进行美化
 **pip install pretty_errors

文件打开
  with open('a.txt', encoding='utf8') as file2:  //通过with打开的文件 发生异常自动关闭
    data = file2.read()

（2）PyMySQl数据库操作

**pip install pymysql

#  /usr/local/mysql/support-files/mysql.server start     //启动mysql服务
# 一般流程
# 开始-创建connection-获取cursor(游标)-CRUD(查询并获取数据)-关闭cursor-关闭connection-结束

配置好mysql的设置        //最好把配置放在专门的文件再去加载（配置文件）
dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'rootroot',
    'db' : 'test'
}                                    //尽量复用链接
配置初始化
class ConnDB(object):
    def __init__(self, dbInfo, sqls):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.sqls = sqls


（3）反爬虫：模拟浏览器的头部信息
让爬虫更像浏览器
User-Agent:
Referer:跳转过来的页面信息
Cookies：登录的信息

**pip install fake-useragent
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

# 模拟不同的浏览器
print(f'Chrome浏览器: {ua.chrome}')
# print(ua.safari)
# print(ua.ie)

# 随机返回头部信息，推荐使用
print(f'随机浏览器: {ua.random}')

（4）cookies验证
存在有效期，需要模拟用户登录，获取cookies
  
         # http 协议的 POST 方法
import requests
r = requests.post('http://httpbin.org/post', data = {'key':'value'})
r.json()
 #httpbin 用来 http学习和调试的网站

      # 在同一个 Session 实例发出的所有请求之间保持 cookie
s = requests.Session()

s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")

查看basic（登录后跳转的页面）
   Request URL(发起请求的地址):
   Request Method(请求方式）:      //Post方式封装信息与scrapy中用start_url代替
   Cookie:
   Host(请求的主机):
   Referer(从哪跳转过来的地址):
   User-Agent:
提交要求 查看浏览器的form_data  要一致
s = requests.Session()
# 会话对象：在同一个 Session 实例发出的所有请求之间保持 cookie， 
# 期间使用 urllib3 的 connection pooling 功能。
# 向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
login_url = 'https://accounts.douban.com/j/mobile/login/basic'
form_data = {
'ck':'',
'name':'15055495@qq.com',
'password':'test123test456',
'remember':'false',
'ticket':''
}

response = s.post(login_url, data = form_data, headers = headers)

疑问：# response3 = newsession.get(url3, headers = headers, cookies = s.cookies)      这里的cookies = s.cookies   中s.cookies的cookies是不是前面s = requests.Session() 中获得的已经存放在session里面了？

（5）WebDriver模拟浏览器行为
**pip install selenium
    browser = webdriver.Chrome()
    # 需要安装chrome driver, 和浏览器版本保持一致  // 需要相应的浏览器驱动放置到当前解析的相同目录中
    # http://chromedriver.storage.googleapis.com/index.html
    
    browser.get('https://www.douban.com')
      ##这里没有通过网络的跳转，只是通过前端，所以这里要把iframe切换为0到输入框
    browser.switch_to_frame(browser.find_elements_by_tag_name('iframe')[0])
    btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')              //切换到密码输入框的位置
    btm1.click() //再通过点击操作

    browser.find_element_by_xpath('//*[@id="username"]').send_keys('15055495@qq.com')                     //找到指定位置，输入账号
    browser.find_element_by_id('password').send_keys('test123test456') //输入密码
    browser.find_element_by_xpath('//a[contains(@class,"btn-account")]').click()          //找到登录按钮 点击
    cookies = browser.get_cookies() # 获取cookies

加密链接的请求
btm1 = browser.find_element_by_xpath('//*[@id="hot-comments"]/a')
    btm1.click()         //通过找到对应位置，模拟浏览器点击操作
    time.sleep(10)
    print(browser.page_source)   

分块下载

############# 大文件下载：
# 如果文件比较大的话，那么下载下来的文件先放在内存中，内存还是比较有压力的。
# 所以为了防止内存不够用的现象出现，我们要想办法把下载的文件分块写到磁盘中。
import requests
file_url = "http://python.xxx.yyy.pdf"
r = requests.get(file_url, stream=True)   //steam 流式下载
with open("python.pdf", "wb") as pdf:
    for chunk in r.iter_content(chunk_size=1024):   //分块下载 1024字节，自行设置
        if chunk:
            pdf.write(chunk)
疑问：要是每次项目都需要用webdriver，那是不是都要手动去把对应浏览器的driver放到目录下？

（6）验证码  ——简单验证码 图形

先安装依赖库（第三方插件）
   # 先安装依赖库libpng, jpeg, libtiff, leptonica    //支持更丰富的图片格式
   # brew install leptonica
   # 安装tesseract          //C语言可执行的命令
   # brew install  tesseract
 **# 与python对接需要安装的包
   # pip3 install Pillow    //对图片做处理
   # pip3 install pytesseract   //调取命令

把验证码图片下载
# 打开并显示文件
im = Image.open('cap.jpg')
im.show()

# 灰度图片    //变成计算机能识别的信息
gray = im.convert('L')
gray.save('c_gray2.jpg')
im.close()

# 二值化          //深色更深，浅色更浅，去除背景
threshold = 100
table = []

for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

out = gray.point(table, '1')
out.save('c_th.jpg')

th = Image.open('c_th.jpg')
print(pytesseract.image_to_string(th,lang='chi_sim+eng'))   //做一个切分
  //tesseract默认支持简体中文和英文
# 各种语言识别库 https://github.com/tesseract-ocr/tessdata
# 放到 /usr/local/Cellar/tesseract/版本/share/tessdata

疑问：灰度处理和二值化用到的参数和方法的作用，还有切分的目的是什么？
brew install  是在哪里进行安装？
无法将“brew”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。

（7）爬虫中间件&系统代理IP
可以用多个中间件（去从左到右，回从右到左——优先级）
实现通过代理IP更改直接请求的IP（给下载中间件改一个代理IP）

##关注日志信息
  引擎模块Twisted 
  对应的配置信息
  扩展信息
  中间件  downloadermidderwares
              spidermiddlewares
  运行结果
  downloader下载器信息
  scheduler调度器信息
scrapy crawl httpbin --nolog  可以去除日志信息

系统代理IP （Scrapy默认支持系统代理自动导入，）

在settings文件里，把DOWNLOADER_MIDDLEWARES注释去掉，写入想要添加的中间件，并指定好优先级（数字越小越优先），暂时不用可以指定为None

自行编写代理，在middlewares文件里，继承已有的类，再去做相应的编写

疑问：在settings文件里 更改User-Agent和Cookies的时候也是使用的中间件吗？
# export http_proxy='http://52.179.231.206:80'   在windows中对应的操作是什么？ 还有为什么ip先经过52.179.231.206:80，然后通过代理ip就变成另外的IP？

（8）自定义中间件&随机代理IP
编写下载中间件，一般重写下面四个主要方法：  （至少实现其中一个方法）
process_request(request,spider)         //真正的请求
request对象经过下载中间件时会被调用，优先级高先调用

process_response(request,response,spider)  //完成后返回
response对象经过下载中间件时会被调用，优先级高后调用

process_exception(request,exception,spider)   //异常处理 （健壮）
当process_response()和process_request()抛出异常时会被调用

from_crawler(cls,crawler)              // 比如初始化信息
使用crawler来创建中间器对象，并（必须）返回一个中间件对象

配置文件 变量都是大写
settings.py文件里面           
DOWNLOADER_MIDDLEWARES = {     //要加载的下载中间件
            'proxyspider.middlewares.RandomHttpProxyMiddleware': 400,	
                // '项目名.middlewares.类名':400（优先级）,      
}

HTTP_PROXY_LIST = [          //存放的代理IP
     'http://52.179.231.206:80',
     'http://95.0.194.241:9090',
]

middlewares文件里
先导入许多包
from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
from collections import defaultdict
from urllib.parse import urlparse
import random

#通过继承HttpProxyMiddleware（读取系统默认代理），然后重写方法
class RandomHttpProxyMiddleware(HttpProxyMiddleware):  
	
        def __init__(self, auth_encoding='utf-8', proxy_list = None): //初始化，接收输入   读取settings
        self.proxies = defaultdict(list)  //把list初始化为字典，因为settings处理都是字典方式
        for proxy in proxy_list:
            parse = urlparse(proxy)  //把http 跟后面的ip做一个拆分
            self.proxies[parse.scheme].append(proxy)   //这里对应字典的key跟value

    @classmethod  // 装饰器 （语法糖）  可以直接调用，不需要实例化
    def from_crawler(cls, crawler):   //判断对应的配置文件
        if not crawler.settings.get('HTTP_PROXY_LIST'):  //读取对应的文件
            raise NotConfigured

        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')  
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')
      #在装饰器下，from_crawler方法直接被最外层的类拿去用
        return cls(auth_encoding, http_proxy_list)   //所以这里返回到上面的init，对应的实例化去接收

    def _set_proxy(self, request, scheme):           //这里设置proxy
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy


疑问：这里三个scheme之间是怎么对应的，scheme的作用是什么？

（9）分布式爬虫
多机通讯，多机同时爬取
需要Redis实现队列和管道的共享（机器要先安装Redis）
scrapy-redis实现Scrapy和Redis的集成
使用scrapy-redis之后Scrapy的主要变化：
1.使用RedisSpider类替代了Spider类
2.Scheduler的queue由Redis实现
3.item pipeline由Redis实现

**pip install scrapy-redis

启动之前做好redis.conf的配置
bind  绑定的ip
port  默认端口 6379 用端口检查redis是否运行
daemonize yes 不会因关掉终端而结束

服务端启动 
redis-server redis.conf

客户端连接
redis-cli

在爬虫编码上基本没什么区别，主要是更改settings设置
settings里设置相应的redis 把原有的Scrapy替换为scrapy-redis

# redis信息
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379

# Scheduler的QUEUE
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Requests的默认优先级队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# 将Requests队列持久化到Redis，可支持暂停或重启爬虫
SCHEDULER_PERSIST = True

# 将爬取到的items保存到Redis
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}


其他的爬虫去调用相同的Redis 就实现了之间的相互通信
Redis集群存储爬取到的数据，再慢慢传入到MySQL数据库中


#  redis 会自动存储到pipeline的item
在命令行终端输入
#  bash$  redis-cli      //进入redis命令
#  redis> keys *         // 看存储key
#  redis> type cluster:items   //查看类型
#  redis> lpop cluster:items   //查看值
#  redis> keys *           //再次查看就空了

疑问：win系统Redis的安装，多机安装以及多台机器的客户端跟服务端的连接还是直接redis-cli吗？是不是要另外的配置，因为视频里是服务端跟客户端同意一台机器，分不清区别。