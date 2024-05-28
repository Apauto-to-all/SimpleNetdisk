from . import uuid_utils


def get_nickname(username: str) -> dict:
    """
    获取用户昵称
    :param username: 用户名
    :return: 用户昵称
    """
    if username:
        return {"nickname": username}


# 获取总容量和使用容量
def get_capacity(username: str) -> dict:
    """
    获取总容量+使用容量+使用百分比
    :param username: 用户名
    :return: 容量字典
    """
    if username:
        total = 1024  # 总容量
        used = 512  # 使用容量
        return {
            "total": total,  # 总容量
            "used": used,  # 使用容量
            "percent": used / total * 100,  # 使用百分比
        }


def get_files(username: str, folder_id: str) -> list:
    """
    获取用户文件，uuid+文件名+文件大小+文件类型+创建时间，文件夹被删除不添加到列表中
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 用户文件字典
    """
    if username and folder_id:
        return [
            {
                "uuid": "uuid",  # 文件id
                "name": "name",  # 文件名
                "size": "size",  # 文件大小
                "type": "type",  # 文件类型
                "time": "time",  # 上传时间
            },
            {
                "uuid2": "uuid2",
                "name2": "name2",
                "size2": "size2",
                "type2": "type2",
                "time2": "time2",
            },
        ]


def get_folders(username: str, folder_id: str) -> list:
    """
    获取所有当前文件夹下的文件夹，uuid+文件夹名+创建时间+文件夹密码，文件夹被删除不添加到列表中
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 用户文件夹字典
    """
    if username and folder_id:
        return [
            {
                "uuid": "uuid",  # 文件夹id
                "name": "name",  # 文件夹名
                "time": "time",  # 创建时间
                "password": "password",  # 文件夹密码
            },
            {
                "uuid2": "uuid2",
                "name2": "name2",
                "time2": "time2",
                "password2": "password2",
            },
        ]


# 获取父类文件夹的层级关系
def get_folder_path(username: str, folder_id: str) -> dict:
    """
    获取父类文件夹的层级关系，文件夹id+文件夹名
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 文件夹层级关系
    """
    if username and folder_id:
        uuid_str = ""  # 文件夹的层级关系
        uuid_list = uuid_utils.split_uuids(uuid_str)  # 分割文件夹id
        dict_path = {}
        for uuid in uuid_list:
            dict_path[uuid] = "name"
        return dict_path


# 获取垃圾桶文件夹
def get_trash_folders(username: str) -> list:
    """
    获取垃圾桶文件夹，uuid+文件夹名+删除剩余时间
    :param username: 用户名
    :return: 垃圾桶文件夹字典
    """
    if username:
        return [
            {
                "uuid": "uuid",  # 文件夹id
                "name": "name",  # 文件夹名
                "time": "time",  # 删除剩余时间
            },
            {
                "uuid2": "uuid2",
                "name2": "name2",
                "time2": "time2",
            },
        ]


# 获取垃圾桶文件
def get_trash_files(username: str) -> list:
    """
    获取垃圾桶文件，uuid+文件名+文件类型+删除剩余时间
    :param username: 用户名
    :return: 垃圾桶文件字典
    """
    if username:
        return [
            {
                "uuid": "uuid",  # 文件id
                "name": "name",  # 文件名
                "type": "type",  # 文件类型
                "time": "time",  # 删除剩余时间
            },
            {
                "uuid2": "uuid2",
                "name2": "name2",
                "type2": "type2",
                "time2": "time2",
            },
        ]
