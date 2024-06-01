# 混合类
# 实现ip+请求头日志记录
import logging
import traceback

# 获取日志记录器
logger = logging.getLogger(__name__)


class AccessLogOperate:
    async def AccessLogTable_insert(self, ip: str, headers: str):
        """
        插入日志
        :param ip: ip地址
        :param headers: 请求头
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO Accesslog (IP, Rheader, Failnum)
        VALUES ($1, $2, 1)
        ON CONFLICT (IP, Rheader)
        DO UPDATE SET Failnum = Accesslog.Failnum + 1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, ip, headers)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    async def AccessLogTable_insert_ip(self, ip: str):
        """
        插入日志
        :param ip: ip地址
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO Accesslog (IP, Rheader, Failnum)
        VALUES ($1, '', 1)
        ON CONFLICT (IP, Rheader)
        DO UPDATE SET Failnum = Accesslog.Failnum + 1;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, ip)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    async def AccessLogTable_get_failnum(self, ip: str, headers: str) -> int:
        """
        获取失败次数
        :param ip: ip地址
        :param headers: 请求头
        :return: 返回失败次数
        """
        sql = """
        select Failnum
        from Accesslog
        where IP = $1 and Rheader = $2;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql, ip, headers)
                return result[0].get("failnum")
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return 0

    # 成功，更新失败次数为 0
    async def AccessLogTable_update_failnum_zero(self, ip: str, headers: str) -> bool:
        """
        更新失败次数为 0
        :param ip: ip地址
        :param headers: 请求头
        :return: 如果更新成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO Accesslog (IP, Rheader, Failnum)
        VALUES ($1, $2, 0)
        ON CONFLICT (IP, Rheader)
        DO UPDATE SET Failnum = 0;
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, ip, headers)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False


"""
--访问日志表
create table Accesslog(
	IP IPDomain, -- IP
	Rheader PathDomain, -- 请求头
	Failnum TimesDomain, -- 登入失败次数
	primary key (IP, Rheader)
);

"""
