学习笔记
（1）开发环境配置
数据展示 多端展示 网页形式

Web框架  web.py   Django Flask  Tornado 等等
遵循MVC模式


Django
以python开发的框架
采用MTV框架（模型【数据】模版 视图【接收请求 调用models 调用Template 响应】）
代码复用（DRY）
组件丰富（关注业务逻辑）
    ORM（对象关系映射）映射类来构建数据模型
    URL支持正则表达式
    模版可继承
    内置用户认证，提供用户认证和权限功能
    admin管理系统
    内置表单模型、Cache缓存系统、国际化系统等

安装
pip  install (--upgrade做升级) django==2.2.13
>>import django 
>>django.__version__   查询版本

用稳定版本，非必要则继续延续旧版本


（2）创建项目
不能直接import使用（Web服务器形式，一直等待着发起连接）
先创建项目
$ django-admin startproject MyDjango（项目名）
$ find MyDjango （查看目录）
创建程序
$ python manage.py startapp index（程序名）
$ python manage.py help  查看具体的功能
运行
$ python manage.py runserver    （默认127.0.0.1:8080）
更改端口
$ python manage.py runserver 0.0.0.0:80
$ Ctrl+c结束

整个项目下
manage.py
settings.py

程序下需要关注的文件
models.py
views.py

另外template需要手动创建


（3）解析settings  ①②

项目路径    os.path.dirname 读取路径

密钥   生产环境部署的密钥设置，建议修改一个较长，较复杂的密钥
 
调试模式        仅用于开发，会打印大量的日志，只能单用户访问

INSTALLED_APPS =[     ]    默认支持的应用程序，自带的程序不要随意改变书写的顺序（不需要可以注释），除非在对应的程序做了修改，要去手动添加自己的程序，自己加的程序在默认程序后面  ①

中间件保持默认

ROOT_URLCONF =' 项目名.urls'     默认使用项目里的urls.py

TEMPLATES   对模版的设置，默认下不改动
              'BACKEND':   可以在这里更换模版的引擎
              'APP_DIRS' :TRUE  一般在应用程序里放置模版，设为TRUE在app里查找模版

WSGI_APPLICATION  调用WSGI

数据库配置  ②   确保有安装好数据库连接包  # pip install pymysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': 'rootroot',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
    # 生产环境有可能连接第二个数据库
    # 'db2': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'mydatabase',
    #     'USER': 'mydatabaseuser',
    #     'PASSWORD': 'mypassword',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3307',
    # }
}
更换为mysql，相应的mysql客户端也要安装，并配置好变量，在python中也要对应的安装加载mysql的驱动，pip install pymysql
**关于版本判断的问题

密码验证  不需要更改

时区 语言改成对应的

静态文件



（4）urls调度器
URLconf
#MyDjango/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('index.urls')),        用include导入程序（绑定）,把功能分为多个程序
]                                   访问为空时，由其他脚本文件解析，写好相应的视图

#index/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index)    这里的index是指函数名，上面的index表示的是程序名
]

#index/views.py
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello Django!")

urls转到view视图
运行manage.py→settings.py(ROOT_URLCONF = 'MyDjango.urls' 项目) →MyDjango/urls.py → 匹配到空 include下绑定 index程序下的urls网址(在settings.py里面注册好对应的程序)  → index/urls.py 程序（通过include过来的要找到urlpatterns）→ 通过 . 在当前路径下 找到views.py → 找到index函数，把请求传递给函数。
找到视图文件后对请求做处理，再进行返回


（5）模块和包
模块： .py结尾的Python程序
        既能执行又可做定义
         if __name__ == '__main__':      //上面写定义，下面写执行
       用做模块的时候 __name__ 就会编程文件名，执行的时候 __name__就会变成main

包：存放多个模块的目录

__init__.py 包运行的初始化文件，可以是空文件   被导入包的时候优先运行这个文件


导入
import
from ... import ...  (as)
同级目录使用 from .  相对路径的方式去调用（比如同目录下模块之间相互调用）


