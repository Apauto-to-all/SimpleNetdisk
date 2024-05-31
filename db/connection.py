import asyncio
import asyncpg  # 导入 asyncpg 模块，用于异步访问 PostgreSQL 数据库
from db.folders_operate import FolderOperate  # 导入文件夹操作类
from db.files_operate import FileOperate  # 导入文件操作类
from db.users_operate import UsersOperate  # 导入用户操作类
from db.accesslog_operate import AccessLogOperate  # 导入日志操作类
from db.grades_operate import GradesOperate  # 导入等级操作类
from db.key_operate import KeyOperate  # 导入密钥操作类
from db.rcodes_operate import RcodesOperate  # 导入注册码操作类
from db.shrink_operate import ShrinkOperate  # 导入缩略图操作类
from db.trash_operate import TrashOperate  # 导入回收站操作类

from db.test import Test  # 导入测试类

import config  # 导入配置文件

db_host = config.db_host  # PostgreSQL 数据库主机
db_port = config.db_port  # 数据库端口
database = config.database  # 数据库名称，在里面创建表
db_user = config.connect_user  # 数据库操作用户名
db_password = config.connect_user_password  # 数据库操作用户密码


# 数据库操作类
class DatabaseOperation(
    FolderOperate,
    FileOperate,
    UsersOperate,
    AccessLogOperate,
    GradesOperate,
    KeyOperate,
    RcodesOperate,
    ShrinkOperate,
    TrashOperate,
    Test,
):
    def __init__(self):
        self.pool = None  # 数据库连接池

    # 使用操作用户连接数据库，主要用于查询，更新，插入操作
    async def connectPool(self):
        """
        连接数据库，使用操作用户
        """
        self.pool = await asyncpg.create_pool(  # 创建数据库连接池，可以异步访问数据库
            user=db_user,  # 数据库操作用户名
            password=db_password,  # 数据库操作用户密码
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
