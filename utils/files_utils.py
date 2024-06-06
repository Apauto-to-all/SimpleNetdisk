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


# 验证并返回文件信息
async def verify_and_return_files_info(username: str, file_id: str) -> dict:
    """
    验证并返回文件信息，文件名和文件路径
    :param username: 用户名
    :param file_id: 文件id
    :return: 文件路径，文件名
    """
    if username and file_id:
        return await db_operation.FileTable_get_name_path(username, file_id)
    return {}


# 删除文件
async def delete_file(username: str, file_id: str) -> bool:
    """
    删除文件
    :param username: 用户名
    :param file_id: 文件id
    :return: 是否删除成功，True 为删除成功，False 为删除失败
    """
    if username and file_id:
        await db_operation.FileTable_delete(username, file_id)
        await db_operation.TrashTable_insert(username, file_id=file_id)
        return True
    return False  # 删除失败


# 删除文件夹，删除成功返回True，失败返回False
async def delete_folder(username: str, folder_id: str) -> bool:
    """
    删除文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 是否删除成功，True 为删除成功，False 为删除失败
    """
    if username and folder_id:
        await db_operation.FolderTable_delete(username, folder_id)
        await db_operation.TrashTable_insert(username, folder_id=folder_id)
        return True
    return False  # 删除失败


# 重命名文件，成功返回True，失败返回False
async def rename_file(username: str, file_id: str, new_file_name: str) -> bool:
    """
    重命名文件
    :param username: 用户名
    :param file_id: 文件id
    :param new_file_name: 新文件名
    :return: True 为重命名成功，False 为重命名失败
    """
    if username and file_id and new_file_name:
        parent_folder = await db_operation.FileTable_get_parent_folder_id(
            username, file_id
        )
        if parent_folder:
            new_file_name = await auto_rename_file(
                username, parent_folder, new_file_name
            )  # 重命名文件
            await db_operation.FileTable_rename_file(
                username, file_id, new_file_name
            )  # 重命名文件
            return True
    return False  # 重命名失败


# 重命名文件夹
async def rename_folder(username: str, folder_id: str, new_folder_name: str) -> bool:
    """
    重命名文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :param new_folder_name: 新文件夹名
    :return: True 为重命名成功，False 为重命名失败
    """
    if username and folder_id and new_folder_name:
        parent_folder = await db_operation.FolderTable_get_parent_folder_id(
            username, folder_id
        )
        if parent_folder:
            new_folder_name = await auto_rename_folder(
                username, parent_folder, new_folder_name
            )  # 重命名文件夹
            await db_operation.FolderTable_rename_folder(
                username, folder_id, new_folder_name
            )
            return True
    return False  # 重命名失败


# 加密文件夹，True 为加密成功，False 为加密失败
async def encrypt_folder(username: str, folder_id: str, password: str) -> bool:
    """
    加密文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :param password: 密码
    :return: True 为加密成功，False 为加密失败
    """
    if username and folder_id and password:
        password = await password_utils.encrypt_password(password)
        await db_operation.FolderTable_encrypt_folder(username, folder_id, password)
        return True
    return False  # 加密失败


# 解密文件夹，True 为解密成功，False 为解密失败
async def decrypt_folder(
    username: str, folder_id: str, password: str, is_permanent: bool
) -> bool:
    """
    解密文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :param password: 密码
    :param is_permanent: 临时解密还是删除加密
    :return: True 为解密成功，False 为解密失败
    """
    if username and folder_id and password:
        hashed_password = await db_operation.FolderTable_get_password(
            username, folder_id
        )
        if await password_utils.verify_password(hashed_password, password):
            if is_permanent:  # 删除密码，永久解密
                await db_operation.FolderTable_delete_password(username, folder_id)
            return True

    return False  # 解密失败


# 判断文件夹是否加密
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


# 获取文件夹id，如果文件的父级文件夹被加密，返回父级文件夹id，否则返回空字符串
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


# 创建文件夹
async def create_folder_get_folder_id(
    username: str, parent_folder_id: str, folder_name: str
) -> str:
    """
    创建文件夹
    :param username: 用户名
    :param parent_folder_id: 父级文件夹id
    :param folder_name: 文件夹名
    :return: 文件夹id
    """
    if username and parent_folder_id and folder_name:
        new_folder_id = await uuid_utils.get_uuid()
        while await verify_folder_is_user(username, new_folder_id):
            new_folder_id = await uuid_utils.get_uuid()
        folder_name = await auto_rename_folder(
            username, parent_folder_id, folder_name
        )  # 重命名文件夹，如果文件夹名重复，则重命名
        await db_operation.FolderTable_insert(
            username, new_folder_id, parent_folder_id, folder_name
        )
        return new_folder_id
    return ""  # 创建失败


# 保存文件，获取文件id
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
        # 文件路径
        file_path = os.path.join(user_all_file_path, new_file_id)
        # 如果命名重复，则重新命名，file_name
        file_name = await auto_rename_file(username, parent_folder, file_name)
        # 保存文件
        await db_operation.FileTable_insert(
            username,
            new_file_id,
            parent_folder,
            file_name,
            file_size_kb,
            file_path,
        )
        # 更新用户使用容量
        await db_operation.UsersTable_update_uspace(username, file_size_kb)
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
        # 获取用户的所有信息
        user_all = await db_operation.UsersTable_select_all(username)
        # 用户使用容量 + 文件大小 > 最大容量
        capacity_used = user_all.get("capacity_used")
        # 用户总容量
        capacity_total = user_all.get("capacity_total")
        # 返回是否超过最大容量
        return int(capacity_used) + int(file_size_kb) > int(capacity_total)
    return False  # 没有超过最大容量


# 自动重命名文件
async def auto_rename_file(username: str, parent_folder: str, file_name: str) -> str:
    """
    自动重命名文件
    :param username: 用户名
    :param file_name: 文件名
    :param parent_folder: 父文件夹id
    :return: 文件名
    """
    new_file_name = file_name
    if username and file_name and parent_folder:
        counter = 1
        file_name_without_ext = os.path.splitext(file_name)[0]  # 文件名不带扩展名
        extension = os.path.splitext(file_name)[1]  # 扩展名
        # 验证文件名是否存在，命名重复，则重新命名
        while await db_operation.FileTable_verify_name_only(
            username, parent_folder, new_file_name
        ):
            if extension:
                new_file_name = f"{file_name_without_ext}_{counter}{extension}"
            else:
                new_file_name = f"{file_name_without_ext}_{counter}"
            counter += 1
    return new_file_name


# 自动重命名文件夹
async def auto_rename_folder(
    username: str, parent_folder: str, folder_name: str
) -> str:
    """
    自动重命名文件夹
    :param username: 用户名
    :param folder_name: 文件夹名
    :param parent_folder: 父文件夹id
    :return: 文件夹名
    """
    new_folder_name = folder_name
    if username and folder_name and parent_folder:
        counter = 1
        # 验证文件夹名是否存在，命名重复，则重新命名
        while await db_operation.FolderTable_verify_name_only(
            username, parent_folder, new_folder_name
        ):
            new_folder_name = f"{folder_name}_{counter}"
            counter += 1
    return new_folder_name
