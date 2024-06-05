from utils import uuid_utils
from db.connection import DatabaseOperation  # 导入数据库操作类

db_operation = DatabaseOperation()  # 实例化数据库操作类


async def get_files(username: str, folder_id: str) -> list:
    """
    获取用户文件，uuid+文件名+文件大小+文件类型+创建时间，文件夹被删除不添加到列表中
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 用户文件字典
    """
    if username and folder_id:
        return await db_operation.FileTable_get_files_from_parent_folder(
            username,
            folder_id,
        )


async def get_folders(username: str, folder_id: str) -> list:
    """
    获取所有当前文件夹下的文件夹，uuid+文件夹名+创建时间+文件夹密码，文件夹被删除不添加到列表中
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 用户文件夹字典
    """
    if username and folder_id:
        return await db_operation.FolderTable_get_folders_from_parent_folder(
            username,
            folder_id,
        )


# 获取父类文件夹的层级关系
async def get_folder_path(username: str, folder_id: str) -> dict:
    """
    获取父类文件夹的层级关系，文件夹id+文件夹名
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 文件夹层级关系
    """
    if username and folder_id:
        uuid_str = await db_operation.FolderTable_get_relation(
            username,
            folder_id,
        )  # 文件夹的层级关系
        uuid_list = await uuid_utils.split_uuids(uuid_str)  # 分割文件夹id，返回列表
        dict_path = {}
        for uuid in uuid_list:  # 遍历文件夹id
            dict_path[uuid] = await db_operation.FolderTable_get_name(
                username,
                uuid,
            )  # 获取文件夹名
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


async def convert_kb_to_human_readable(file_size_kb: int) -> str:
    """
    将KB转换为MB，GB，保留两位小数
    :param file_size_kb: 文件大小
    :return: 文件大小
    """
    if file_size_kb < 1024:
        return f"{file_size_kb}KB"
    elif file_size_kb < 1024 * 1024:
        return f"{file_size_kb / 1024:.2f}MB"
    else:
        return f"{file_size_kb / 1024 / 1024:.2f}GB"


async def get_all(username: str, folder_id: str) -> dict:
    """
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 返回页面所有文件的内容
    """
    all_dict = {}
    all_dict["folders_path"] = await get_folder_path(username, folder_id)
    all_dict["folders"] = await get_folders(username, folder_id)
    all_dict["files"] = await get_files(username, folder_id)
    for file in all_dict["files"]:
        file["size"] = await convert_kb_to_human_readable(
            file["size"]
        )  # 将KB转换为MB，GB，保留两位小数
        file["time"] = await convert_time_to_chinese(
            file["time"]
        )  # 时间转换为中文的年月日
    for folder in all_dict["folders"]:
        folder["time"] = await convert_time_to_chinese(
            folder["time"]
        )  # 时间转换为中文的年月日
    return all_dict


async def get_all_user(username: str) -> dict:
    """
    获取用户昵称，用户头像路径，用户总容量，用户已使用容量，用户容量百分比
    :param username: 用户名
    :return: 用户信息
    """
    all_user_dict = await db_operation.UsersTable_select_all(username)
    all_user_dict["capacity_percent"] = round(
        all_user_dict["capacity_used"] / all_user_dict["capacity_total"] * 100, 2
    )
    all_user_dict["capacity_total"] = await convert_kb_to_human_readable(
        all_user_dict["capacity_total"]
    )  # 将KB转换为MB，GB，保留两位小数
    all_user_dict["capacity_used"] = await convert_kb_to_human_readable(
        all_user_dict["capacity_used"]
    )  # 将KB转换为MB，GB，保留两位小数
    return all_user_dict


async def get_all_trash(username: str) -> dict:
    """
    :param username: 用户名
    :return: 返回页面所有文件的内容
    """
    all_dict = {}
    all_dict["trash_folders"] = get_trash_folders(username)
    all_dict["trash_files"] = get_trash_files(username)
    return all_dict


# 2024-06-04 15:35:22.276136，时间转换为中文的年月日
async def convert_time_to_chinese(time_str: str) -> str:
    """
    时间转换为中文的年月日
    :param time_str: 时间
    :return: 中文的年月日
    """
    # 格式化为中文的年月日
    chinese_date = time_str.strftime("%Y年%m月%d日")
    return chinese_date
