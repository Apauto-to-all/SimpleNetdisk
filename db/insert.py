from connection import DatabaseConnectionManager


# 插入数据
class Insert(DatabaseConnectionManager):
    def __init__(self):
        super().__init__()

    # 插入一些数据
    async def insertData(self, username: str, password: str) -> bool:
        """
        插入数据
        :param username: 用户名
        :param password: 密码
        :return: 如果插入数据成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO users(username, password)
        VALUES($1, $2)
        """
        try:
            async with self.pool.acquire() as connection:  # 获取数据库连接
                result = await connection.execute(sql, username, password)  # 插入数据
                return True if result else False
        except Exception as e:  # 如果插入数据失败
            return False
