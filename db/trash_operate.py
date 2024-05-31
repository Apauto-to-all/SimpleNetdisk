# 混合类
# 数据库垃圾桶表操作类


class TrashOperate:
    async def TrashTable_insert(self):
        """
        插入删除的文件
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO trash(url, code)
        VALUES($1, $2)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql)
                return True if result else False
        except Exception as e:
            return False
