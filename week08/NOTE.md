学习笔记


（1）变量的赋值
变量是可以赋值并且是可以连续赋值的
多个变量同时指向一个常数时，内存地址是相同的

连续赋值，等于最末的值

变量x指向列表，把这个变量x赋值给y，y也等于指向的列表
x指向的列表增加内容，y也会随着x发生变化

整个列表做替换则不会随着变化（标签从这个箱子换到另一个箱子）
指定列表某个元素做替换则会随着变化（标签不变，箱子内容变了）


python一切皆对象
传递的都是对象
有的传递对象本身，有的传递对象的引用

不可变类型（对象本身）
整型 int
浮点型 float
字符串 String
元组  tuple
优点：内存中不管有多少个引用，引用的都是相同的对象，只占一块内存
缺点：当对变量进行运算，改变变量引用的对象的值，必须新创建对象（原先的值占用的内存还在，改变值，重新占用内存，重新给变量赋值）


可变类型（对象引用）传递列表最开头的地址
列表  list
字典  dict
可变类型对值的变化不会产生新的对象，因为内存地址不变，是内容改变，或地址得到扩充

在工作中既可以选择可变又可以不可变，根据性能去考虑选择类型。

纸箱子（内存地址）贴上标签（变量），不可变的数据是都存放在一个箱子里然后贴上了标签，一个箱子可以贴上多个标签（多个变量指向）；可变数据是存放在多个箱子里，这些个箱子绑定在一起，标签只需要贴在第一个箱子上，如果增加新的一排箱子，把标签换到新的这排箱子上，则指定的内容变化了，内存地址也变了，若只是把原本每个箱子里的内容作了替换，但是标签没有变，但是内存地址没有变。


（2）容器序列
从类型定义的角度，序列 （如列表，元组）非序列（如字典） 
序列分类
容器序列：list、tuple、collections.deque等，能存放不同类型的数据。容器序列可以存放不同类型的数据。（如列表里可以放字符串、数字、甚至一个列表、列表中的列表）


扁平序列：str、bytes、bytearray、memoryview（内存视图）、array.array等，存放的是相同类型的数据。扁平序列只能容纳一种类型。


容器序列在深拷贝、浅拷贝问题
（非容器（数字、字符串、元组）类型没有拷贝问题）
列表里的子列表是随着拷贝一起拷贝过去，还是只拷贝列表的引用

import copy
copy.copy(object)
copy.deepcopy(object)

创建新的列表，跟原有的值相等，但是跟原有的列表不相同（不是同一个了）

深拷贝，把列表里所有的值（深入内部）都拷贝（之后原列表改变，拷贝的列表不受影响）
浅拷贝，列表里嵌套的列表值拷贝引用（原列表改变，拷贝受影响）

（3）字典与扩展数据类型
字典的key是可以进行哈希的（不可变的类型）

扩充数据类型collections： 提供加强版的数据类型
collections 官方文档：
https://docs.python.org/zh-cn/3.7/library/collections.html 

namedtuple ——带命名的元组
import collections
Point = collections.namedtuple('Point',['x','y'])
p = Point(11,y=22) 任意传递参数
支持运算

counter  计数器
做统计使用
from collections import Counter
mystring = ['a','b','c','d','d','d','d','c','c','e']
# 取得频率最高的前三个值
cnt = Counter(mystring)
cnt.most_common(3)
cnt['b']

deque 双向队列
from collections import deque
d = deque('uvw')
d.append('xyz')
d.appendleft('rst')

查看官方文档更多的类型，使用时导入对应的库。

魔术方法对运算符进行重载

（4）函数的调用
函数：可调用的对象
调用
作用域
参数
返回值

不带括号就是传递的对象（函数本身），带括号就是执行（传递的返回值）
可以通过类来创建函数，同理带括号跟不带括号是不一样的。


（5）变量作用域
也叫命名空间
高级语言对变量的使用
变量声明
定义类型
初始化
引用

Python和高级语言有很大差别，在模块、类、函数中定义，才有作用域的概念。
一般情况都不需要指定类型，不需要初始化（引用类型特殊功能的时候需要）
不用考虑申请内存跟释放，python自动完成，坏处：传参时候可能传错参数


