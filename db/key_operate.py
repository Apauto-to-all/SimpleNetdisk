# 混合类
# 密匙表的操作
import datetime
import logging
import traceback
import config
import secrets  # 导入secrets模块，用于生成随机密钥

# 获取日志记录器
logger = logging.getLogger(__name__)


class KeyOperate:
    async def KeyTable_insert_update_key(self, key: str) -> bool:
        """
        插入密匙，如果已经存在就更新密匙
        :param key: 密匙
        :return: 如果插入成功就返回 True，否则返回 False
        """
        sql = """
        INSERT INTO Keys (Kid, Key, Todate)
        VALUES ('1', $1, $2)
        ON CONFLICT (Kid) 
        DO UPDATE SET Key = EXCLUDED.Key, Todate = EXCLUDED.Todate;
        """
        todate = datetime.datetime.now() + datetime.timedelta(
            days=config.KEY_EXPIRE_DAYS
        )  # 生成到期时间
        try:
            async with self.pool.acquire() as connection:
                result = await connection.execute(sql, key, todate)
                return True if result else False
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return False

    async def KeyTable_get_key(self) -> str:
        """
        获取密匙
        :return: 返回密匙
        """
        sql = """
        SELECT Key
        FROM Keys
        WHERE Kid = '1' AND Todate > NOW()
        """
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetch(sql)
                if result:
                    return result[0]["key"]
                else:
                    await self.KeyTable_insert_update_key(
                        secrets.token_hex(32)
                    )  # 生成一个新的密匙，插入到数据库
                return await self.KeyTable_get_key()
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            return ""


"""
--密匙表
create table Keys(
	Kid KidDomain primary key,--密匙id
	Key KeyDomain,--密匙
	Todate timeDomain--到期时间
);
create domain timeDomain timestamp;
"""