（6-7）URL支持变量
对一类请求处理
对类型做处理；支持正则表达式，；匹配自定义的规则

变量类型包括：str; int; slug（备注）; uuid; path。
一个变量
path('<int:year>',views.myyear),  用尖括号括起来，定义好类型，变量，传递的view视图
传入指定类型的变量，才能做处理，否则返回404的错误

多个变量
path('<int:year>/<str:name>',views.name),
在views中接收不定长的参数，不用具体指定，用**kwargs接收，下标指定具体取参
   def name(request,**kwargs):
              return HttpResponse(kwargs['name'])   

正则表达式
path改用re_path('(?P<year>[0-9]{4}).html',views.myyear,name='urlyear'),
?P作为正则开始的标志，()表示正则的范围，name指定这个路径名，之后可以让template去使用
def myyear(request, year):
    return render(request, 'yearview.html')      返回的时候可以指定到一个文件里
Template文件
<a href="{% url 'urlyear' 2020 %}">2020 booklist</a>

自定义匹配
from . import views, converters  导入自己编写的定义文件
要去自己编写一个文件，然后注册进来
register_converter(converters.IntConverter,'myint')  文件名.定义的类名，起别名
register_converter(converters.FourDigitYearConverter, 'yyyy')
在 #converters.py
class IntConverter:      定义一个类，做一个类似重写
    regex = '[0-9]+'      匹配的规则， 以字符串的形式引入

    def to_python(self, value):    从url获取的去转到python里
        return int(value)

    def to_url(self, value):   把python里的再传回url
        return str(value)
必须包含三个部分 regex（定义的规则）； to_python ； to_url

    ### 自定义过滤器
    path('<yyyy:year>', views.year), 

注意在使用前要引入re_path包，register_converter包
from django.urls import path, re_path, register_converter

（8）view视图快捷方式
Response返回（基础返回）
HttpResponse('Hello world')     200，成功接收
HttpResponseRedirect('/admin/')  302，重定向
HttpResponsePermanentRedirect('/admin/') 301，永久重定向
HttpResponseBadRequest('BadRequest')  400，页面不存在或请求错误
HttpResponseNotFound('NotFound')  404，页面不存在或URL失效
HttpResponseForbidden('NotFound')  403，没有访问权限
HttpResponseNotAllowed('NotAllowedGet')  405，不允许该请求方式
HttpResponseSeverError('SeverError')  500，服务器内容错误

二次封装
快捷函数
render()   把返回的内容写入到专门的文件里，支持导入变量
就是模版文件跟view视图绑定
     return render(request,'yearview.html')    依然要接受request，加上返回的文件
没有指定路径，在settings里已经把模版配置 'APP_DIRS':True,设置为True了，默认去查找templates（手动创建，名称不要变）

redirect()    将一个HttpResponseRedirect返回到传递的参数的适当URL
做URL的解析，然后重新回到URL实现跳转（一般用于验证登录后的跳转）
    return redirect('/2020.html')  这样就返回到urls去做解析


get_object_or_404()  从模型取数据，取不到直接返回404  
view视图和模型做绑定



（9）ORM创建数据表
model做数据的存取，以及增删改查等操作
Django并不是直接操作数据库，做了对象的提取，类的名称变成表的名称，类的属性变成表的字段
Django提供自动生成访问数据库的API

from django.db import models
class Person(models.Model):
        id = models.IntegerField(primary_key = True)
        first_name =  models.CharField(max_length = 30)
        last_name = models.CharField(max_length = 30)

对应的sql表
CREATE TABLE myapp_person(
        "id" serial NOT NULL PRIMARY KEY,
        "first_name" varchar(30) NOT NULL,
        "last_name" varchar(30) NOT NULL
);
**通过ORM生成表结构，或者把存在的数据库反向转成ORM
**在Django里会自动创建id，并且自增，设置为主键

$ python manage.py makemigrations   生成中间文件 把对应的class加上必要的功能
$ python manage.py migrate   中间python脚本再转回SQL的表


配置文件（连接mysql）
先安装好pip install pymysql
在__init__.py文件里
import pymysql
pymysql.install_as_MySQLdb()

