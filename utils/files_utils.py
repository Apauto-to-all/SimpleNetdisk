# 验证文件夹id是否为用户的文件夹
import os
from utils import password_utils, uuid_utils
import config
from db.connection import DatabaseOperation  # 导入数据库操作类

db_operation = DatabaseOperation()  # 实例化数据库操作类


async def is_folder_has_folder(username: str, folder_id: str) -> bool:
    """
    验证文件夹是否有文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 是否有文件夹
    """
    if username and folder_id:
        return await db_operation.FolderTable_has_folder(username, folder_id)
    return False


async def verify_folder_is_user(username: str, folder_id: str) -> bool:
    """
    验证文件夹id是否为用户的文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 是否为用户的文件夹
    """
    if await db_operation.FolderTable_verify(username, folder_id):
        return True
    return False


async def verify_file_is_user(username: str, file_id: str) -> bool:
    """
    验证文件id是否为用户的文件
    :param username: 用户名
    :param file_id: 文件id
    :return: 是否为用户的文件
    """
    if username and file_id:
        return await db_operation.FileTable_verify(username, file_id)
    return False


# 验证并放回文件信息
async def verify_and_return_files_info(username: str, file_id: str) -> dict:
    """
    验证并返回文件信息
    :param username: 用户名
    :param file_id: 文件id
    :return: 文件路径，文件名
    """
    if username and file_id:
        return await db_operation.FileTable_get_name_path(username, file_id)
    return {}


# 获取文件夹内的文件夹
def get_folders_in_folder(username: str, folder_id: str) -> list:
    """
    获取文件夹内的文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 文件夹列表
    """
    if username and folder_id:
        return [
            {
                "folder_id": "1",
                "folder_name": "文件夹1",
                "folder_path": "f1",
                "folder_size": "0",
                "folder_create_time": "2021-08-01 12:00:00",
            },
            {
                "folder_id": "2",
                "folder_name": "文件夹2",
                "folder_path": "f2",
                "folder_size": "0",
                "folder_create_time": "2021-08-01 12:00:00",
            },
        ]
    return []


# 删除文件，获取父级文件夹id
async def delete_file_get_parent_folder_id(username: str, file_id: str) -> str:
    """
    删除文件
    :param username: 用户名
    :param file_id: 文件id
    :return: 父级文件夹id
    """
    if username and file_id:
        return await db_operation.FileTable_delete_get_parent_folder_id(
            username, file_id
        )
    return ""  # 删除失败


# 删除文件夹，获取父级文件夹id
async def delete_folder_get_parent_folder_id(username: str, folder_id: str) -> str:
    """
    删除文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 父级文件夹id
    """
    if username and folder_id:
        await db_operation.FolderTable_delete(username, folder_id)
        return await db_operation.FolderTable_get_parent_folder_id(username, folder_id)
    return ""  # 删除失败


# 获取父级文件夹id
def get_parent_folder_id(username: str, folder_id: str) -> str:
    """
    获取父级文件夹id
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 父级文件夹id
    """
    if username and folder_id:
        return "/"
    return ""  # 删除失败


async def rename_file_get_parent_folder_id(
    username: str, file_id: str, new_file_name: str
) -> str:
    """
    重命名文件
    :param username: 用户名
    :param file_id: 文件id
    :param new_file_name: 新文件名
    :return: 父级文件夹id
    """
    if username and file_id and new_file_name:
        return await db_operation.FileTable_rename_file_get_parent_folder_id(
            username, file_id, new_file_name
        )
    return ""  # 重命名失败


async def rename_folder_get_parent_folder_id(
    username: str, folder_id: str, new_folder_name: str
) -> str:
    """
    重命名文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :param new_folder_name: 新文件夹名
    :return: 父级文件夹id
    """
    if username and folder_id and new_folder_name:
        await db_operation.FolderTable_rename_folder(
            username, folder_id, new_folder_name
        )
        return await db_operation.FolderTable_get_parent_folder_id(username, folder_id)
    return ""  # 重命名失败