同名不同作用域，以及上述情况下的查找顺序也会影响程序运行

遵循LEGB    顺序查找
L-Local(function);函数内的名字空间
E-Enclosing function locals;外部嵌套函数的名字空间 (例如closure)  形成闭包
G-Global(module);函数定义所在模块（文件）的名字空间
B-Builtin(Python);Python内置模块的名字空间

# L G
x = 'Global'
def func2():
    x = 'Enclosing'    

    def func3():
        x = 'Local'

        print (x)
    func3()
print(x)     输出  'Global'
func2()              'Loca'


# E
x = 'Global'
def func4():
    x = 'Enclosing'          func5跟Enclosing 结合形成闭包
    def func5():                 在local里没有x，往上去找
        return x
    return func5

var = func4()
print( var() )             'Enclosing'

# B
print (dir (__builtins__) )          B作用域里的变量

避免同名不同作用域的错误
根据LEGB作用域逐层向上去查找，（L->E->G->B）
还要注意程序执行时函数的调用跟变量的位置关系。


（6）函数工具与高阶函数
函数的参数：位置参数，关键字参数等根据实际功能传递不同的参数
动态参数（可变长参数），传入参数的对象类型（字典或序列类型）
*args 一个星接收序列参数，**kargs 两个星接收关键字参数（key value），需要注意传参时的位置顺序，序列参数默认是按照传值的顺序，**kargs优先获取关键字参数

偏函数（当需要把部分参数固定，只需要传递一个参数时）
functools.partial :返回一个可调用的partial对象
使用：  partial(func,*args,**kw)
注：func是必须参数；至少需要一个args或kw参数

高阶函数
高阶：参数是函数、返回值是函数
常见的高阶函数：map（可替代）、reduce（functools中）、filter（可替代）、apply（2.3移除）

Lambda表达式（称作匿名函数）
Lambda只是表达式，不是所有的函数逻辑都能封装进去
 k = lambda x:x+1
 print(k(1))

lambda  后面只能有一个表达式
简单的函数或只有一个语句块的，没有更复杂分支的可以写成lambda表达式，
使用高阶函数的时候一般使用Lambda表达式

 k = lambda  x :    x+1                           
def             k(x):   return x+1        相对应的函数

#  map    做映射，第一个必须是可执行的函数，传入的参数依次去执行
def square(x):
    return x**2

m = map(square, range(10))
next(m)
list(m)
[square(x) for x in range(10)]
dir(m)

# reduce          两两相加，之后跟下一个再相加
# reduce(f, [x1, x2, x3]) = f(f(x1, x2), x3)
from functools import reduce
def add(x, y):
    return x + y

reduce(add, [1, 3, 5, 7, 9])
#25


# filter            做过滤
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))


# 偏函数       固定一个或多个参数
def add(x, y):
    return x + y

import functools
add_1 = functools.partial(add, 1)
add_1(10)

import itertools      自加1的功能
g = itertools.count()
next(g)
next(g)
auto_add_1 = functools.partial(next, g)
auto_add_1()

官方文档
itertools: https://docs.python.org/3/library/itertools.html
functools: https://docs.python.org/3/library/functools.html
operator: https://docs.python.org/3/library/operator.html


（7）闭包
函数返回值，返回的时候有两个关键字，第一个是return，另一个是yield
return返回的对象，不关注类型，基本数据类型就能直接给被赋予者，返回一个函数的对象，变量还可以继续去调用（闭包（装饰器））；yield返回的值通过构成是一个一个查看的方式（迭代器）。

内部函数对外部函数作用域里变量的引用（非全局变量），称内部函数为闭包

同名不同作用域，在闭包里不受外部同名变量的影响（闭包通过__closuer__方法获取）

#查看 编译后函数体保存的局部变量
print(my_line.__code__.co_varnames)
# 编译后函数体保存的自由变量
print(my_line.__code__.co_freevars)
# 自由变量真正的值
print(my_line.__closure__[0].cell_contents)


#####################
# 函数和对象比较有哪些不同的属性
# 函数还有哪些属性
def func(): 
    pass
func_magic = dir(func)

# 常规对象有哪些属性
class ClassA():
    pass