找到客户端
$ export PATH=$PATH:/  客户端所在的目录 把路径放在这里。
which mysql 查看路径
可以写入配置文件，永久生效

可能存在两个报错，ctrl点击报错提示的文件
注释判断版本的代码
注释关于decode的代码

自动创建后的表就存放在DATABASE指向的数据库，多个数据库要做好指定

$ mysql -uroot -prootroot     用户名跟密码，进入mysql
$ use db2;  进入db2
$ show tables;  查看数据表    存在Django默认创建的表格和自己创建的表格
$ desc index_name;  查看表结构


（10）ORM  API
找到对应的字段，查看官方文档 https://docs.djangoproject.com/
熟悉整数，浮点数，字符，日期等常用的字段属性
字段选项 primary_key，null，default等


操作
做增删改查
找到manag.py所在位置
$ python manage.py shell    进入交互模式
ORM一般操作
$ python manage.py  shell
>>> from index.models import *
>>> n = Name()
>>> n.name='红楼梦'
>>> n.author='曹雪芹'
>>> n.stars=9.6
>>> n.save()    通过sava存入数据

使用ORM框架api实现
增
>>> from index.models import *
>>> Name.objects.create(name='红楼梦', author='曹雪芹', stars='9.6')  默认写入
>>> Name.objects.create(name='活着', author='余华', stars='9.4')

查
>>> Name.objects.get(id=2).name

改
>>> Name.objects.filter(name='红楼梦').update(name='石头记')
 filter 相当于SQL中的where

删 
单条数据
>>> Name.objects.filter(name='红楼梦').delete()
全部数据
>>> Name.objects.all().delete()

其他常用查询
>>> Name.objects.all()[0].name    通过下标的方式指定取值[0]
>>> n = Name.objects.all()     赋值给变量
>>> n[0].name           也是下标取值
>>> n[1].name

