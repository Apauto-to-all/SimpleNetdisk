from utils import uuid_utils
from db.connection import DatabaseOperation
from utils import files_utils

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


# 从文件夹id获取文件夹名
async def get_folder_name(username: str, folder_id: str) -> str:
    """
    从文件夹id获取文件夹名
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 文件夹名
    """
    return await db_operation.FolderTable_get_name(username, folder_id)


# 获取页面所有文件的内容
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


# 获取用户昵称，用户头像路径，用户总容量，用户已使用容量，用户容量百分比
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


# 获取新文件id
async def get_new_file_id(username: str) -> str:
    """
    获取新文件id
    :return: 新文件id
    """
    new_file_id = await uuid_utils.get_uuid()  # 生成文件id
    while await files_utils.verify_file_is_user(
        username, new_file_id
    ):  # 如果文件id已经存在，重新生成，直到文件id不存在
        new_file_id = await uuid_utils.get_uuid()
    return new_file_id


# 获取新文件夹id
async def get_new_folder_id(username: str) -> str:
    """
    获取新文件夹id
    :return: 新文件夹id
    """
    new_folder_id = await uuid_utils.get_uuid()  # 生成文件夹id
    while await files_utils.verify_folder_is_user(
        username, new_folder_id
    ):  # 如果文件夹id已经存在，重新生成，直到文件夹id不存在
        new_folder_id = await uuid_utils.get_uuid()
    return new_folder_id


# 获取文件类型对应的缩略图路径
async def get_thumbnail_path(file_type: str) -> str:
    """
    获取文件类型对应的缩略图路径
    :param file_type: 文件类型
    :return: 缩略图路径
    """
    if file_type:
        image_path = await db_operation.ShrinkTable_get_shrink(file_type)
    if image_path:
        return image_path
    return ""


# 获取用户头像路径
async def get_avatar_path(username: str) -> str:
    """
    获取用户头像路径
    :param username: 用户名
    :return: 用户头像路径
    """
    if username:
        return await db_operation.UsersTable_select_hpath(username)
    return ""
