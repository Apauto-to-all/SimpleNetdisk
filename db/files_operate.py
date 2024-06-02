# 混入类
# 实现对文件表的操作
import logging
import traceback
import asyncpg

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
            return

    async def FileTable_verify(self, username: str, file_id: str) -> bool:
        """
        验证文件是否存在
        :param username: 用户名
        :param file_id: 文件id
        :return: 如果文件存在就返回 True，否则返回 False
        """
        sql = """
        SELECT Uname
        FROM Files
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, file_id)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False
    
    


"""
--文件表
create table Files(
	Uname UnameDomain,--用户名
	Fid FidDomain,--文件id
    Foid FidDomain,--文件夹id
	Finame FnameDomain,--文件名
	Fictime FctimeDomain,--文件创建时间
	Fifdel ifDomain,--文件是否被删除
	FiKB CapacityDomain,--文件大小
	Fipath PathDomain,--文件路径
	primary key (Uname, Fid),
    foreign key (Uname, Foid) references Folders(Uname, Foid),
    foreign key (Uname) references Users(Uname)
);
"""