obj = ClassA()
obj_magic = dir(obj)

# 比较函数和对象的默认属性
set(func_magic) - set(obj_magic)


a=100
b=100     这里的a，b不会影响到下面的函数
def line_conf(a, b):       也是闭包 这里是enclosing，local与这里的a,b绑定了
    def line(x):
        return a*x + b
    return line

line1 = line_conf(1, 1)
print(line1(5))

函数里面又定义了一个函数，函数内外部不太相关，
外部函数是对函数做修改，做装饰（定义某些功能的初次定义），内部函数去执行得到结果；在定义的时候就设置好模式，定义态。


def counter(start=0):
   count=[start]
   def incr():
       count[0]+=1
       return count[0]
   return incr

c1=counter(10)

print(c1())
# 结果：11


 nonlocal访问外部函数的局部变量
# 注意start的位置，return的作用域和函数内的作用域不同
def counter2(start=0):
    def incr():
        nonlocal start       把作用域扩大，获取到外部的start
        start+=1
        return start
    return incr
c1=counter2(5)
print(c1())

好处：在闭包下，创建多个计数器互不干扰



（8）装饰器
对原有的对象进行装饰（添加一系列的装饰）
增强而不改变原有函数
装饰器强调函数的定义态而不是运行态

@decorate
def target():
    print('do something')


def target():
    print('do something')
target = decorate(target)

target 表示函数
target() 表示函数执行
new = func 体现“一切皆对象”，函数也可以被当做对象进行赋值


被装饰函数带参数
被装饰函数带不定长参数
被装饰函数带返回值

PEP318

def decorate(func):
    print('running in modlue')
    def inner():
        return func()
    return inner

@decorate
def func2():
    pass
个人理解：装饰器 是@函数名（已定义好的函数），放置在将要定义的函数前，就能直接引用之前定义过的函数，然后运行后返回的值用来给被装饰的函数。

用在flask框架中
让代码更优雅
# Flask 的装饰器是怎么用的？
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
   return '<h1>hello world </h1>'

# 注册
@route('index',methods=['GET','POST'])
def static_html():
    return  render_template('index.html')


# 包装
def html(func):
    def decorator():
        return f'<html>{func()}</html>'
    return decorator

def body(func):
    def decorator():
        return f'<body>{func()}</body>'
    return decorator

@html
@body           套了两层装饰器，先套body，再套html  最后返回的是@html的值
def content():
    return 'hello world'

content()


装饰器在模块导入的时候会自动运行
默认使用的装饰器，返回的函数已经被替换成了装饰器里的装饰函数



（9）被装饰函数带参数和返回值的处理

被装饰函数名传递给装饰器
装饰器函数名传递给被装饰函数
# 被修饰函数带参数
def outer(func):
    def inner(a,b):
        print(f'inner: {func.__name__}')
        print(a,b)
        func(a,b)
    return inner

@outer
def foo(a,b):
    print(a+b)
    print(f'foo: {foo.__name__}')
        
foo(1,2)

inner:foo
1 2
3
foo:inner


# 被修饰函数带不定长参数  
用*和**来接收不定长的参数
def outer2(func):
    def inner2(*args,**kwargs):
        func(*args,**kwargs)
    return inner2

@outer2
def foo2(a,b,c):
    print(a+b+c)
    
foo2(1,3,5)

# 被修饰函数带返回值
装饰器里也要有对应的接收返回
def outer3(func):
    def inner3(*args,**kwargs):
        ###   增加功能
        ret = func(*args,**kwargs)     接收的参数处理后给ret
        ###   增加功能  不用考虑返回值
        return ret               接收ret的返回
    return inner3

@outer3
def foo3(a,b,c):
    return (a+b+c)
    
print(foo3(1,3,5))

装饰器带参数和返回值
# 装饰器带参数 

def outer_arg(bar):
    def outer(func):
        def inner(*args,**kwargs):
            ret = func(*args,**kwargs)
            print(bar)
            return ret
        return inner
    return outer

# 相当于outer_arg('foo_arg')(foo)()
@outer_arg('foo_arg')
def foo(a,b,c):
    return (a+b+c)
    
print(foo(1,3,5))

