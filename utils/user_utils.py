from . import jwt_token, password_utils


def isLogin(access_token) -> bool:
    """
    判断用户是否登录
    :param access_token: JWT Token
    :return: 如果用户登录，返回 True，否则返回 False
    """
    if jwt_token.get_user_from_jwt(access_token):  # 从 JWT 中获取用户名
        return True  # 返回 True
    return False


def get_token(user: str) -> str:
    """
    通过用户名获取 Token
    :param user: 用户名
    :return: JWT Token
    """
    return jwt_token.get_access_jwt(user)  # 生成 JWT Token


async def verifyLogin(username, password) -> bool:
    """
    验证登录
    :param username: 用户名
    :param password: 密码
    :return: 如果用户名和密码正确，返回 True，否则返回 False
    """
    if username == "admin" and password == "passwd":
        return True
    return False


async def verifyUsername(username: str) -> bool:
    """
    验证用户名是否存在
    :param username: 用户名
    :return: 如果用户名存在，返回 False，否则返回 True
    """
    if username == "admin":  # 如果用户名存在
        return False
    return True  # 如果用户名不存在


async def verifyCaptcha(captcha: str) -> bool:
    """
    验证验证码
    :param captcha: 验证码
    :return: 如果验证码正确，返回 True，否则返回 False
    """
    if captcha == "captcha":  # 如果验证码正确
        return True  # 返回 True
    return False  # 返回 False


async def verifyRegCode(regCode: str) -> bool:
    """
    验证注册码
    :param regCode: 注册码
    :return: 如果注册码正确，返回 True，否则返回 False
    """
    if regCode == "regCode":  # 如果注册码正确
        return True  # 返回 True
    return False  # 返回 False


async def registerSuccess(username: str, password: str, regCode: str):
    """
    注册成功，保存用户信息，并让注册码使用次数-1
    :param username: 用户名
    :param password: 密码
    :param regCode: 注册码
    """
    password = password_utils.encrypt_password(password)  # 加密密码


failed_count = 0  # 访问者错误次数


async def isUseCapthca() -> bool:
    """
    判断是否使用验证码
    :return: 如果使用验证码，返回 True，否则返回 False
    """
    global failed_count  # 全局变量
    if failed_count >= 3:  # 如果错误次数大于等于 3
        return True
    return False  # 否则返回 False


async def login_or_register_failed():
    """
    登录或注册失败
    访问者错误次数+1
    """
    global failed_count  # 全局变量
    failed_count += 1  # 错误次数+1
    pass


async def login_or_register_success():
    """
    登入或注册成功
    访问者错误次数清零
    """
    global failed_count  # 全局变量
    failed_count = 0  # 错误次数清零
    pass
