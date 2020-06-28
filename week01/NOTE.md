学习笔记

pip install  包名 来安装需要使用的第三方包。

常用 pip 源地址

    豆瓣： https://pypi.doubanio.com/simple/
    清华： https://mirrors.tuna.tsinghua.edu.cn/help/pypi/
    中科大： https://pypi.mirrors.ustc.edu.cn/simple/
    阿里云： https://mirrors.aliyun.com/pypi/simple/
更换镜像源，修改方式

临时替换    源地址+包名
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

永久替换（先升级 pip：pip install pip -U ）   源地址
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

包版本的迁移（freeze）
导出  pip freeze > requirements.txt (约定俗称的文件名)
导入  pip install -r requirements.txt

windows下创建虚拟环境
python -m venv venv1 
Windows下进入虚拟环境
venv1\Scripts\activate.bat    （venv1是虚拟环境的名称） 

(1)开发规律
  1.提出需求   具体完成的任务
  2.编码          动手打代码实现功能
  3.代码run起来     能让程序运行起来
  4.修复和完善    修复bug优化

requests简单的爬虫   获取的整个网页的信息
import 导入第三方库
requests.get(myrul,headers=header)
   myurl  存放我们要爬取的网址
   headers  尽可能的去模拟使用的浏览器
增加头部信息 user_agent =' '
	    header = {'user-agent':user_agent}

*不用urllib
   下方还有很多包，引入不便
  要用urlopen打开网页，用read()和decode()来展示网页，操作方式不简洁，没有requests方便
  
(2)beautifulsoup      对网页的信息过滤，获得指定的信息（解析）
   通过网页源代码，来获取需要的指定信息的位置。
    用beautifulsoup进行解析，在导入的是用as进行重命名为bs
    bs_info = bs(response.text, 'html.parser')  //解析之后存到变量bs_info里，只是对整个网页做了一个搜索。
    具体的过滤条件（模拟指针点击网页的操作）
    for tags in bs_info.find_all('div', attrs={'class': 'hd'}):          //使用finde_all方法  attrs是函数参数
    for atag in tags.find_all('a'):
        print(atag.get('href'))        //这里href是取得它的属性，所以直接取  .get
        # 获取所有链接
        print(atag.find('span').text)   // .text方法获取内容  find().text
        # 获取电影名字
     
(3) XPath
使用XPath来简化beautifulsoup的操作
 导入lxml.etree
   # xml化处理
selector = lxml.etree.HTML(response.text)  //处理请求结果
在网页源代码点击要获取的信息，右键高亮部分 copy-copy XPath   来获取XPath
film_name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')   // 同样的text() 是获取内容
print(f'电影名称: {film_name}')
mylist = [film_name, plan_date, rating]    // 将信息汇总
导入pandas库 利用pandas进行保存  可以指定保存的文件格式，编码(Windows改成GBK)
movie1 = pd.DataFrame(data = mylist)     //DataFrame进行汇总
# windows需要使用gbk字符集
movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False) //to_csv 的方式保存成movie1.csv

(4)模拟翻页
通过网页地址的规律来编写对应的函数实现翻页功能。

(5)Scrapy爬虫
Engine        指挥组件协同工作
Scheduler   自动去重
Downloader 下载网页内容
Spiders           爬取信息即实体（Item）  需要修改
Itm Pipelines     存入指定的介质             需要修改
Downloader Middlewares
Spider Middlewares

创建爬虫项目
scrapy startproject spiders  (通用名称spiders)
cd spiders
cd spiders
scrapy genspider   名称  域名
运行项目
scrapy crawl my_scrapy(编写爬虫逻辑的文件名)

allowed_domains  限制爬取域名范围
start_urls   发起第一次请求 异步框架的原因；获取头部信息

item组件 通过管道的方式把数据传递给不同的items（解耦）

通过parse来做具体的操作，可以根据需要写相应的parse

 with open打开的时候 关闭操作是多余的，with可以自动关闭文件

在pipelines中最后要返回 item

selector 配合XPath  提高效率
XPath 路径
// 双斜线  从上到下进行匹配条件
/  单斜线  从最上层开始
.  一个点 从当前位置向下开始找
.. 两个点 从当前位置的同一级(平级位置)开始找
  取内容 text  取属性@