通过Query方法
>>> Name.objects.values_list('name')    使用values_list方法
<QuerySet [('红楼梦',), ('活着',)]>   查出QuerySet类型
>>> Name.objects.values_list('name')[0]  下标方式取值
('红楼梦’,)
filter支持更多查询条件
filter(name=xxx, id=yyy)
  
可以引入python的函数（在python环境中）
>>> Name.objects.values_list('name').count()    引用count函数

（11）模版

模版变量 {{ variables }}
从URL获取模版变量 {% url 'urlyear' 2020 %}    去urls.py找
读取静态资源内容 {% static "css/header.css" %}
for遍历标签 {% for type in type_list %}   {% endfor %}
if判断标签 {% if name.type == type.type %}  {% endif %}



（12）






 







（14）urlconf与models配置

在开始Django项目的时候，一种是先实现整个主页，具体细致化开发的时候，通过URLconf再去指定路径给新的app，另一种是开发之前，网站的大体结构已经规划好，创建好项目同时把需要的app也创建，最后也通过URLconf去耦合。


把app跟项目联系起来
首先在settings里注册自己的app ， ***通过path，include才能找到我们的app
在创建的app下也要写好对应的urls.py（默认不存在）文件，文件写好相应的路径。

***在Django项目下的urls.py文件里，写的路径后面要带上/（斜线），才能实现路径拼接


Django项目下的urls.py找到要访问的app，通过include再去加载到app下的urls.py通过对应的路径，再去到指定的view视图
例如：http://ip:port/douban/index


***配置urls 指定好访问的路径，通过path指定好父级目录，之后每一个应用程序中可以写自己的index，不用担心和其他app产生重复

***在指定view视图方面，urls.py文件里通过from . 来限制在当前目录，就不会去找到其他应用下面。
在views.py文件里，定义好函数（通过函数名调用对应的views），通过函数去models取对应的数据，再去调用render，通过template展示

数据获取
除了正向通过ORM创建sql

反向生成ORM  （也是要提前配置好数据库）
通过命令行 $ python manage.py inspectdb > models.py

class Meta:      元数据，不属于任何一个字段的数据
     managed = False    把ORM转成sql的功能关闭 避免造成数据的不安全
     db_table = 't1' 

反向转过来之前，一定要配置好数据库的连接（settings.py文件里）


（15）views视图编写
from .models import T1    导入model，把model引入view视图 T1是反向生成的模型
查询就要用到model对应的管理器 objects（可以改名）

Manager只能通过模型类访问，不是通过模型实例
查看官方文档里 model执行查询里检索对象后的命令，是对model进行的操作，所以要查看model方面的文档
通过objects管理器获取的数据是queryset类型，支持python方法，支持管理器方法

取全部数值
counter = T1.objects.all().count()

取指定的数据
通过比较
queryset = T1.objects.values('sentiment') 去指定的值到queryset是一种固定的写法
condtions={ 'sentiment__gte':0.5} 指定字段 __(双下划线)gte(做判断，大于等于)数值 在这里构建这个类似于字典的表达式
plus = queryset.filter(**condtions).count()                     filter(**kwargs)   传进来的参数类似于字典，要有key有value

通过平均值
聚合函数（高级）
from django.db.models import Avg

star_avg = f" {T1.objects.aggregate(Avg('n_star')) ['n_star__avg']:0.1f}"
         T1.objects.aggregate(Avg('n_star'))   在sql中取平均值的方法  Avg('字段')
         取出来的返回值是 ['字段__avg']    这里类似字典的key
         整条语句 套在一个 f:str中       把value设置为0.1f 表示 小数点后取1位








（16）结合bootstrap
使用bootstrap框架
必须存在的文件
static/css
bootstrap.min.css
static/js
bootstrap.min.js
jquery.js

可以在官网下载需要的模版，
把js、css、字体以及图片放到stati下，把html放到模版里

通过bootstrap下面的组件找到按钮，去查看更多的样式，在官网上找Examples更多自定的页面或其他人写的样式。


栅格系统（自适应）Layout
指定不同的container标签   根据屏幕的尺寸自适应展示（提前设置好每个元素对应的容器，前端框架根据屏幕自动整理排列方式）

假定把屏幕大小当作12格位置，当屏幕足够大的尺寸下，每个位置有3格，可以放四个“卡片”，低于某个尺寸（宽度），就变为每个位置占6格，这样就只能放两个，结果就是根据尺寸大小，展示为横向的4个或者横向的2个，做出了动态适应。
 <div class="col-lg-3 col-md-6">    大尺寸占3格，中尺寸占6格


<div class ="huge"> {{ variables }}  </div>  对应的数值，可以把变量传递进去

侧边栏  这里点击按钮后， <a href="index"> 并不是直接去找index.html，找的不是html页面，而传递的是一个url链接，所以去到urls.py，再去到view视图，然后去vies视图指定的html

***local函数  把当前函数下所有的属性通通加载，并传递给render

{% extends "base_layout.html" %} {% block title %}Welcome{% endblock %} 
{% load static %}
{% block head %}      头部块信息
    {{ block.super }}
    <link rel="stylesheet" href="{% static 'css/timeline.css' %}">
    <link rel="stylesheet" href="{% static 'css/morris.css' %}">
{% endblock %}     这里是结束
{% block content %}

{ % extends     %}  把其他的html内容继承过来
{% load static %}  告知templates模版 static下的文件内容才能使用
   {{ block.super }} 使用这一条语句，继承的html里定义的内容还能保留，不会因为新增的link把父级的模版覆盖掉。如果新增的link跟父级的重复了，那就覆盖父级的标签

result.html 里
<div id="morris-donut-chart" lg05={{ plus }} lt05={{ minus }}></div>

数据从js里传递过去
morris-data.js
$(function() {
    let lg05 = $("#morris-donut-chart").attr('lg05')         传递给js
    let lt05 = $("#morris-donut-chart").attr('lt05')
    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "正向评价",
            value: lg05
        }, {
            label: "负向评价",
            value: lt05
        }],
        resize: true
    });


});


看懂bootstrap框架的基本结构，调整框架，要知道传递变量的位置（通过view视图提取的变量），把变量传递到bootstrap里


