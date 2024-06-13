# 混合类
# 数据库操作缩略图类
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class ShrinkOperate:
    async def ShrinkTable_insert(self, file_type: str, shrink_path: str) -> bool:
        """
        插入缩略图
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO Shrink(Fitype, Spath) VALUES($1, $2)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, file_type, shrink_path)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    # 通过文件类型获取缩略图
    async def ShrinkTable_get_shrink(self, file_type: str) -> str:
        """
        通过文件类型获取缩略图
        :param file_type: 文件类型
        :return: 缩略图路径
        """
        sql = """
        select Spath
        from Shrink
        where Fitype = $1
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetchval(sql, file_type)
                return result if result else ""
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""


"""
--缩略图表
create table Shrink(
	Fitype FitypeDomain primary key,--文件类型
	Spath PathDomain --缩略图路径
);
"""
