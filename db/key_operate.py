# 混合类
# 密匙表的操作
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class KeyOperate:
    async def KeyTable_insert(self, key: str):
        """
        插入密匙
        :param key: 密匙
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO keys(key)
        VALUES($1)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, key)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False
