# 混合类
# 操作数据库中的rcodes注册码表


class RcodesOperate:
    async def RcodesTable_insert(self, rcode: str):
        """
        插入注册码
        :param rcode: 注册码
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO rcodes(rcode)
        VALUES($1)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, rcode)
                return True if result else False
        except Exception as e:
            return False
