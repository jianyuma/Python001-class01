学习笔记

（1）pandas
数据清洗

结构化演示练习数据
from sklearn import datasets #引入数据集
先用常见的数据集和pandas结合在一起练习，实际工作中在用生产数据做精细化处理

数据做划分后，就可以用pandas把数据加载后去处理或者用来做机器学习深度学习
生产数据用pandas做数据清洗之后转换成 X和Y 的结构


pandas的基本使用方法  

import pandas as pd                 //
import numpy as np                 //pandas的底层，是一个数学库，做数学分析
import matplotlib as plt           //可视化展示
import os                                 //加载文件

pwd = os.path.dirname(os.path.realpath(__file__))    //双下划线file魔术方法获取当前文件的路径 动态加载路径，但是对交互模式不友好，进入虚拟环境后文件的位置是在虚拟环境可执行命令的位置，
book = os.path.join(pwd,'book_utf8.csv')    //绝对路径+加载的文件
df = pd.read_csv('book_utf8.csv')

##df = pd.read_csv('book_utf8.csv')  //文件在当前可执行的目录，就使用这条代码

df 是pandas里的一中数据类型DataFrame类似Excel中的表格
直接print(df)就能输出df中的全部内容
pandas很智能，会判断屏幕的长度和宽度，输出内容过长会自动做省略处理，会自动加上行号，默认把第一行当作表头

# 筛选标题为"还行"这一列
df['还行']

# 切片方式筛选
# 显示前3行    DataFrame下标是从0开始计数
df[0:3]

# 增加列名
df.columns = ['star', 'vote', 'shorts']

# 显示特定的行、列
df.loc[1:3, ['star']]

# 过滤数据
df['star'] == '力荐'          筛选到的数据为True
df [ df['star'] == '力荐' ]     把筛选为True的再筛选出来

# 缺失数据          删除掉缺失数据
df.dropna()

# 数据聚合
df.groupby('star').sum()

# 创建新列
star_to_number = {
    '力荐' : 5,
    '推荐' : 4,
    '还行' : 3,
    '较差' : 2,
    '很差' : 1
}
df['new_star'] = df['star'].map(star_to_number)


挖坑  分词  理解词性 做出分数理解情感倾向
疑问：对pandas的使用必须以命令行的方式吗

（2）pandas基本数据类型
Series数据结构
当作Excel中的一行或一列，建议当成一列（纵向）
两个基本属性 index 和 value
会自动加上索引，还能更改索引

DataFrame
当作Excel结构中的多行和多列（表格处理）
指定行的索引，列的索引

创建Series
# 从列表创建Series
pd.Series(['a', 'b', 'c'])

# 通过字典创建带索引的Series
s1 = pd.Series({'a':11, 'b':22, 'c':33})
# 通过关键字创建带索引的Series
s2 = pd.Series([11, 22, 33], index = ['a', 'b', 'c'])

# 获取全部索引
s1.index
# 获取全部值
s1.values

# 类型
type(s1.values)    # <class 'numpy.ndarray'>
type(np.array(['a', 'b']))

# 转换为列表
s1.values.tolist()


使用pandas是带有索引的动能，能加快查询的效率
支持map映射


创建DataFrame
# 列表创建dataframe
df1 = pd.DataFrame(['a', 'b', 'c', 'd'])
# 嵌套列表创建dataframe      可以使用多行多列
df2 = pd.DataFrame([
                     ['a', 'b'], 
                     ['c', 'd']
                    ])
# 自定义列索引
df2.columns= ['one', 'two']
# 自定义行索引
df2.index = ['first', 'second']
# 可以在创建时直接指定 DataFrame([...] , columns='...', index='...' )

# 查看索引
df2.columns, df2.index
type(df2.values)

疑问：区分pandas类型和python类型


（3）pandas数据导入  （获取）
Pandas支持大量格式的导入，使用的是read_*()的形式

import pandas as pd
pd.read_excel(r'1.xlsx')

pd.read_csv(r'c:\file.csv',sep='',nrows=10,encoding='utf-8')空格分隔；导入行数；字符
pd.read_table( r'file.txt' , sep = ' ')

pd.read_sql(sql,conn)


#pip install xlrd
#excel底层依赖xlrd包
# 导入excel文件
excel1 = pd.read_excel(r'1.xlsx')           //NaN为空值
# 指定导入哪个Sheet
pd.read_excel(r'1.xlsx',sheet_name = 0)
# 熟悉数据
# 显示前几行
excel1.head(3)

# 行列数量
excel1.shape

# 详细信息
excel1.info()
excel1.describe()


import pymysql             //与数据库结合使用
sql  =  'SELECT *  FROM mytable'
conn = pymysql.connect('ip','name','pass','dbname','charset=utf8')
df = pd.read_sql(sql,conn)


（4）pandas数据预处理 （清洗择菜）
series
#检验序列中是否存在缺失值
x.hasnans

# 将缺失值填充为平均值
x.fillna(value = x.mean())

