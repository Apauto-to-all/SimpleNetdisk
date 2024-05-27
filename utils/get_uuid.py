import uuid


def get_uuid() -> str:
    """
    生成uuid，返回uuid字符串
    :return: uuid字符串
    """
    return str(uuid.uuid4())  # 生成uuid，长度为36位
