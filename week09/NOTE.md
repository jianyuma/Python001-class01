学习笔记





偏函数

降低函数调用的难度



URLconf的include
加载子项目当中的urlpatterns
内部做了很多处理，做了更多拆分，使用更加优雅




view视图的请求过程

request 贯穿整个Django的请求
返回 模版渲染用render（功能更强大的Http返回）  返回Http使用HttpResponse 
request是HttpRequest类的对象 （manag.py做各种初始化加载配置文件，WSGI创建HttpRequest）
HttpResponse由开发者创建

        QueryDict  key 是id  值是多个值 用列表存放（传入key完全相同但是值不同）



view视图的响应过程
查看子类源代码
多查看官方文档



view视图完整流程


每次请求都带着实例




自增主键




查询管理器  objects










