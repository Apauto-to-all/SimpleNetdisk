# 混入类
# 实现对文件表的操作
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class FileOperate:
    async def FileTable_insert(self, file_name: str, username: str, parent_folder: str):
        """
        插入文件
        :param file_name: 文件名称
        :param username: 用户名
        :param parent_folder: 父文件夹
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO files(file_name, username, parent_folder)
        VALUES($1, $2, $3)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(
                    sql, file_name, username, parent_folder
                )
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False
