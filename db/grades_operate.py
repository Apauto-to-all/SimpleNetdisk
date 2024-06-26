# 混合类
# 等级表的操作
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class GradesOperate:
    async def GradesTable_insert(self, grade: str):
        """
        插入等级
        :param grade: 等级
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO grades(grade)
        VALUES($1)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, grade)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False
