# 验证文件夹id是否为用户的文件夹
import os
from utils import password_utils, uuid_utils
import config


def verify_folder_is_user(username: str, folder_id: str) -> bool:
    """
    验证文件夹id是否为用户的文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 是否为用户的文件夹
    """
    if username and folder_id:
        return True


def verify_file_is_user(username: str, file_id: str) -> bool:
    """
    验证文件id是否为用户的文件
    :param username: 用户名
    :param file_id: 文件id
    :return: 是否为用户的文件
    """
    if username == "admin" and file_id == "aaa":
        return True
    return False


# 验证并放回文件信息
def verify_and_return_files_info(username: str, file_id: str) -> dict:
    """
    验证并返回文件信息
    :param username: 用户名
    :param file_id: 文件id
    :return: 文件路径，文件名
    """
    if username and file_id:
        file_path = "f1/1.jpg"
        file_name = "图片.jpg"
        return {
            "file_path": file_path,
            "file_name": file_name,
        }
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
def delete_file_get_parent_folder_id(username: str, file_id: str) -> str:
    """
    删除文件
    :param username: 用户名
    :param file_id: 文件id
    :return: 父级文件夹id
    """
    if username and file_id:
        return "/"
    return ""  # 删除失败


# 删除文件夹，获取父级文件夹id
def delete_folder_get_parent_folder_id(username: str, folder_id: str) -> str:
    """
    删除文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 父级文件夹id
    """
    if username and folder_id:
        return "/"
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


def rename_file_get_parent_folder_id(
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
        return "/"
    return ""  # 重命名失败


def rename_folder_get_parent_folder_id(
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
        return "/"
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
        return "/"
    return ""  # 加密失败


def get_folder_password(username: str, folder_id: str) -> str:
    if username and folder_id:
        return (
            "$2b$12$RnKEz5vMMQW6zZ1/1fNntesE3dF88VDXHXa9XA4Mx7V6Ik.loMd0S"  # password
        )
    return ""  # 获取密码失败


def rm_folder_password(username: str, folder_id: str) -> bool:
    """
    删除文件夹密码
    :param username: 用户名
    :param folder_id: 文件夹id
    :return 如何删除密码成功就返回Treu，否则False
    """
    if username and folder_id:
        return True
    return False


async def decrypt_folder_get_parent_folder_id(
    username: str, folder_id: str, password: str, is_temporary: bool
) -> str:
    """
    解密文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :param password: 密码
    :param is_temporary: 临时解密还是删除加密
    :return: 父级文件夹id
    """
    if username and folder_id and password:
        hashed_password = get_folder_password(username, folder_id)
        if await password_utils.verify_password(hashed_password, password):
            if not is_temporary:  # 删除密码，永久实现
                rm_folder_password(username, folder_id)  # 删除文件夹密码
            return "/"
    return ""  # 解密失败


def is_folder_encrypted(username: str, folder_id: str) -> bool:
    """
    判断文件夹是否加密
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 是否加密，True 为加密，False 为未加密
    """
    if username and folder_id:
        return False
    return True


def get_parent_folder_id_is_locked(username: str, file_id: str) -> str:
    """
    如果文件的父级文件夹被加密，返回父级文件夹id，否则返回空字符串
    :param username: 用户名
    :param file_id: 文件id
    :return: 父级文件夹id
    """
    if username and file_id:
        return "/"
    return ""  # 获取失败


def create_folder_get_folder_id(username: str, folder_id: str, folder_name: str) -> str:
    """
    创建文件夹
    :param username: 用户名
    :param folder_id: 父级文件夹id
    :param folder_name: 文件夹名
    :return: 文件夹id
    """
    if username and folder_id and folder_name:
        new_folder_id = uuid_utils.get_uuid()
        return new_folder_id
    return ""  # 创建失败


def get_file_path(username: str) -> str:
    """
    获取用户的文件路径
    :param username: 用户名
    :return: 文件路径
    """
    if username:
        file_path = os.path.join(config.user_files_path, username)  # 用户的文件夹
        if not os.path.exists(file_path):  # 如果文件夹不存在，创建文件夹
            os.makedirs(file_path)
        return file_path
    return ""  # 获取失败


def save_file_get_file_id(username: str, file_name: str, file_size_kb: str) -> str:
    """
    保存文件
    :param username: 用户名
    :param file_name: 文件名
    :param file_size_kb: 文件大小
    :return: 文件id
    """
    if username and file_name and file_size_kb:  # 保存文件
        new_file_id = uuid_utils.get_uuid()  # 生成文件id
        while verify_file_is_user(
            username, new_file_id
        ):  # 如果文件id已经存在，重新生成，直到文件id不存在
            new_file_id = uuid_utils.get_uuid()

        user_all_file_path = os.path.join(
            config.user_files_path, username
        )  # 用户的文件夹
        if not os.path.exists(user_all_file_path):  # 如果文件夹不存在，创建文件夹
            os.makedirs(user_all_file_path)  # 创建用户的文件夹

        file_path = os.path.join(user_all_file_path, new_file_id)
        if username and file_name and file_path and file_size_kb:  # 保存文件
            return new_file_id
    return ""  # 保存失败