装饰器堆叠   需要注意内外层套用顺序

@classmethod
@synchronized(lock)
def foo(cls):
    pass

def foo(cls):
    pass
foo2 = synchronized(lock)(foo)
foo3 = classmethod(foo2)
foo = foo3

（10）python内置装饰器

# functools.wraps
# @wraps接受一个函数来进行装饰
# 并加入了复制函数名称、注释文档、参数列表等等的功能
# 在装饰器里面可以访问在装饰之前的函数的属性
# @functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
# 用于在定义包装器函数时发起调用 update_wrapper() 作为函数装饰器。 
# 它等价于 partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)。

用了wraps传递给装饰器的函数，处理之后传出来的还是原来的函数，不会被装饰器内部函数替换掉

from time import ctime,sleep
from functools import wraps
def outer_arg(bar):
    def outer(func):
        # 结构不变增加wraps
        @wraps(func)
        def inner(*args,**kwargs):
            print("%s called at %s"%(func.__name__,ctime()))
            ret = func(*args,**kwargs)
            print(bar)
            return ret
        return inner
    return outer

只在结构里增加wraps，其他结构不变，对装饰器的使用还是照常使用 
例如在flask里进行登录验证，验证后依然传出原来的函数
做日志记录，记录之后都能返回原来的名称

# functools.lru_cache
# 《fluent python》的例子
# functools.lru_cache(maxsize=128, typed=False)有两个可选参数
# maxsize代表缓存的内存占用值，超过这个值之后，就的结果就会被释放
# typed若为True，则会把不同的参数类型得到的结果分开保存
import functools
@functools.lru_cache()

用了lru_cache把多次调用的函数做一个缓存，加快处理速度。


（11）类装饰器
python2.6后开始添加类装饰器

引入 __init__
要写__call__作为外层函数
__call__ 要将self作为第一个参数

class MyClass(object):
    def __init__(self, var='init_var', *args, **kwargs):
        self._v = var
        super(MyClass, self).__init__(*args, **kwargs)
    
    def __call__(self, func):
        # 类的函数装饰器
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            func_name = func.__name__ + " was called"
            print(func_name)
            return func(*args, **kwargs)
        return wrapped_function

另一个实例

class Count(object):
    def __init__(self,func):
        self._func = func
        self.num_calls = 0    一些属性前面要加上self
    
    def __call__(self, *args, **kargs):
        self.num_calls += 1
        print(f'num of call is {self.num_calls}')
        return self._func(*args, **kargs)      返回时依然跟上self

@Count
def example():
    print('hello')


装饰器装饰类，对类中的某一个函数做装饰，语法糖写在类的上面


（12）装饰器官方文档

# 向一个函数添加属性
def attrs(**kwds):
    def decorate(f):
        for k in kwds:
            setattr(f, k, kwds[k])
        return f
    return decorate

@attrs(versionadded="2.2",
       author="Guido van Rossum")
def mymethod(f):
    pass


