# 混合类
# 数据库垃圾桶表操作类
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


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
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False