（17）阅读Django源代码
去阅读编写优雅的程序，更深入的了解软件，知道Python语言高级特性的使用。

哪一个程序最先运行，就作为Python的入口。

运行manage 有两种方法
一种是 python manage.py  直接运行        就运行main()
另一种 import manage   导包的形式     __name__就变成导入manage对应文件的名字


分析runserver
运行 python manage.py runserver 8080  运行的时候绑定8080端口参数 也能指定ip
①解析对应的参数
②加载runserver文件    其实是个模块文件
③检查INSTALLED_APPS，检查IP端口占用情况，检查ORM设置
④实例化WSGIserver才能接收http请求
⑤动态创建一些类，这些类才是真正接收请求



manage.py

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyDjango.settings')  注册环境变量，Django项目的配置文件

之后try  except 来做一个前期的检查，Django是否安装等

假设运行 python manage.py runserver 8080

from django.core.management import execute_from_command_line


execute_from_command_line(sys.argv) sys.argv接收传递的参数，就会替换为变量(runserver,8080)


D:\Python3\lib\site-packages\django\core\management\__init__.py

def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)同样的argv接收传递来的参数(runserver,8080)
    utility.execute()

查看源码，不仅要跟踪调用的，还要看最上边导入的功能
from collections import OrderedDict, defaultdict  这里导入有序的字典类型（默认是哈希无序的）

from django.conf import settings

from django.core.management.base import (
    BaseCommand, CommandError, CommandParser, handle_default_options,
)


class ManagementUtility:
    """
    Encapsulate the logic of the django-admin and manage.py utilities.
    """
    def __init__(self, argv=None):         传递 (runserver,8080)
        self.argv = argv or sys.argv[:]


    def execute(self):
        subcommand = self.argv[1]     （runserver传递进来）
 
        settings.INSTALLED_APPS          django.conf引入进来的
        
        if subcommand == 'runserver'     （判断传进来的是否为runserver）
     self.autocomplete()

        self.fetch_command(subcommand).run_from_argv(self.argv)
                                          (runserver)                               (8080)



    def fetch_command(self, subcommand):       依然runserver
       
        commands = get_commands()
        try:
            app_name = commands[subcommand]       runserver
       
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, subcommand)
        return klass


def load_command_class(app_name, name):
   
    module = import_module('%s.management.commands.%s' % (app_name, name))      // 导入模块，通过模块的具体路径，不用自带import，可以重新编写函数再去指定路径下的文件
    return module.Command()

runserver.py.Command().run_from_argv(self.argv)  8080

D:\Python3\lib\site-packages\django\contrib\staticfiles\management\commands\runserver.py          做一个接收      run_from_argv(8080)  
D:\Python3\lib\site-packages\django\core\management\commands\runserver.py                                设置初始化属性
D:\Python3\lib\site-packages\django\core\management\base.py

一直找父类，找到execute，做检查，执行还是在第一个runserver.py
        self.execute(*args, **cmd_options)


另一方面
    def get_handler(self, *args, **options):           找WSGI的配置
通过get_handler的父类找到
def get_internal_wsgi_application():            加载WSGI配置
    return WSGIHandler()







理解runserver运行的中间过程，如果某个过程失败，可以通过源代码去定位问题，或者某个过程不够优雅，可做修改  
通过源代码分析理解Python更深层的特性





（总结）
一些总结，提取
urls转到view视图
运行manage.py→settings.py(ROOT_URLCONF = 'MyDjango.urls' 项目) →MyDjango/urls.py → 匹配到空 include下绑定 index程序下的urls网址(在settings.py里面注册好对应的程序)  → index/urls.py 程序（通过include过来的要找到urlpatterns）→ 通过 . 在当前路径下 找到views.py → 找到index函数，把请求传递给函数。
找到视图文件后对请求做处理，再进行返回


网页的路径请求>项目下的urls.py （空就直接访问主页）>到指定的app下的urls.py >对应的vies视图 > 在view视图里定义好获取对应的数据（从models获取）> 调用render通过模版template进行展示


views是展示的具体内容


