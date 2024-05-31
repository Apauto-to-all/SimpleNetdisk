# 混合类
# 实现ip+请求头日志记录


class AccessLogOperate:
    async def AccessLogTable_insert(self, ip: str, headers: str):
        """
        插入日志
        :param ip: ip地址
        :param headers: 请求头
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO accesslog(ip, headers)
        VALUES($1, $2)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, ip, headers)
                return True if result else False
        except Exception as e:
            return False
