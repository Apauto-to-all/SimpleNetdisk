# 混合类
# 数据库操作缩略图类


class ShrinkOperate:
    async def ShrinkTable_insert(self):
        """
        插入缩略码
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO shrinks(url, code)
        VALUES($1, $2)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql)
                return True if result else False
        except Exception as e:
            return False
