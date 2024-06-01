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
                return result[0].get("passwd")
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
        SELECT Nname, Hpath, Uspace, Mspace
        FROM (
            SELECT Grade
            FROM Users
            WHERE Uname = $1
        ) AS UserGrade
        INNER JOIN Grades ON UserGrade.Grade = Grades.Grade;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, username)
                return result[0]
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return {}


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
