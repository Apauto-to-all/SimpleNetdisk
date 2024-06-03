# 混入类
# 实现对文件表的操作
import logging
import os
import traceback
import asyncpg


# 获取日志记录器
logger = logging.getLogger(__name__)


# 从文件名中获取文件类型
async def get_file_type(file_name: str) -> str:
    """
    从文件名中获取文件类型
    :param file_name: 文件名
    :return: 文件类型
    """
    file_type = os.path.splitext(file_name)[-1]  # 获取文件类型
    return file_type if file_type else "unknown"  # 返回文件类型


class FileOperate:
    async def FileTable_insert(
        self,
        username: str,
        file_id: str,
        parent_folder: str,
        file_name: str,
        file_size: int,
        file_path: str,
    ):
        """
        插入文件到文件表
        :param username: 用户名
        :param file_id: 文件id
        :param parent_folder: 父文件夹id
        :param file_name: 文件名
        :param file_size: 文件大小
        :param file_path: 文件路径
        """
        sql = """
        INSERT INTO Files(Uname, Fid, Foid, Finame, Fictime, FiKB, Fipath)
        VALUES($1, $2, $3, $4, now(), $5, $6)
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    sql,
                    username,
                    file_id,
                    parent_folder,
                    file_name,
                    file_size,
                    file_path,
                )
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

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

    # 从父类文件夹文件夹id中获取文件
    async def FileTable_get_files_from_parent_folder(
        self, username: str, parent_folder: str
    ) -> list:
        """
        从父类文件夹文件夹id中获取文件
        :param username: 用户名
        :param parent_folder: 父文件夹id
        :return: 文件列表
        """
        sql = """
        SELECT Fid, Finame, FiKB, Fictime
        FROM Files
        WHERE Uname = $1 AND Foid = $2 AND Fifdel = false
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, parent_folder)
                files_list = []
                for i in result:
                    files_list.append(
                        {
                            "uuid": i.get("fid"),
                            "name": i.get("finame"),
                            "size": i.get("fikb"),
                            "type": await get_file_type(i.get("finame")),
                            "time": i.get("fictime"),
                        }
                    )
                return files_list
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return []

    # 如果文件的父级文件夹被加密，返回父级文件夹id，否则返回空字符串
    async def FileTable_get_lock_parent_folder_id(
        self, username: str, file_id: str
    ) -> str:
        """
        如果文件的父级文件夹被加密，返回父级文件夹id，否则返回空字符串
        :param username: 用户名
        :param file_id: 文件id
        :return: 父级文件夹id
        """
        sql = """
        SELECT Files.Foid
        FROM Files
        INNER JOIN Folders ON Files.Foid = Folders.Foid
        WHERE Files.Uname = $1 AND Files.Fid = $2 AND Folders.Fopasswd IS NOT NULL
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, file_id)
                return result[0].get("foid") if result else ""
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""

    # 获取文件名和文件路径
    async def FileTable_get_name_path(self, username: str, file_id: str) -> dict:
        """
        获取文件名和文件路径
        :param username: 用户名
        :param file_id: 文件id
        :return: 文件名和文件路径
        """
        sql = """
        SELECT Finame, Fipath
        FROM Files
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, file_id)
                return (
                    {
                        "file_name": result[0].get("finame"),
                        "file_path": result[0].get("fipath"),
                    }
                    if result
                    else {}
                )
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return {}

    # 删除文件，设置Fifdel为true，获取父级文件夹id
    async def FileTable_delete_get_parent_folder_id(
        self, username: str, file_id: str
    ) -> str:
        """
        删除文件，设置Fifdel为true，获取父级文件夹id
        :param username: 用户名
        :param file_id: 文件id
        :return: 父级文件夹id
        """
        update_sql = """
        UPDATE Files
        SET Fifdel = true
        WHERE Uname = $1 AND Fid = $2
        """
        select_sql = """
        SELECT Foid
        FROM Files
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(update_sql, username, file_id)
                result = await connection.fetch(select_sql, username, file_id)
                return result[0].get("foid") if result else ""
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""

    # 重命名文件，并返回父类文件夹id
    async def FileTable_rename_file_get_parent_folder_id(
        self, username: str, file_id: str, new_file_name: str
    ) -> str:
        """
        重命名文件，并返回父类文件夹id
        :param username: 用户名
        :param file_id: 文件id
        :param new_file_name: 新文件名
        :return: 父类文件夹id
        """
        update_sql = """
        UPDATE Files
        SET Finame = $3
        WHERE Uname = $1 AND Fid = $2
        """
        select_sql = """
        SELECT Foid
        FROM Files
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(update_sql, username, file_id, new_file_name)
                result = await connection.fetch(select_sql, username, file_id)
                return result[0].get("foid") if result else ""
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""


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
"""
--文件夹表
create table Folders(
	Uname UnameDomain,--用户名
	Foid FidDomain,--文件夹id
	Faid FidDomain,--父级文件夹id
	Foname FnameDomain,--文件夹名
	Foctime FctimeDomain,--文件夹创建时间
	Foifdel ifDomain,--文件夹是否被删除
	Relation PathDomain,--当前文件夹隶属：文件夹的层级关系
	Fopasswd FopasswdDomain,--文件夹密码
	primary key (Uname, Foid),
	foreign key (Uname) references Users(Uname)
);
"""
