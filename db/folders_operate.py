# 混入类，实现对文件夹表的操作
# 实现对文件夹表的操作
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class FolderOperate:
    # 插入文件夹
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
        sql = """
        INSERT INTO folders(Uname, Foid, Faid, Foname, Foctime, Relation)
        VALUES($1, $2, $3, $4, now(), $5)
        """
        try:
            async with self.pool.acquire() as connection:
                folder_relation = None
                # 如果父文件夹id不为空，且不为根目录
                if parent_folder_id and parent_folder_id != "/":
                    parent_folder_relation = await self.FolderTable_get_relation(
                        username, parent_folder_id
                    )  # 获取父文件夹的层级关系
                    folder_relation = (
                        parent_folder_relation + parent_folder_id
                        if parent_folder_relation
                        else parent_folder_id
                    )
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

    # 获取父类文件夹下的所有文件夹
    async def FolderTable_get_all_folders_from_parent_folder_cpMove(
        self, username: str, parent_folder: str
    ) -> dict:
        """
        获取父类文件夹下的所有文件夹
        :param username: 用户名
        :param parent_folder: 父文件夹
        :return: 父类文件夹下的所有文件夹，返回一个字典，键为文件夹id，值为文件夹名
        """
        sql = """
        SELECT Foid, Foname
        FROM folders
        WHERE Uname = $1 AND Faid = $2 AND Foifdel = false
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username, parent_folder)
                list_folder = {}
                if result:
                    for i in result:
                        list_folder[i.get("foid")] = i.get("foname")
                return list_folder
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return {}

    # 获取文件夹下的所有文件夹id，返回一个列表
    async def FolderTable_get_all_file_id_from_parent_folder(
        self, username: str, parent_folder: str
    ) -> list:
        """
        获取文件夹下的所有文件夹id，返回一个列表
        :param username: 用户名
        :param parent_folder: 父文件夹
        :return: 文件夹下的所有文件夹id
        """
        sql = """
        SELECT Foid
        FROM folders
        WHERE Uname = $1 AND Faid = $2 AND Foifdel = false
        """
        try:
            async with self.pool.acquire() as connection:
                list_folder = []
                result = await connection.fetch(sql, username, parent_folder)
                if result:
                    for i in result:
                        list_folder.append(i["foid"])
                return list_folder
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return []

    # 父类文件夹下的所有文件夹id，包括子类文件夹，再子类文件夹下的文件夹id，返回一个列表
    async def FolderTable_get_all_folder_id(
        self, username: str, parent_folder: str
    ) -> list:
        """
        父类文件夹下的所有文件夹id，包括子类文件夹，再子类文件夹下的文件夹id，返回一个列表
        :param username: 用户名
        :param parent_folder: 父文件夹
        :return: 父类文件夹下的所有文件夹id，包括子类文件夹，再子类文件夹下的文件夹id
        """
        sql = """
        WITH RECURSIVE subfolders AS (
        SELECT Foid
        FROM folders
        WHERE Uname = $1 AND Faid = $2
        UNION ALL
        SELECT f.Foid
        FROM folders f
        INNER JOIN subfolders sf ON f.Faid = sf.Foid
        )
        SELECT Foid FROM subfolders;
        """
        try:
            async with self.pool.acquire() as connection:
                list_folder = []
                result = await connection.fetch(sql, username, parent_folder)
                if result:
                    for i in result:
                        list_folder.append(i["foid"])
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

    # 还原文件夹
    async def FolderTable_restore_folder(self, username: str, folder_id: str):
        """
        还原文件夹
        :param username: 用户名
        :param folder_id: 文件夹id
        """
        update_sql = """
        UPDATE folders
        SET Foifdel = false
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(update_sql, username, folder_id)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 重命名文件夹
    async def FolderTable_rename_folder(
        self, username: str, folder_id: str, new_folder_name: str
    ):
        """
        重命名文件夹
        :param username: 用户名
        :param folder_id: 文件夹id
        :param new_folder_name: 新文件夹名
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

    # 验证文件夹下是否存在文件夹
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

    # 验证同一文件夹下，是否存在文件夹名
    async def FolderTable_verify_name_only(
        self, username: str, parent_folder: str, folder_name: str
    ) -> bool:
        """
        验证同一文件夹下，是否存在文件夹名
        :param username: 用户名
        :param parent_folder: 父文件夹id
        :param folder_name: 文件夹名
        :return: 如果存在就返回 True，否则返回 False
        """
        sql = """
        SELECT Foname
        FROM folders
        WHERE Uname = $1 AND Faid = $2 AND Foname = $3
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(
                    sql, username, parent_folder, folder_name
                )
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    # 移动文件夹
    async def FolderTable_move_folder(
        self, username: str, target_folder_id: str, folder_id: str
    ):
        """
        移动文件夹
        :param username: 用户名
        :param target_folder_id: 目标文件夹id
        :param folder_id: 文件夹id
        """
        update_sql = """
        UPDATE Folders
        SET Faid = $3, Relation = $4
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                new_relation = None
                if target_folder_id and target_folder_id != "/":
                    # 获取 target_folder_id 的 Relation
                    target_relation = await self.FolderTable_get_relation(
                        username, target_folder_id
                    )
                    # 构建新的 Relation 值
                    new_relation = (
                        target_relation + target_folder_id
                        if target_relation
                        else target_folder_id
                    )
                # 更新 folder_id 的 Faid 和 Relation
                await connection.execute(
                    update_sql, username, folder_id, target_folder_id, new_relation
                )
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 复制文件夹
    async def FolderTable_copy_folder(
        self,
        username: str,
        target_folder_id: str,
        folder_id: str,
        new_folder_id: str,
    ):
        """
        复制文件夹
        :param username: 用户名
        :param target_folder_id: 目标文件夹id
        :param folder_id: 文件夹id
        :param new_folder_id: 新文件夹id
        """
        insert_sql = """
        INSERT INTO Folders(Uname, Foid, Faid, Foname, Foctime, Relation, Fopasswd)
        SELECT Uname, $3, $4, Foname, now(), $5, null
        FROM Folders
        WHERE Uname = $1 AND Foid = $2
        """
        try:
            async with self.pool.acquire() as connection:
                new_relation = None
                if target_folder_id and target_folder_id != "/":
                    # 获取 target_folder_id 的 Relation
                    target_relation = await self.FolderTable_get_relation(
                        username, target_folder_id
                    )
                    # 构建新的 Relation 值
                    new_relation = (
                        target_relation + target_folder_id
                        if target_relation
                        else target_folder_id
                    )
                # 复制文件夹
                await connection.execute(
                    insert_sql,
                    username,
                    folder_id,
                    new_folder_id,
                    target_folder_id,
                    new_relation,
                )
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)


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
