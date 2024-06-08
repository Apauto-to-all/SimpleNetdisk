# 混入类
# 实现对文件表的操作
import logging
import os
import traceback


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
    # 插入文件到文件表
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
        INSERT INTO Files(Uname, Fid, Foid, Finame, Fictime, FiKB, Fipath, Copytimes)
        VALUES($1, $2, $3, $4, now(), $5, $6, 1)
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

    # 验证文件是否为用户所有
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
        :return: [
            {
                "uuid": 文件id,
                "name": 文件名,
                "size": 文件大小,
                "type": 文件类型,
                "time": 文件创建时间
            }
        ]
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

    # 获取到父类文件夹下的所有文件id
    async def FileTable_get_all_file_id_from_parent_folder(
        self, username: str, parent_folder: str
    ) -> list:
        """
        获取到父类文件夹下的所有文件id
        :param username: 用户名
        :param parent_folder: 父文件夹id
        :return: 文件id列表，["uuid1", "uuid2", "uuid3"]
        """
        sql = """
        SELECT Fid
        FROM Files
        WHERE Uname = $1 AND Foid = $2 AND Fifdel = false
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, parent_folder)
                return [i.get("fid") for i in result] if result else []
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
    async def FileTable_delete(self, username: str, file_id: str) -> str:
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
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(update_sql, username, file_id)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 还原文件，设置Fifdel为false
    async def FileTable_restore_file(self, username: str, file_id: str):
        """
        还原文件，设置Fifdel为false
        :param username: 用户名
        :param file_id: 文件id
        """
        update_sql = """
        UPDATE Files
        SET Fifdel = false
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(update_sql, username, file_id)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 获取父类文件夹id
    async def FileTable_get_parent_folder_id(self, username: str, file_id: str) -> str:
        """
        获取父类文件夹id
        :param username: 用户名
        :param file_id: 文件id
        :return: 父类文件夹id
        """
        sql = """
        SELECT Foid
        FROM Files
        WHERE Uname = $1 AND Fid = $2
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

    # 重命名文件
    async def FileTable_rename_file(
        self, username: str, file_id: str, new_file_name: str
    ) -> str:
        """
        重命名文件
        :param username: 用户名
        :param file_id: 文件id
        :param new_file_name: 新文件名
        """
        update_sql = """
        UPDATE Files
        SET Finame = $3
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    update_sql, username, file_id, new_file_name
                )  # 执行更新
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 检测文件名，是否存在于父类文件夹中
    async def FileTable_verify_name_only(
        self, username: str, parent_folder: str, file_name: str
    ) -> bool:
        """
        检测文件名，是否存在于父类文件夹中
        :param username: 用户名
        :param parent_folder: 父文件夹id
        :param file_name: 文件名
        :return: 如果文件名存在就返回 True，否则返回 False
        """
        sql = """
        SELECT Finame
        FROM Files
        WHERE Uname = $1 AND Foid = $2 AND Finame = $3
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, parent_folder, file_name)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    # 文件复制次数减一
    async def FileTable_update_cpnums_minus_one(self, username: str, file_path: str):
        """
        文件复制次数减一，如果为0或空就不修改
        :param username: 用户名
        :param file_path: 文件路径
        """
        update_sql = """
        UPDATE Files
        SET Copytimes = Copytimes - 1
        WHERE Uname = $1 AND Fipath = $2 AND Copytimes IS NOT NULL AND Copytimes > 0;
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(update_sql, username, file_path)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 获取到文件的复制次数
    async def FileTable_get_cpnums(self, username: str, file_id: str) -> int:
        """
        获取到文件的复制次数
        :param username: 用户名
        :param file_id: 文件id
        :return: 复制次数
        """
        sql = """
        SELECT Copytimes
        FROM Files
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, file_id)
                return result[0].get("copytimes") if result else 0
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return 0

    # 移动文件到新的文件夹
    async def FileTable_move_file(
        self, username: str, target_folder_id: str, file_id: str
    ):
        """
        移动文件到新的文件夹
        :param username: 用户名
        :param target_folder_id: 目标文件夹id
        :param file_id: 文件id
        """
        update_sql = """
        UPDATE Files
        SET Foid = $3
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    update_sql, username, file_id, target_folder_id
                )
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 复制文件到新的文件夹
    async def FileTable_copy_file(
        self, username: str, target_folder_id: str, file_id: str, new_file_id: str
    ):
        """
        复制文件到新的文件夹
        :param username: 用户名
        :param target_folder_id: 目标文件夹id
        :param file_id: 文件id
        :param new_file_id: 新文件id
        """
        # 首先，获取原文件的路径
        get_path_sql = """
        SELECT Fipath
        FROM Files
        WHERE Uname = $1 AND Fid = $2
        """
        insert_sql = """
        INSERT INTO Files(Uname, Fid, Foid, Finame, Fictime, Fifdel, FiKB, Fipath, Copytimes)
        SELECT Uname, $3, $4, Finame, now(), Fifdel, FiKB, Fipath, Copytimes
        FROM Files
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                # 执行复制操作
                await connection.execute(
                    insert_sql, username, file_id, new_file_id, target_folder_id
                )
                # 获取原文件路径
                file_path = await connection.fetchval(get_path_sql, username, file_id)
                # 更新复制次数，假设 file_path 已经正确获取
                await self.FileTable_update_cpnums_plus_one(username, file_path)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 更新文件的复制次数加一
    async def FileTable_update_cpnums_plus_one(self, username: str, file_path: str):
        """
        更新文件的复制次数加一
        :param username: 用户名
        :param file_path: 文件路径
        """
        update_sql = """
        UPDATE Files
        SET Copytimes = Copytimes + 1
        WHERE Uname = $1 AND Fipath = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(update_sql, username, file_path)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 获取文件的内存大小
    async def FileTable_get_file_size(self, username: str, file_id: str) -> int:
        """
        获取文件的内存大小
        :param username: 用户名
        :param file_id: 文件id
        :return: 文件大小
        """
        sql = """
        SELECT FiKB
        FROM Files
        WHERE Uname = $1 AND Fid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetchval(sql, username, file_id)
                return result if result else 0
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return 0


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
	Copytimes CapacityDomain,
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
