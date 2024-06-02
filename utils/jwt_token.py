from utils.uuid_utils import get_uuid  # 导入生成UUID的方法
import jwt  # 导入jwt模块
from datetime import datetime, timedelta, timezone

import config  # 导入配置文件
from db.connection import DatabaseOperation  # 导入数据库操作类

ALGORITHM = "HS256"  # 加密算法
db_operation = DatabaseOperation()


async def get_access_jwt(user: str) -> str:
    """
    生成JWT
    :param user: 用户信息
    :return: JWT Token
    """
    SECRET_KEY = await db_operation.KeyTable_get_key()  # 获取密匙
    payload = {
        "jti": get_uuid(),  # JWT ID
        "user": user,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=config.login_time),  # 使用带有UTC时区信息的datetime对象
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # 生成token
    return access_token


async def get_user_from_jwt(token: str) -> str:
    """
    验证JWT，返回用户信息，如果Token无效，返回空字符串
    :param token: JWT Token
    :return: 用户信息，如果Token无效，返回None
    """
    SECRET_KEY = await db_operation.KeyTable_get_key()  # 获取密匙
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # 解码token
        return payload.get("user")  # 返回用户信息
    except jwt.ExpiredSignatureError:
        "Token已过期"
        return None
    except jwt.InvalidTokenError:
        "无效的Token"
        return None
