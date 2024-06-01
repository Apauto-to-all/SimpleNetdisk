# 混合类
# 操作数据库中的rcodes注册码表
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class RcodesOperate:
    async def RcodesTable_insert(self, rcode: str):
        """
        插入注册码
        :param rcode: 注册码
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO rcodes(rcode)
        VALUES($1)
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, rcode)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    # 验证注册码是否存在
    async def RcodesTable_verify_rcode(self, rcode: str) -> bool:
        """
        验证注册码是否存在
        :param rcode: 注册码
        :return: 如果注册码存在，使用次数大于 0，返回 True，否则返回 False
        """
        sql = """
        select Rcode, Times
        from Rcodes
        where Rcode = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, rcode)
                if result:
                    if result[0].get("times") > 0:
                        return True
                return False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    # 注册码使用次数-1
    async def RcodesTable_update_times_sub_one(self, rcode: str) -> bool:
        """
        注册码使用次数-1
        :param rcode: 注册码
        :return: 如果更新成功就返回 True，否则返回 False
        """
        sql = """
        update Rcodes
        set Times = Times - 1
        where Rcode = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, rcode)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    # 通过注册码获取等级
    async def RcodesTable_get_grade(self, rcode: str) -> int:
        """
        通过注册码获取等级
        :param rcode: 注册码
        :return: 返回等级
        """
        sql = """
        select Grade
        from Rcodes
        where Rcode = $1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, rcode)
                return int(result[0].get("grade"))
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return 0


"""
--注册码表
create table Rcodes(
	Rcode RcodeDomain primary key, --注册码
	Grade GradeDomain, --注册码等级
	Times TimesDomain, --注册码使用次数
	foreign key (Grade) references Grades(Grade)
);
"""