async def encrypt_folder_get_parent_folder_id(
    username: str, folder_id: str, password: str
) -> str:
    """
    加密文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :param password: 密码
    :return: 父级文件夹id
    """
    if username and folder_id and password:
        password = await password_utils.encrypt_password(password)
        await db_operation.FolderTable_encrypt_folder(username, folder_id, password)
        return await db_operation.FolderTable_get_parent_folder_id(username, folder_id)
    return ""  # 加密失败


async def decrypt_folder_get_parent_folder_id(
    username: str, folder_id: str, password: str, is_permanent: bool
) -> str:
    """
    解密文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :param password: 密码
    :param is_permanent: 临时解密还是删除加密
    :return: 父级文件夹id
    """
    if username and folder_id and password:
        hashed_password = await db_operation.FolderTable_get_password(
            username, folder_id
        )
        if await password_utils.verify_password(hashed_password, password):
            if is_permanent:  # 删除密码，永久解密
                await db_operation.FolderTable_delete_password(username, folder_id)
            return await db_operation.FolderTable_get_parent_folder_id(
                username, folder_id
            )
    return ""  # 解密失败


async def is_folder_encrypted(username: str, folder_id: str) -> bool:
    """
    判断文件夹是否加密
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 是否加密，True 为加密，False 为未加密
    """
    if username and folder_id:
        return (
            True
            if await db_operation.FolderTable_get_password(username, folder_id)
            else False
        )
    return True


async def get_parent_folder_id_is_locked(username: str, file_id: str) -> str:
    """
    如果文件的父级文件夹被加密，返回父级文件夹id，否则返回空字符串
    :param username: 用户名
    :param file_id: 文件id
    :return: 父级文件夹id
    """
    if username and file_id:
        return await db_operation.FileTable_get_lock_parent_folder_id(username, file_id)
    return ""  # 获取失败


async def create_folder_get_folder_id(
    username: str, folder_id: str, folder_name: str
) -> str:
    """
    创建文件夹
    :param username: 用户名
    :param folder_id: 父级文件夹id
    :param folder_name: 文件夹名
    :return: 文件夹id
    """
    if username and folder_id and folder_name:
        new_folder_id = await uuid_utils.get_uuid()
        while await verify_folder_is_user(username, new_folder_id):
            new_folder_id = await uuid_utils.get_uuid()
        await db_operation.FolderTable_insert(
            username, new_folder_id, folder_id, folder_name
        )
        return new_folder_id
    return ""  # 创建失败


async def save_file_get_file_id(
    username: str, file_name: str, file_size_kb: str, parent_folder: str
) -> str:
    """
    保存文件
    :param username: 用户名
    :param file_name: 文件名
    :param file_size_kb: 文件大小
    :param parent_folder: 父文件夹id
    :return: 文件id
    """
    if username and file_name and parent_folder:  # 保存文件
        new_file_id = await uuid_utils.get_uuid()  # 生成文件id
        while await verify_file_is_user(
            username, new_file_id
        ):  # 如果文件id已经存在，重新生成，直到文件id不存在
            new_file_id = await uuid_utils.get_uuid()

        user_all_file_path = os.path.join(
            config.user_files_path, username
        )  # 用户的文件夹
        if not os.path.exists(user_all_file_path):  # 如果文件夹不存在，创建文件夹
            os.makedirs(user_all_file_path)  # 创建用户的文件夹

        file_path = os.path.join(user_all_file_path, new_file_id)
        await db_operation.FileTable_insert(
            username,
            new_file_id,
            parent_folder,
            file_name,
            file_size_kb,
            file_path,
        )
        return new_file_id
    return ""  # 保存失败


# 检测上传的文件后，使用容量是否超过最大容量
async def verify_capacity_exceeded(username: str, file_size_kb: str) -> bool:
    """
    检测上传的文件后，使用容量是否超过最大容量
    :param username: 用户名
    :param file_size_kb: 文件大小
    :return: 是否超过最大容量
    """
    if username and file_size_kb:
        user_all = await db_operation.UsersTable_select_all(username)
        capacity_used = user_all.get("capacity_used")
        capacity_total = user_all.get("capacity_total")
        return int(capacity_used) + int(file_size_kb) > int(capacity_total)
    return False  # 没有超过最大容量
