from connection import DatabaseConnectionManager


# 查询，获取数据，返回list或dict类型
class QueryGetData(DatabaseConnectionManager):
    def __init__(self):
        super().__init__()

    # 获取所有用户
    async def getAllUsers(self) -> list:
        """
        获取所有用户
        :return: 返回所有用户，使用列表存储，如果查询失败就返回空列表
        """
        sql = """
        SELECT username
        FROM users
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql)
                list = []
                for i in result:
                    list.append(i["username"])
                return list
        except Exception as e:
            return []

    # 获取所有数据
    async def getAllData(self) -> list:
        """
        获取所有数据
        :return: 返回所有数据，使用列表存储，列表每个元素是一个字典，如果查询失败就返回空列表
        """
        sql = """
        SELECT *
        FROM users
        """
        try:
            async with self.pool.acquire() as connection:  # 获取数据库连接
                result = await connection.fetch(sql)  # 获取查询结果
                list = []
                for i in result:
                    dict = {}
                    dict["username"] = i["username"]
                    dict["password"] = i["password"]
                    list.append(dict)
                return list  # 返回所有数据
        except Exception as e:  # 如果查询失败
            return []

    # 获取密码
    async def getPassword(self, username: str) -> str:
        """
        获取密码
        :param username: 用户名
        :return: 返回密码，如果查询失败就返回 None
        """
        sql = """
        SELECT password
        FROM users
        WHERE username = $1
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username)
                password = result[0]["password"]
                return password
        except Exception as e:
            return None
