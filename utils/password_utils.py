import bcrypt


def encrypt_password(password: str) -> str:
    """
    加密密码，返回加密后的密码
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()  # 返回加密后的密码，长度为60位


def verify_password(hashed_password: str, password: str) -> bool:
    """
    验证密码，返回True或False
    """
    return bcrypt.checkpw(
        password.encode(), hashed_password.encode()
    )  # 返回True或False，表示密码是否正确
