import bcrypt  # 导入bcrypt库，用于密码加密


def encrypt_password(password: str) -> str:
    """
    :param password: 密码
    :return: 返回加密后的密码
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()  # 返回加密后的密码，长度为60位


async def verify_password(hashed_password: str, password: str) -> bool:
    """
    :param hashed_password: 加密后的密码
    :param password: 密码
    :return: 返回密码是否正确，True表示密码正确，False表示密码错误
    """
    try:
        return bcrypt.checkpw(
            password.encode(), hashed_password.encode()
        )  # 返回True或False，表示密码是否正确
    except Exception as e:
        return False  # 返回False，表示密码错误


def verify_get_password_format(password) -> str:
    """
    :param password: 密码
    :return: 密码缺少的格式信息，如果密码格式正确，返回空字符串
    """
    if len(password) < 8:
        return "密码长度不能小于8"
    if len(password) > 20:
        return "密码长度不能大于20"
    if not any(c.isdigit() for c in password):
        return "密码中必须包含数字"
    if not any(c.isupper() for c in password):
        return "密码中必须包含大写字母"
    if not any(c.islower() for c in password):
        return "密码中必须包含小写字母"
    if not any(c in "@#$%^&*()_+-=" for c in password):
        return "密码中必须包含特殊符号（@#$%^&*()_+-=）"
    return ""
