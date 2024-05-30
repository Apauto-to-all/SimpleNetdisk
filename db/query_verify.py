from connection import DatabaseConnectionManager


# 查询，验证数据是否存在，返回bool类型
class QueryVerify(DatabaseConnectionManager):
    def __init__(self):
        super().__init__()

    # 查询用户是否存在
    async def queryUsername(self, username: str) -> bool:
        """
        查询数据库中是否存在该用户名
        return: 返回查询结果，如果用户存在就true，否则为false
        """
        sql = """
        SELECT username 
        FROM users 
        WHERE username = $1
        """
        try:
            async with self.pool.acquire() as connection:  # 获取数据库连接
                result = await connection.fetch(sql, username)  # 获取查询结果
                return True if result else False  # 如果查询结果为空，返回 False
        except Exception as e:  # 如果查询失败
            return False
