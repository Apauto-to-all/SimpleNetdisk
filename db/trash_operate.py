# 混合类
# 数据库垃圾桶表操作类
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class TrashOperate:
    async def TrashTable_insert(
        self,
        username: str,
        file_id: str = None,
        folder_id: str = None,
    ):
        """
        插入删除的文件或文件夹到垃圾桶表
        """
        select_date = """
        SELECT Grades.Ktime
        FROM Users
        INNER JOIN Grades ON Users.Grade = Grades.Grade
        WHERE Users.Uname = $1
        """
        sql = """
        INSERT INTO Trash(Uname, Fshareid, ForFi, Ptime, Fideltime)
        VALUES ($1, $2, $3, now(), now() + interval '1 day' * $4)
        """
        try:
            async with self.pool.acquire() as connection:
                day_num = await connection.fetchval(select_date, username)
                if file_id:
                    await connection.execute(sql, username, file_id, False, day_num)
                if folder_id:
                    await connection.execute(sql, username, folder_id, True, day_num)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    async def TrashTable_get_all_folder(
        self,
        username: str,
    ) -> list:
        """
        获取用户所有删除的文件夹
        """
        sql = """
        SELECT T.Fshareid, T.Ptime, T.Fideltime, F.Foname
        FROM Trash T
        JOIN Folders F ON T.Uname = F.Uname AND T.Fshareid = F.Foid
        WHERE T.Uname = $1 AND T.ForFi = true;
        """
        try:
            async with self.pool.acquire() as connection:
                folder_list = await connection.fetch(sql, username)
                list = []
                for folder in folder_list:
                    list.append(
                        {
                            "uuid": folder["fshareid"],
                            "folder_name": folder["foname"],
                            "drop_time": folder["ptime"],
                            "delete_time": folder["fideltime"],
                        }
                    )
                return list
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return []

    # 获取用户所有删除的文件
    async def TrashTable_get_all_file(
        self,
        username: str,
    ) -> list:
        """
        获取用户所有删除的文件
        """
        sql = """
        SELECT T.Fshareid, T.Ptime, T.Fideltime, Fi.Finame
        FROM Trash T
        JOIN Files Fi ON T.Uname = Fi.Uname AND T.Fshareid = Fi.Fid
        WHERE T.Uname = $1 AND T.ForFi = false;
        """
        try:
            async with self.pool.acquire() as connection:
                file_list = await connection.fetch(sql, username)
                list = []
                for file in file_list:
                    list.append(
                        {
                            "uuid": file["fshareid"],
                            "file_name": file["finame"],
                            "drop_time": file["ptime"],
                            "delete_time": file["fideltime"],
                        }
                    )
                return list
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return []

    # 还原文件夹，删除垃圾桶表中的文件夹记录
    async def TrashTable_delete_folder(
        self,
        username: str,
        folder_id: str,
    ):
        """
        还原文件夹，删除垃圾桶表中的文件夹记录
        """
        sql = """
        DELETE FROM Trash
        WHERE Uname = $1 AND Fshareid = $2 AND ForFi = true
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(sql, username, folder_id)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 还原文件，删除垃圾桶表中的文件记录
    async def TrashTable_delete_file(
        self,
        username: str,
        file_id: str,
    ):
        """
        还原文件，删除垃圾桶表中的文件记录
        """
        sql = """
        DELETE FROM Trash
        WHERE Uname = $1 AND Fshareid = $2 AND ForFi = false
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(sql, username, file_id)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)


"""
--垃圾桶表
create table Trash(
	Uname UnameDomain,--用户名
	Fshareid FidDomain,--文件id和文件夹id
	ForFi ifDomain,--文件还是文件夹，true为文件夹，false为文件
	Ptime timeDomain,--放入回收站时间
	Fideltime timeDomain,--文件删除时间
	primary key (Uname, Fid),
	foreign key (Uname) references Users(Uname),
);
"""
