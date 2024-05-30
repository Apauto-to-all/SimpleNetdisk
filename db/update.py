from connection import DatabaseConnectionManager


# 更新
class Update(DatabaseConnectionManager):
    def __init__(self):
        super().__init__()

    # 更新数据
    async def updateData(self, username: str, new_password: str) -> bool:
        """
        更新数据
        :param username: 用户名
        :param new_password: 新密码
        :return: 如果更新数据成功就返回 True，否则返回 False
        """
        sql = """
        UPDATE users
        SET password = $2
        WHERE username = $1
        """
        try:
            async with self.pool.acquire() as connection:  # 获取数据库连接
                result = await connection.execute(
                    sql, username, new_password
                )  # 更新数据
                return True if result else False
        except Exception as e:
            return False