# 函数参数观察器
import functools
def trace(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        print(f, args, kwargs)
        result = f(*args, **kwargs)
        print(result)
    return decorated_function
@trace
def greet(greeting, name):
    return '{}, {}!'.format(greeting, name)

greet('better','me')


# Python3.7 引入 Data Class  PEP557
from dataclasses import dataclass
@dataclass
class MyClass:
    var_a: str             str 这里是提示类型作用
    var_b: str

var_1 = MyClass('x','y')    判断相等
var_2 = MyClass('x','y')

# 存在的问题: var_a var_b不能作为类属性访问


了解官方PEP，可以学习新的功能，知道过期动能，及时对python的变化做更新。


（13）对象协议与鸭子类型
协议：通信的标准

对象协议，需要使用某个方法，然后能够支持，就满足了协议（比如调用字典，对方有这个方法，就满足了协议）

python当中实现对象协议，用魔术方法实现，根据调用方决定，满足调用就返回正确的结果，不满足直接告诉调用类型出错。
通俗的讲，鸭子类型，看到个动物，叫起来像鸭子，走路像鸭子，就认为是鸭子。python中，按照字典方式调用，能够返回，就认为你是字典
定义的对象没有初始化类型，甚至能够在运行的过程中改变类型。

需要学习常用的魔术方法
  容器类型协议
  __str__ 打印对象时，默认输出该方法的返回值
  __getitem__、__setitem__、delitem__ 字典索引操作
  __iter__ 迭代器
  __call__ 可调用对象协议
  比较大小协议
  __eq__
  __gt__
  描述符协议和属性交互协议
  __get__
  __set__
  可哈希对象
  __hash__
假如用字典、字符串等数据类型能解决的就用原生数据类型，如果解决不了，需要自己定义，自己编写的东西，要向标准的数据类型对齐。这样python会越写越简单

上下文管理器
with 上下文表达式的用法
底层是使用 __enter__() __exit__() 实现上下文管理器

代码样例
class Foo(object):
    # 用与方法返回
    def __str__(self):
        return '__str__ is called'

    # 用于字典操作
    def __getitem__(self, key):
        print(f'__getitem__ {key}') 
    
    def __setitem__(self, key, value):    这里要参数设定value，因为要传key传value
        print(f'__setitem__ {key}, {value}')
    
    def __delitem__(self, key):
        print(f'__delitem__ {key}')

    # 用于迭代
    def __iter__(self):
        return iter([i for i in range(5)])

# __str__
bar = Foo()
print(bar)         打印后默认输出返回值

# __XXitem__
bar['key1']        取value
bar['key1']='value1'   改value
del bar['key1']   删除value

# __iter__
for i in bar:     通过迭代循环输出
    print(i)

FormatString

firstname = 'yin'
lastname = 'wilson'
print('Hello, %s %s.' % (lastname, firstname))    要考虑类型考虑值
print('Hello, {1} {0}.'.format(firstname, lastname))         位置要对应
print(f'Hello, {lastname} {firstname}.') 通过f-string  可以直接使用，直接填充通过花括号{}替换

class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):        正常输出调用
        return f'hello, {self.first_name} {self.last_name}.'

    def __repr__(self):   程序对象之间同信调用
        return f'hello, {self.first_name} {self.last_name}.'


type hint 类型注解
！！！只是类型的注解，并不是类型的强制要求，使用其他类型调用也是可以的

def func(text: str, number: int) -> str:                : （空格）类型的形式来写注解
    return text * number                                     -> 类型：   表示返回的类型

func('a', 5)


（14）yield
返回后，函数会暂停
创造新的类型生成器（generator），返回可迭代的对象

1.在函数中使用yield关键字，可以实现生成器
2.生成器可以让函数返回可迭代对象。
3.yield和return不同，return返回后，函数状态终止，yield保持函数的执行状态，返回后，函数回到之前保存的状态继续执行。
4.函数被yield会暂停，局部变量也会被保存。
5.迭代器终止时，会抛出StopIteration异常。


生成器-2
[ i for i in range(0,11)]

(i for i in range(0,11))

gennumber = ( i for i in range(0,11))   生成器赋值变量
next(gennumber)  等于 gennumber.__next__()
print(list(gennumber))
结论一：列表是可迭代对象，但不是迭代器，不可next()
[] 换成() 不再是列表，是生成器 既可以iter()又可以next()取值



实现next又实现for in，即叫做生成器，又叫做迭代器（实现完整迭代器协议）
只实现for in叫做可迭代对象
（next()方法底层就是__next__魔术方法，同样的iter()方法也是）

Iterables（可迭代）：包含__getitem__()或__iter__()方法的容器对象
Iterator（迭代器）：包含next()和__iter__()方法
Generator（生成器）：包含yield语句函数
（Iterator包含Generator，Iterables包含Iterator）

结论二：生成器实现完整的迭代器协议

判断是否有某功能
alist = [1, 2, 3, 4, 5]
hasattr( alist, '__iter__' )  # True       
hasattr( alist, '__next__' )  # False

# 类实现完整的迭代器协议

class SampleIterator:
    def __iter__(self):
        return self

    def __next__(self):
        # Not The End
        if ...:
            return ...
        # Reach The End
        else:
            raise StopIteration

# 函数实现完整的迭代器协议
def SampleGenerator():
    yield ...
    yield ...
    yield ...  # yield语句
