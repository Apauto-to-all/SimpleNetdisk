from db.connection import DatabaseOperation
from utils import get_data_utils

db_operation = DatabaseOperation()


async def get_all_folder_from_parent_folder_id(
    username: str, parent_folder_id: str
) -> dict:
    """
    获取父类文件夹下的所有子类文件夹
    :param username: 用户名
    :param parent_folder_id: 父类文件夹 id
    :return: {
        "uuid1": "folder_name1",
        "uuid2": "folder_name2",
    }
    """
    if username and parent_folder_id:
        return await db_operation.FolderTable_get_all_folders_from_parent_folder_cpMove(
            username,
            parent_folder_id,
        )
    return {}


# 移动文件夹和文件
async def move_files_and_folders(
    username: str,  # 用户名
    target_folder_id: str,  # 目标文件夹 id
    files_id_list: list,  # 文件 id 列表
    folders_id_list: list,  # 文件夹 id 列表
):
    """
    移动文件夹和文件
    :param username: 用户名
    :param target_folder_id: 目标文件夹 id
    :param files_id_list: 文件 id 列表
    :param folders_id_list: 文件夹 id 列表
    """
    if username and target_folder_id:
        if files_id_list:  # 如果有文件 id 列表
            for file_id in files_id_list:  # 遍历文件 id 列表
                await db_operation.FileTable_move_file(  # 移动文件
                    username,
                    target_folder_id,
                    file_id,
                )
        if folders_id_list:  # 如果有文件夹 id 列表
            for folder_id in folders_id_list:
                await db_operation.FolderTable_move_folder(  # 移动文件夹
                    username,
                    target_folder_id,
                    folder_id,
                )
                await move_files_and_folders(  # 递归移动文件夹和文件
                    username,
                    folder_id,
                    [],
                    await db_operation.FolderTable_get_all_file_id_from_parent_folder(
                        username,
                        folder_id,
                    ),
                )


# 复制文件夹和文件
async def copy_files_and_folders(
    username: str,  # 用户名
    target_folder_id: str,  # 目标文件夹 id
    files_id_list: list,  # 文件 id 列表
    folders_id_list: list,  # 文件夹 id 列表
):
    """
    复制文件夹和文件
    :param username: 用户名
    :param target_folder_id: 目标文件夹 id
    :param files_id_list: 文件 id 列表
    :param folders_id_list: 文件夹 id 列表
    """
    if username and target_folder_id:
        if files_id_list:  # 如果有文件 id 列表
            for file_id in files_id_list:  # 遍历文件 id 列表
                new_file_id = await get_data_utils.get_new_file_id(
                    username
                )  # 获取新文件 id
                await db_operation.FileTable_copy_file(  # 复制文件
                    username,
                    target_folder_id,
                    file_id,
                    new_file_id,
                )
        if folders_id_list:  # 如果有文件夹 id 列表
            for folder_id in folders_id_list:
                # 获取新文件夹 id
                new_folder_id = await get_data_utils.get_new_folder_id(
                    username
                )  # 获取新文件夹 id
                await db_operation.FolderTable_copy_folder(  # 复制文件夹
                    username,
                    target_folder_id,
                    folder_id,
                    new_folder_id,
                )
                # 递归复制文件夹和文件
                await copy_files_and_folders(
                    username,
                    new_folder_id,
                    await db_operation.FileTable_get_all_file_id_from_parent_folder(
                        username,
                        folder_id,
                    ),
                    await db_operation.FolderTable_get_all_file_id_from_parent_folder(
                        username,
                        folder_id,
                    ),
                )  # 递归复制文件夹和文件
