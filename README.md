# annosSQL

#### 介绍
annosSQL是一个基于python实现对mysql、oracle、sqllite数据库交互库，基础是基于对pymysql等库的封装，其用法有些特别。annosSQL中实现了一种缓存算法（通过LRU算法实现），对于近期相同sql的查询，
会优先从缓存获取，当缓存空间不存在该数据时，再次访问数据库。

#### 安装教程
```shell
pip install annosSQL
```

#### 使用说明

1. 使用案例
```python
from annosSQL.Innos.Interface import Interface, Handler
from annosSQL.Donos.doconn import Connection
from annosSQL.Donos.dosql import execute

@Interface()
class T4:
    #配置处理器，这是入口，是必须
    @Handler()
    def hand(self) -> list: pass

    #配置连接池
    @Connection(driver="mysql", host="127.0.0.1", user="root", password="123456", port=3306, database="czh")
    def conn(self) -> any: pass

    '''
    查询所有数据，p1方法不能有任何的形参变量，必须是空函数，'->'箭头后面跟的是返回值类型，'list'或'dict'或'tuple'都行
    这里返回list数据类型
    '''
    @execute(sql="select * from user_copy1")
    def p1(self) -> list: pass

    @execute(sql="select * from user_copy1")
    def p2(self) -> dict: pass

    @execute(sql="select * from user_copy1")
    def p3(self) -> tuple: pass

    '''
    占位符使用 {}/#{}/%s,
    条件查询时，函数的形参必须带类型，如s1方法里的id必须写出：id:int
    '''
    # {}占位符是通过str().format()实现的，此时，函数形参的位置十分重要，它将影响sql的条件的正确性
    @execute(sql="select * from user_copy1 where id={}")
    def s1(self,id:int) -> list: pass
    # #{}占位符的基本形式如下：#{1}，通过#{}大括号里的数值来定位绑定到函数的形参
    @execute(sql="select * from user_copy1 where id=#{1}")
    def s2(self, id: int) -> dict: pass
    # %s 多行占位符 支持数据多行数据类型：列表与元组
    @execute(sql="select * from user_copy1 where id=%s")
    def s3(self, id: int) -> tuple: pass

    '''
    快捷符的使用：A(select)
    '''
    @execute(sql="A(select) user_copy1")
    def a1(self) -> tuple: pass



if __name__=='__main__':
    t4=T4()
    t4.hand() #调用入口
    print('p1返回的数据：')
    p1=t4.p1()
    print(p1)

    print('p2返回的数据：')
    p2 = t4.p2()
    print(p2)

    print('p3返回的数据：')
    p2 = t4.p2()
    print(p2)

    print('s1返回的数据：')
    s1 = t4.s1(1)
    print(s1)

    print('s2返回的数据：')
    s2 = t4.s2(1)
    print(s2)

    print('s3返回的数据：')
    s3 = t4.s2(1)
    print(s3)

    print('a1返回的数据：')
    a1 = t4.a1()
    print(a1)    

```
2. 运行结果
```text
p1返回的数据：
[[1, 'chx', '123455', '1'], [2, 'czh', '123456', '2']]
p2返回的数据：
[{'id': 1, 'user': 'chx', 'password': '123455', 'z': '1'}, {'id': 2, 'user': 'czh', 'password': '123456', 'z': '2'}]
p3返回的数据：
((1, 'chx', '123455', '1'), (2, 'czh', '123456', '2'))
s1返回的数据：
[[1, 'chx', '123455', '1']]
s2返回的数据：
[{'id': 1, 'user': 'chx', 'password': '123455', 'z': '1'}]
s3返回的数据：
[{'id': 1, 'user': 'chx', 'password': '123455', 'z': '1'}]
a1返回的数据：
((1, 'chx', '123455', '1'), (2, 'czh', '123456', '2'))
```
3. xxxx
#### 其他说明
> #{} %s {}
    # #{}、 {} 普通占位符
    # %s 多行占位符 支持数据多行数据类型：列表与元组
    # select * from  ->  A(select) user
    # insert into table values(S{,}[])
    # insert into table values(C{})
    # insert into table values(L{})
    # insert into table values(T{%s,%s})