dataframe
# 前向填充缺失值
df3.isnull().sum() # 查看缺失值汇总
df3.ffill() # 用上一行填充
df3.ffill(axis=1)  # 用前一列填充

# 缺失值删除
df3.info()
df3.dropna()

# 填充缺失值
df3.fillna('无')

# 重复值处理
df3.drop_duplicates()


（5）pandas数据调整（切菜挑选加工）


# 列的选择,多个列要用列表     一定要用列表
df[ ['A', 'C'] ]

# 某几列
df.iloc[:, [0,2]] # :表示所有行，获得第1和第3列

# 行选择
df.loc[ [0, 2] ] # 选择第1行和第3行
df.loc[ 0:2    ] # 选择第1行到第3行

# 比较
df[ ( df['A']<5 ) & ( df['C']<4 )   ]   括号优先级更高 再做与运算

选择行列之后并不会改变原本的DataFrame数据，对于符合要求的需要保存到一个新的变量进行存储。

# 数值替换

# 一对一替换
# 用于单个异常值处理
df['C'].replace(4,40)    //4替换成40

import numpy as np
df.replace(np.NaN, 0)   //空值替换成0

# 多对一替换
df.replace([4,5,8], 1000)    //多个值用列表存放并统一替换成1000

# 多对多替换
df.replace({4:400,5:500,8:800})    //字典的形式各自替换


# 排序
# 按照指定列降序排列
df.sort_values ( by = ['A'] ,ascending = False)     // by关键字    False从大到小 

# 多列排序
df.sort_values ( by = ['A','C'] ,ascending = [True,False]) //True从小到大


# 删除
# 删除列
df.drop( 'A' ,axis = 1)   //  '' 列名为A的一列

# 删除行
df.drop( 3 ,axis = 0)    //  索引为3的一行
**axis是坐标轴，1表示横轴，方向从左到右；0表示纵轴，方向从上到下。当axis=1时，数组的变化是横向的，而体现出来的是列的增加或者减少。
axis的重点在于方向，而不是行和列。

# 删除特定行
df.drop(df [ df['A'] < 4 ].index) 
//df [  df['A'] < 4 ]


# 行列互换   行变列 列变行
df.T
df.T.T


# 索引重塑
df4.stack()          //根据行来做数据透视   堆栈操作 堆叠起来
df4.unstack()      //根据列
df4.stack().reset_index()  //重置索引，根据行做数据透视把空白内容填充，并添加了索引

疑问：在删除特定行的时候，做小于4的删除说到空值也是成立的，是哪方面的成立

（6）pandas基本操作 （炒菜）
计算，行或者列与数字间的计算，列与列之间的计算，用数学的参数来处理数据。

空值没办法计算比较
# 算数运算
# 两列之间的加减乘除
df['A'] + df['C']       //空值为NaN

# 任意一列加/减一个常数值，这一列中的所有值都加/减这个常数值
df['A'] + 5             //空值为NaN

# 比较运算
df['A'] > df ['C']     //空值返回false

# count非空值计数
df.count()

# 非空值每列求和
df.sum()
df['A'].sum()

# mean求均值
# max求最大值
# min求最小值
# median求中位数  
# mode求众数
# var求方差
# std求标准差

Pandas 计算功能操作文档：
https://pandas.pydata.org/docs/user_guide/computation.html#method-summary


（7）pandas分组聚合
（装盘）
df2 = pd.DataFrame(sales)       //导入 变成类似Excel的行列
df2.groupby('type').groups      // 根据type 分组  前半部分为DataFrameGroupBy对象                                                        加上 .groups 属性 取得对应的值
for a, b in df2.groupby('type'):       //取得详细的组信息
    print(a)
    print(b)

（摆盘）
# 聚合后再计算     
df2.groupby('type').count()     //计数
# df2.groupby('Jan').sum()      //总和


# 各类型产品的销售数量和销售总额
df2.groupby('type').aggregate( {'type':'count' , 'Feb':'sum' })  //写成一条语句，aggregate可以调用多个

data.groupby('group').agg('mean')        //用agg调用函数 'mean'是求平均值（合并）
data.groupby('group').mean().to_dict()  //单独一个函数可以直接调用，并且能转成python数据类型
data.groupby('group').transform('mean') //transform处理后结果丢给原来单独的值

# 数据透视表         //类似Excel中的数据透视表，根据实际的需要去做相应的调整
pd.pivot_table(data, 
               values='salary', 
               columns='group', 
               index='age', 
               aggfunc='count', 
               margins=True  
            ).reset_index()


（8）pandas多表拼接（拼盘）
少数时候使用多表拼接，可以参考数据库的操作
merge  模拟数据库理论

# 一对一    一个公共列
pd.merge(data1, data2)

# 多对一    多个公共列，on 指定公共列
pd.merge(data3, data2, on='group')

# 多对多     多个公共列
pd.merge(data3, data2)

# 连接键类型，解决没有公共列问题   
pd.merge(data3, data2, left_on= 'age', right_on='salary')

# 连接方式
# 内连接，不指明连接方式，默认都是内连接
pd.merge(data3, data2, on= 'group', how='inner')
# 左连接 left
# 右连接 right
# 外连接 outer

