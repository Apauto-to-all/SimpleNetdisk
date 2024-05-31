# 混合类
# 操作用户表的类


class UsersOperate:
    async def UsersTable_insert(self, username: str, password: str):
        """
        插入用户
        :param username: 用户名
        :param password: 密码
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO users(username, password)
        VALUES($1, $2)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, username, password)
                return True if result else False
        except Exception as e:
            return False