# 只要一个函数的定义中出现了 yield 关键词，则此函数将不再是一个函数，
# 而成为一个“生成器构造函数”，调用此构造函数即可产生一个生成器对象。


# check iter   做检查
def check_iterator(obj):
    if hasattr( obj, '__iter__' ):  
        if hasattr( obj, '__next__' ):
            print(f'{obj} is a iterator') # 完整迭代器协议
        else:
            print(f'{obj} is a iterable') # 可迭代对象
    else:
        print(f'{obj} can not iterable') # 不可迭代

def func1():
    yield range(5) 
check_iterator(func1())             执行后才是生成器

# 结论三： 有yield的函数是迭代器，执行yield语句之后才变成生成器构造函数



（15）迭代器注意事项

无限迭代器

# itertools的三个常见无限迭代器
import itertools

count = itertools.count()  # 计数器
next(count)

###############
cycle = itertools.cycle( ('yes', 'no') ) # 循环遍历
next(cycle)

##############
repeat = itertools.repeat(10, times=2)  # 重复
next(repeat)

################
# 有限迭代器
for j in itertools.chain('ABC',[1, 2, 3]) :    加了chain之后输出是A B C 1 2 3
    print(j)                                                 不是'ABC',[1,2,3]

# Python3.3 引入了 yield from 
# PEP-380
def chain(*iterables):
    for it in iterables:
        for i in it:
            yield i

s = 'ABC'
t = [1, 2, 3]
list(chain(s, t))

def chain2(*iterables):
    for i in iterables:
        yield from i    !!# 替代内层循环

list(chain2(s, t))

通过字典产生的迭代器，
# RuntimeError: 字典进行插入操作后，字典迭代器会立即失效
列表产生的迭代器
# 尾插入操作不会损坏指向当前元素的List迭代器,列表会自动变长

迭代器一旦耗尽，就永久损坏，只能取出来一次
不同于列表可以重复取值
  

（16）yield表达式
作为表达式为变量传递参数，既可以输出又可以输入。

next()输出    send()做输入参数
yield可以暂停程序，通过输入输出操作暂停跟开始程序
def jumping_range(up_to):
    index = 0
    while index < up_to:
        jump = yield index
        print(f'jump is {jump}')
        if jump is None:
            jump = 1   # next() 或者 send(None)
        index += jump 
        print(f'index is {index}')

if __name__ == '__main__':
    iterator = jumping_range(5)
    print(next(iterator)) # 0
    print(iterator.send(2)) # 2
    print(next(iterator)) # 3
    print(iterator.send(-1)) # 2
    for x in iterator:
        print(x) # 3, 
通过这种模式来达到协程


（17）协程简介
提高IO密集型程序的工作效率。遇到IO操作，切换到其他部分，收到IO准备就绪再恢复操作。

协程和线程的区别

协程是异步的，线程是同步的
协程是非抢占式的，线程是抢占式的
协程是主动调度的，线程是被动调度的
协程可以暂停函数的执行，保留上一次调用时的状态，是增强型生成器
协程是用户级的任务调度，线程是内核级的任务调度
协程适用于IO密集型程序，不适用于CPU密集型程序的处理

异步编程
# python3.5 增加async await  取代yield from方式
import asyncio
async def py35_func():                 async是关键字
    await sth()                                await是关键字

# 注意： await 接收的对象必须是awaitable对象
# awaitable 对象定义了__await__()方法
# awaitable 对象有三类
# 1 协程 coroutine
# 2 任务 Task
# 3 未来对象 Future

理解事件循环



#################
# 协程调用过程： 
# 调用协程时，会被注册到ioloop，返回coroutine对象
# 用ensure_future 封装为Future对象
# 提交给ioloop

# 官方文档
# https://docs.python.org/zh-cn/3/library/asyncio-task.html


（18）aiohttp简介


# Web Server
from aiohttp import web









（总结）
python一切皆对象。
纸箱子（内存地址）贴上标签（变量）。
容器传递对象的引用。
创建新的列表，跟原有的值相等，但是跟原有的列表不相同（不是同一个了）。
一般情况都不需要指定类型，不需要初始化。
（用函数的对象名称还是取函数执行后的值
变量作用域
参数
返回值）