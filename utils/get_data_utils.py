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
        total = 1024  # 总容量，KB
        used = 500  # 使用容量，KB
        return {
            "total": total,  # 总容量
            "used": used,  # 使用容量
            "percent": round(used / total * 100, 2),  # 使用百分比
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
                "uuid": "bb0c75ae-b2f2-4c56-838b-f6f2e21efef0",  # 文件id
                "name": "name",  # 文件名
                "size": "size",  # 文件大小
                "type": "type",  # 文件类型
                "time": "time",  # 上传时间
            },
            {
                "uuid": "8a5eca0a-7946-4650-ba7c-14f64140f15a",
                "name": "name2",
                "size": "size2",
                "type": "tddddype2",
                "time": "time2",
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
                "uuid": "5f1dadcf-5842-411b-89d0-dff767d1fd30",  # 文件夹id
                "name": "name",  # 文件夹名
                "time": "time",  # 创建时间
                "password": "password",  # 文件夹密码
            },
            {
                "uuid": "f7becf55-2d8d-40bc-a971-ec4318a751ad",
                "name": "name2",
                "time": "time2",
                "password": "",
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
        uuid_str = "adaa6474-a046-4148-bbfc-6ea9f7cc62f3c7f0654a-e4b1-479e-bc22-ac9f9237b5fce7ab8022-7998-432b-bfa2-f44185e28e45"  # 文件夹的层级关系
        uuid_list = uuid_utils.split_uuids(uuid_str)  # 分割文件夹id
        dict_path = {}
        for i, uuid in enumerate(uuid_list):  # 遍历文件夹id
            dict_path[uuid] = f"name{i}"  # 文件夹id+文件夹名
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
                "uuid": "979575c3-3ebe-465e-9f1e-f176fe321003",  # 文件夹id
                "name": "name",  # 文件夹名
                "time": "time",  # 删除剩余时间
            },
            {
                "uuid2": "9339848c-b14c-482f-8c46-5f7cc4a64a97",
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
                "uuid": "c6f414e2-08c0-4aac-849f-2e03640e5d42",  # 文件id
                "name": "name",  # 文件名
                "type": "type",  # 文件类型
                "time": "time",  # 删除剩余时间
            },
            {
                "uuid": "c2f6aa56-4c38-41f8-9d7a-a54ad42f178a",
                "name": "name2",
                "type": "type",
                "time": "time2",
            },
        ]


def get_all(username: str, folder_id: str) -> dict:
    """
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 返回页面所有文件的内容
    """
    all_dict = {}
    all_dict["folders_path"] = get_folder_path(username, folder_id)
    all_dict["folders"] = get_folders(username, folder_id)
    all_dict["files"] = get_files(username, folder_id)
    return all_dict


def get_all_user(username: str) -> dict:
    """
    获取用户信息+容量信息
    :param username: 用户名
    :return: 用户信息
    """
    all_user_dict = {}
    all_user_dict.update(get_nickname(username))
    all_user_dict["capacity"] = get_capacity(username)
    return all_user_dict


def get_all_trash(username: str) -> dict:
    """
    :param username: 用户名
    :return: 返回页面所有文件的内容
    """
    all_dict = {}
    all_dict["trash_folders"] = get_trash_folders(username)
    all_dict["trash_files"] = get_trash_files(username)
    return all_dict
