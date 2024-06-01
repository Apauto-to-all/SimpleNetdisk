# 混合类
# 数据库操作缩略图类
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


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
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False
