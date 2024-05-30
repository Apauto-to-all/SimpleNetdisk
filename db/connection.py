import config  # 导入全局配置文件
import asyncpg  # 导入 asyncpg 模块，用于异步访问 PostgreSQL 数据库

db_host = config.db_host  # PostgreSQL 数据库主机
db_port = config.db_port  # 数据库端口
database = config.database  # 数据库名称，在里面创建表


# 数据库连接
class DatabaseConnectionManager:
    def __init__(self):
        self.pool = None  # 数据库连接池

    # 使用操作用户连接数据库，主要用于查询，更新，插入操作
    async def connectPool(self):
        """
        连接数据库，使用操作用户
        """
        self.pool = await asyncpg.create_pool(  # 创建数据库连接池，可以异步访问数据库
            user=config.connect_user,  # 操作用户
            password=config.connect_user_password,  # 查询用户的密码
            database=database,  # 数据库名称
            host=db_host,  # 数据库主机
            port=db_port,  # 数据库端口
        )

    # 创建表
    async def createTable(self):
        """
        创建表
        :return: 如果创建表成功就返回 True，否则返回 False
        """
        sql = """
        CREATE TABLE users(
            username VARCHAR(255),
            password VARCHAR(255),
            PRIMARY KEY(username)
        )
        """
        try:
            async with self.pool.acquire() as connection:

                result = await connection.execute(sql)
                return True if result else False
        except Exception as e:  # 如果创建表失败
            return False

    # 关闭数据库连接
    async def close(self):
        """
        关闭数据库连接
        """
        try:
            await self.pool.close()
        except Exception as e:
            pass
