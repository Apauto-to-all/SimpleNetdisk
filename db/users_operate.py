# 混合类
# 操作用户表的类
import os
import traceback
import config  # 配置文件
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


class UsersOperate:
    async def UsersTable_insert(
        self,
        username: str,
        password: str,
        grade: int,
    ) -> bool:
        """
        插入用户
        :param username: 用户名
        :param password: 密码
        :param grade: 等级
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql_insert_user = """
        INSERT INTO Users(Uname, Passwd, Grade, Uspace, Nname, Hpath)
        VALUES($1, $2, $3, 0, $4, $5); 
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(
                    sql_insert_user,
                    username,
                    password,
                    grade,
                    username,
                    os.path.join(config.user_avatar_path, "default.jpg"),
                )
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    async def UsersTable_verify_username(self, username: str) -> bool:
        """
        验证用户名是否存在
        :param username: 用户名
        :return: 如果用户名存在，返回 True，否则返回 False
        """
        sql = """
        select Uname
        from Users
        where Uname = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    async def UsersTable_get_password(self, username: str) -> str:
        """
        获取用户密码
        :param username: 用户名
        :return: 返回用户密码
        """
        sql = """
        select Passwd
        from Users
        where Uname = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username)
                return result[0].get("passwd") if result else ""
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""

    # 更新用户密码
    async def UsersTable_update_password(self, username: str, password: str) -> bool:
        """
        更新用户密码
        :param username: 用户名
        :param password: 密码
        :return: 如果更新成功就返回 True，否则返回 False
        """
        sql = """
        update Users
        set Passwd = $2
        where Uname = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, username, password)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    # 查询用户的所有信息
    async def UsersTable_select_all(self, username: str) -> dict:
        """
        查询用户的所有信息
        :param username: 用户名
        :return: 返回用户的所有信息
        """
        sql = """
        SELECT Nname, Uspace, Mspace
        FROM Users
        INNER JOIN Grades ON Users.Grade = Grades.Grade
        WHERE Uname = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username)
                dict = {}
                if result:
                    dict["nickname"] = result[0].get("nname")
                    dict["capacity_used"] = result[0].get("uspace")
                    dict["capacity_total"] = result[0].get("mspace")
                return dict
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return {}

    # 查询头像路径
    async def UsersTable_select_hpath(self, username: str) -> str:
        """
        查询头像路径
        :param username: 用户名
        :return: 返回头像路径
        """
        sql = """
        select Hpath
        from Users
        where Uname = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username)
                if result:
                    return result[0].get("hpath")
                return ""
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""

    # 插入文件后，更新用户已使用容量
    async def UsersTable_update_uspace(self, username: str, file_size: int):
        """
        插入文件后，更新用户已使用容量
        :param username: 用户名
        :param file_size: 文件大小
        :return: 如果更新成功就返回 True，否则返回 False
        """
        sql = """
        update Users
        set Uspace = Uspace + $2
        where Uname = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(sql, username, file_size)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)

    # 更新用户昵称
    async def UsersTable_update_nickname(self, username: str, nickname: str) -> bool:
        """
        更新用户昵称
        :param username: 用户名
        :param nickname: 昵称
        :return: 如果更新成功就返回 True，否则返回 False
        """
        sql = """
        update Users
        set Nname = $2
        where Uname = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, username, nickname)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    # 获取用户最大上传文件大小
    async def UsersTable_select_max_upload_file_size(self, username: str) -> int:
        """
        获取用户最大上传文件大小
        :param username: 用户名
        :return: 返回用户最大上传文件大小
        """
        sql = """
        SELECT Mupfile
        FROM Users
        INNER JOIN Grades ON Users.Grade = Grades.Grade
        WHERE Uname = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username)
                return result[0].get("mupfile") if result else 0
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return 0

    # 更新用户的使用空间，减去永久删除的文件大小
    async def UsersTable_update_uspace_minus_file_size(
        self, username: str, file_size: int
    ):
        """
        更新用户的使用空间，减去永久删除的文件大小，如果减去的大小大于用户的使用空间，就设置使用空间为 0
        :param username: 用户名
        :param file_size: 文件大小，要减去的大小，
        """
        sql = """
        update Users
        set Uspace = GREATEST(Uspace - $2, 0)
        where Uname = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(sql, username, file_size)
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)


"""
--等级表
create table Grades(
	Grade GradeDomain primary key, --等级
	Mspace CapacityDomain, --最大容量
	Mupfile CapacityDomain, --最大上传文件大小
	Ktime KtimeDomain --回收站保存时间
);

--用户表
create table Users(
	Uname UnameDomain primary key, --用户名
	Passwd PasswdDomain, --密码
	Grade GradeDomain, --等级
	Uspace UspaceDomain, --用户空间
	Nname NnameDomain, --昵称
	Hpath PathDomain, --头像路径
	foreign key (Grade) references Grades(Grade)
);
"""
