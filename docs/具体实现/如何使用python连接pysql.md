# 使用python连接PostgreSQL数据库

## 安装asyncpg

本次使用的是asyncpg，是一个PostgreSQL数据库异步驱动。

可以用于异步连接PostgreSQL数据库。

```python
pip install asyncpg
```

## 前言
我在db文件夹下创建了一些例子，以及错误处理方法。(主要查看)

按照这个方法，熟悉实现数据库的原理。

大部分的操作都是一样的，只是SQL语句不同。

如果你要实现：[数据库操作函数实现](../数据库操作函数实现.md)，可以参考这个方法。

如果实在无法理解下面的代码，可以实现[数据库操作函数实现](../数据库操作函数实现.md)中的sql语句，然后我来实现python运行sql语句。

## 连接数据库

```python
import asyncpg

"首先为了实现并发操作，我们需要创建一个连接池。"

async def create_pool():
    pool = await asyncpg.create_pool(
        user='postgres',
        password='password',
        database='database',
        host='host',
        port='port'
    )
    return pool
```

## 使用连接池

```python
"然后我们可以通过连接池执行一条SQL语句。"

async def execute(pool):
    async with pool.acquire() as connection:
        sql = """
        SELECT username
        FROM users
        """
        result = await connection.fetch(sql)
        return result
```

## 获取查询结果的数据

```python
"""
结果是一个列表，列表中的每个元素是一个字典。
比如：
result = [{'username': 'admin'}, {'username': 'user'}]
"""

"获取其中的数据"
result = await execute(pool)
for i in result: # 遍历列表，i是字典
    i['username'] # 获取字典中的值，即用户名，也可以用i.get('username')
    print(i['username']) # 输出用户名
```

## 关闭连接池

```python
"如果不使用数据库了，可以关闭连接池。"
await pool.close()
"不过我们搭建的是web后端，一般不需要关闭连接池。"
```

## 我们可以将这些操作封装成一个类

```python
import asyncpg

class Database:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            user='postgres',
            password='password',
            database='database',
            host='host',
            port='port'
        )

    async def execute(self):
        async with self.pool.acquire() as connection:
            sql = """
            SELECT username
            FROM users
            """
            result = await connection.fetch(sql)
            for i in result:
                print(i['username'])
                "或者"
                print(i.get('username'))
    
    async def close_pool(self):
        await self.pool.close()
```

## 如何使用这个类

```python
db = Database() # 实例化一个对象
await db.create_pool() # 创建连接池
await db.execute() # 执行SQL语句
await db.close_pool() # 关闭连接池
```
