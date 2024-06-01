# 混入类，实现对文件夹表的操作
# 实现对文件夹表的操作
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class FolderOperate:
    async def FolderTable_insert(
        self, folder_name: str, username: str, parent_folder: str
    ):
        """
        插入文件夹
        :param folder_name: 文件夹名称
        :param username: 用户名
        :param parent_folder: 父文件夹
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO folders(folder_name, username, parent_folder)
        VALUES($1, $2, $3)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(
                    sql, folder_name, username, parent_folder
                )
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False
