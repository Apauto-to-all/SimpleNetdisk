import uuid


async def get_uuid() -> str:
    """
    生成uuid，返回uuid字符串
    :return: uuid字符串
    """
    return str(uuid.uuid4())  # 生成uuid，长度为36位


async def split_uuids(uuids_str: str) -> list:
    """
    分割uuid字符串
    :param uuids_str: 连接的uuid字符串
    :return: 分割后的uuid列表
    """
    if not uuids_str:
        return []
    return [uuids_str[i : i + 36] for i in range(0, len(uuids_str), 36)]
