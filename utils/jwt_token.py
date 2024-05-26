import uuid
import jwt  # 导入jwt模块
import binascii  # 导入binascii模块，用于生成随机密钥
from datetime import datetime, timedelta, timezone
import secrets  # 导入secrets模块，用于生成随机密钥

ALGORITHM = "HS256"  # 加密算法


def create_secret_key():
    """
    创建并储存密钥
    """
    SECRET_KEY = secrets.token_hex(32)  # 生成64位随机密钥
    # 储存密钥
    return SECRET_KEY


def get_secret_key() -> str:
    """
    获取密钥
    """
    # 读取密钥
    SECRET_KEY = "secret_key"
    return SECRET_KEY


def get_access_jwt(user: str) -> str:
    """
    生成JWT
    """
    SECRET_KEY = get_secret_key()
    payload = {
        "jti": str(uuid.uuid4()),  # JWT ID
        "user": user,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=20),  # 使用带有UTC时区信息的datetime对象
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # 生成token
    return access_token


def get_user_from_jwt(token: str) -> str:
    """
    验证JWT，返回用户信息
    """
    SECRET_KEY = get_secret_key()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # 解码token
        return payload.get("user")  # 返回用户信息
    except jwt.ExpiredSignatureError:
        "Token已过期"
        return None
    except jwt.InvalidTokenError:
        "无效的Token"
        return None
