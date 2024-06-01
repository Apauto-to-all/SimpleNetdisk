from . import jwt_token, password_utils
from fastapi import Request
from db.connection import DatabaseOperation

db_operation = DatabaseOperation()


async def isLogin_getUser(access_token: str) -> str:
    """
    判断用户是否登录，并通过 JWT Token 获取用户名
    :param access_token: JWT Token
    :return: 如果用户登录，返回用户名，否则返回空字符串
    """
    return jwt_token.get_user_from_jwt(access_token)  # 从 JWT 中获取用户名


async def get_token(user: str) -> str:
    """
    通过用户名获取 Token
    :param user: 用户名
    :return: JWT Token
    """
    return jwt_token.get_access_jwt(user)  # 生成 JWT Token


async def verify_get_username_format(username: str) -> str:
    """
    只能是英文或数字，长度在4-20之间
    验证用户名格式，并返回用户名缺少的格式信息
    :param username: 用户名
    :return: 如果用户名格式正确，返回 ""，否则返回用户名缺少的格式信息
    """
    if len(username) < 4:
        return "用户名长度不能小于4"
    if len(username) > 20:
        return "用户名长度不能大于20"
    if not username.isalnum():
        return "用户名只能包含字母和数字"
    return ""


async def verifyLogin(username, password) -> bool:
    """
    验证登录
    :param username: 用户名
    :param password: 密码
    :return: 如果用户名和密码正确，返回 True，否则返回 False
    """
    hashed_password = await db_operation.UsersTable_get_password(
        username
    )  # 获取用户密码
    if await password_utils.verify_password(hashed_password, password):  # 验证密码
        return True
    return False


async def verifyUsername(username: str) -> bool:
    """
    验证用户名是否存在
    :param username: 用户名
    :return: 如果用户名存在，返回 False，否则返回 True
    """
    if await db_operation.UsersTable_verify_username(username):
        return False
    return True


async def verifyCaptcha(captcha, hashed_captcha) -> bool:
    """
    验证验证码
    :param captcha: 验证码
    :param hashed_captcha: 加密后的验证码
    :return: 如果验证码正确，返回 True，否则返回 False
    """
    if await password_utils.verify_password(
        hashed_captcha, captcha.lower()
    ) or await password_utils.verify_password(hashed_captcha, captcha):
        return True  # 返回 True
    return False  # 返回 False


async def verifyRegCode(regCode: str) -> bool:
    """
    验证注册码
    :param regCode: 注册码
    :return: 如果注册码正确，且使用次数大于 0，返回 True，否则返回 False
    """
    if await db_operation.RcodesTable_verify_rcode(regCode):
        return True
    return False


async def registerSuccess(username: str, password: str, regCode: str):
    """
    注册成功，保存用户信息，并让注册码使用次数-1
    :param username: 用户名
    :param password: 密码
    :param regCode: 注册码
    """
    password = password_utils.encrypt_password(password)  # 加密密码
    grade = await db_operation.RcodesTable_get_grade(regCode)  # 获取等级
    if await db_operation.UsersTable_insert(
        username, password, grade
    ):  # 插入用户信息，如果插入成功
        await db_operation.RcodesTable_update_times_sub_one(regCode)  # 注册码使用次数-1


async def isUseCapthca(request: Request) -> bool:
    """
    判断是否使用验证码
    :return: 如果使用验证码，返回 True，否则返回 False
    """
    client_host = request.client.host  # 获取客户端IP地址
    user_agent = request.headers.get("User-Agent")  # 获取User-Agent请求头
    faile_num = await db_operation.AccessLogTable_get_failnum(
        client_host, user_agent
    )  # 获取失败次数
    if faile_num == -1 or faile_num >= 3:  # 如果失败次数为 -1 或者大于 3
        return True  # 返回 True
    return False  # 返回 False


async def login_or_register_failed(request: Request):
    """
    登录或注册失败
    访问者错误次数+1
    """
    client_host = request.client.host  # 获取客户端IP地址
    user_agent = request.headers.get("User-Agent")  # 获取User-Agent请求头
    await db_operation.AccessLogTable_insert(client_host, user_agent)  # 插入日志
    await db_operation.AccessLogTable_insert_ip(client_host)  # 插入日志


async def login_or_register_success(request: Request):
    """
    登入或注册成功
    访问者错误次数清零
    """
    client_host = request.client.host  # 获取客户端IP地址
    user_agent = request.headers.get("User-Agent")  # 获取User-Agent请求头
    await db_operation.AccessLogTable_update_failnum_zero(
        client_host, user_agent
    )  # 更新失败次数为 0
