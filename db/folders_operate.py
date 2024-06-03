# 混入类，实现对文件夹表的操作
# 实现对文件夹表的操作
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class FolderOperate:

    async def FolderTable_insert(
        self,
        username: str,
        new_folder_id: str,
        parent_folder_id: str,
        folder_name: str,
    ):
        """
        插入文件夹
        :param username: 用户名
        :param new_folder_id: 新文件夹id
        :param parent_folder_id: 父文件夹id
        :param folder_name: 文件夹名
        """
        sql_select_parent_folder_relation = """
        SELECT Relation
        FROM folders
        WHERE Uname = $1 AND Foid = $2
        """
        sql = """
        INSERT INTO folders(Uname, Foid, Faid, Foname, Foctime, Relation)
        VALUES($1, $2, $3, $4, now(), $5)
        """
        try:
            async with self.pool.acquire() as connection:
                folder_relation = None
                if (
                    parent_folder_id and parent_folder_id != "/"
                ):  # 如果父文件夹id不为空，且不为根目录
                    parent_folder_relation = await connection.fetch(
                        sql_select_parent_folder_relation,
                        username,
                        parent_folder_id,
                    )
                    if parent_folder_relation:
                        folder_relation = (
                            parent_folder_relation[0]["relation"] or ""
                        )  # 获取父文件夹的层级关系
                        folder_relation += parent_folder_id  # 添加父文件夹id
                await connection.execute(
                    sql,
                    username,
                    new_folder_id,
                    parent_folder_id,
                    folder_name,
                    folder_relation,
                )
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 验证文件夹id是否为用户的文件夹
    async def FolderTable_verify(self, username: str, folder_id: str) -> bool:
        """
        验证文件夹id是否为用户的文件夹
        :param username: 用户名
        :param folder_id: 文件夹id
        :return: 如果是用户的文件夹就返回 True，否则返回 False
        """
        sql = """
        SELECT Uname
        FROM folders
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, folder_id)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    # 获取文件夹的层级文件id
    async def FolderTable_get_relation(self, username: str, folder_id: str) -> str:
        """
        获取文件夹的层级文件id
        :param username: 用户名
        :param folder_id: 文件夹id
        :return: 文件夹的层级文件id
        """
        sql = """
        SELECT Relation
        FROM folders
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, folder_id)
                return result[0]["relation"] if result else ""
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""

    # 获取文件夹名
    async def FolderTable_get_name(self, username: str, folder_id: str) -> str:
        """
        获取文件夹名
        :param username: 用户名
        :param folder_id: 文件夹id
        :return: 文件夹名
        """
        sql = """
        SELECT Foname
        FROM folders
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, folder_id)
                return result[0]["foname"] if result else ""
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""

    # 获取同一父类文件夹下的所有文件夹
    async def FolderTable_get_folders_from_parent_folder(
        self, username: str, parent_folder: str
    ) -> list:
        """
        获取同一父类文件夹下的所有文件夹
        :param username: 用户名
        :param parent_folder: 父文件夹
        :return: 同一父类文件夹下的所有文件夹
        """
        sql = """
        SELECT Foid, Foname, Foctime, Fopasswd
        FROM folders
        WHERE Uname = $1 AND Faid = $2 AND Foifdel = false
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, parent_folder)
                list_folder = []
                if result:
                    for i in result:
                        list_folder.append(
                            {
                                "uuid": i["foid"],
                                "name": i["foname"],
                                "time": i["foctime"],
                                "password": i["fopasswd"],
                            }
                        )
                return list_folder
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return []

    # 获取父级文件夹id
    async def FolderTable_get_parent_folder_id(
        self, username: str, folder_id: str
    ) -> str:
        """
        获取父级文件夹id
        :param username: 用户名
        :param folder_id: 文件夹id
        :return: 父级文件夹id
        """
        sql = """
        SELECT Faid
        FROM folders
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, folder_id)
                return result[0].get("faid")
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""

    # 获取文件夹密码
    async def FolderTable_get_password(self, username: str, folder_id: str) -> str:
        """
        获取文件夹密码
        :param username: 用户名
        :param folder_id: 文件夹id
        :return: 返回文件夹密码
        """
        sql = """
        SELECT Fopasswd
        FROM folders
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, folder_id)
                return result[0].get("fopasswd") if result else ""
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""

    # 删除文件夹
    async def FolderTable_delete(self, username: str, folder_id: str) -> str:
        """
        删除文件夹
        :param username: 用户名
        :param folder_id: 文件夹id
        """
        delete_sql = """
        UPDATE folders
        SET Foifdel = true
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(delete_sql, username, folder_id)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 重命名文件夹
    async def FolderTable_rename_folder(
        self, username: str, folder_id: str, new_folder_name: str
    ):
        """
        重命名文件夹，并返回父类文件夹id
        :param username: 用户名
        :param folder_id: 文件夹id
        :param new_folder_name: 新文件夹名
        :return: 父类文件夹id
        """
        update_sql = """
        UPDATE folders
        SET Foname = $3
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    update_sql, username, folder_id, new_folder_name
                )
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 加密文件夹
    async def FolderTable_encrypt_folder(
        self, username: str, folder_id: str, folder_password: str
    ):
        """
        加密文件夹
        :param username: 用户名
        :param folder_id: 文件夹id
        :param folder_password: 文件夹密码
        """
        update_sql = """
        UPDATE folders
        SET Fopasswd = $3
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    update_sql, username, folder_id, folder_password
                )
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 删除文件夹密码
    async def FolderTable_delete_password(self, username: str, folder_id: str):
        """
        删除文件夹密码
        :param username: 用户名
        :param folder_id: 文件夹id
        """
        sql = """
        UPDATE folders
        SET Fopasswd = null
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(sql, username, folder_id)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    async def FolderTable_has_folder(self, username: str, folder_id: str) -> bool:
        """
        验证文件夹下是否存在文件夹
        :param username: 用户名
        :param folder_id: 文件夹id
        :return: 如果文件夹存在，返回 True，否则返回 False
        """
        sql = """
        SELECT Foid
        FROM folders
        WHERE Uname = $1 AND Faid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, folder_id)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False


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