# 纵向拼接   python用法的连接，在实际中用的更多 把多个字段进行相应的同一，纵向拼接成一个大表
pd.concat([data1, data2])


（9）pandas输出和绘图（上菜）

# 导出为.xlsx文件
df.to_excel( excel_writer = r'file.xlsx')

# 设置Sheet名称
df.to_excel( excel_writer = r'file.xlsx', sheet_name = 'sheet1')

# 设置索引,设置参数index=False就可以在导出时把这种索引去掉
df.to_excel( excel_writer = r'file.xlsx', sheet_name = 'sheet1', index = False)

# 设置要导出的列
df.to_excel( excel_writer = r'file.xlsx', sheet_name = 'sheet1', 
             index = False, columns = ['col1','col2'])


# 设置编码格式       windows  GBK    linux mac android utf-8
enconding = 'utf-8'

# 缺失值处理
na_rep = 0 # 缺失值填充为0

# 无穷值处理
inf_rep = 0

# 导出为.csv文件
to_csv()

# 性能   excel的10倍以上
df.to_pickle('xx.pkl') 
pkl 用来快速读取和保存
 
agg(sum) # 快   使用内置函数更快，尽量使用
agg(lambda x: x.sum()) # 慢

图形

dates = pd.date_range('20200101', periods=12)
df = pd.DataFrame(np.random.randn(12,4), index=dates, columns=list('ABCD'))
练习的时候使用生成随机数

import matplotlib.pyplot as plt
plt.plot(df.index, df['A'], )        //组成横坐标和纵坐标
plt.show()               //展示出来

使用参数增加图形样式
plt.plot(df.index, df['A'], 
        color='#FFAA00',    # 颜色
        linestyle='--',     # 线条样式
        linewidth=3,        # 线条宽度
        marker='D')         # 点标记

# seaborn其实是在matplotlib的基础上进行了更高级的API封装，从而使绘图更容易、更美观
import seaborn as sns
使用现有的工具来绘制

# 绘制散点图
plt.scatter(df.index, df['A'])

# 美化plt
sns.set_style('darkgrid')
plt.scatter(df.index, df['A'])


（10）jieba分词与提取关键词
自然语言处理，语义的分析

分词  jieba工具
import jieba
切分
for string in strings:
    result = jieba.cut(string, cut_all=False) # 精确模式       True为全模式
    print('Default Mode: ' + '/'.join(list(result)))

jieba.cut_for_search()  # 搜索引擎模式


关键词
import jieba.analyse
自动做出权重分析
# 基于TF-IDF算法进行关键词抽取
tfidf = jieba.analyse.extract_tags(text,
topK=5,                   # 权重最大的topK个关键词
withWeight=True)         # 返回每个关键字的权重值
# 基于TextRank算法进行关键词抽取
textrank = jieba.analyse.textrank(text,
topK=5,                   # 权重最大的topK个关键词
withWeight=False)         # 返回每个关键字的权重值

import pprint             # pprint 模块提供了打印出任何Python数据结构的类和方法
pprint.pprint(tfidf)


人工干预    
使用stop_words   把不想要的词屏蔽掉
在stop_words文件里把屏蔽的词写好，把文件放在脚本下的相对路径，做好路径拼接
stop_words=r'2jieba/extra_dict/stop_words.txt'
# stop_words 的文件格式是文本文件，每行一个词语
jieba.analyse.set_stop_words(stop_words)

用户词典    
定义词典
词的内容   权重   词性
写好词典，做好路径
# 自定义词典     加载词典 在cut之前
jieba.load_userdict(user_dict)


# 动态添加词典  不用专门去修改词典，让程序支持
jieba.add_word('极客大学')

# 动态删除词典
jieba.del_word('自定义词')


解决错分
# 关闭自动计算词频
result = jieba.cut(string2, HMM=False)

# 调整分词，合并
jieba.suggest_freq('中出', True)

# 调整词频，分开分词
jieba.suggest_freq(('中','将'), True)


分词处理好之后，词性的标注  做情感分析


（11）SnowNLP情感分析
from snownlp import SnowNLP
分词
s = SnowNLP(text)

# 1 中文分词
s.words

# 2 词性标注 (隐马尔可夫模型)
list(s.tags)

# 3 情感分析（朴素贝叶斯分类器）  0-1  越接近1是越好的
s.sentiments
做情感分析  用购物的评价来训练的
对饭店，购物的评价更准

# 4 拼音（Trie树） 拼音转文字
s.pinyin

# 5 繁体转简体
text3 = '後面這些是繁體字'
s3 = SnowNLP(text3)
s3.han

# 6 提取关键字
s.keywords(limit=5)

# 7 信息衡量
s.tf # 词频越大越重要
s.idf # 包含此条的文档越少，n越小，idf越大，说明词条t越重要

# 8 训练
from snownlp import seg
seg.train('data.txt')
seg.save('seg.marshal')
# 修改snownlp/seg/__init__.py的 data_path 指向新的模型即可

情感分析
还需要深入学习
















