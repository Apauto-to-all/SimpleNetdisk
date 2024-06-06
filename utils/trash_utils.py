import os
from db.connection import DatabaseOperation
from utils import files_utils, get_data_utils

db_operation = DatabaseOperation()


# 获取被删除的文件夹信息，包括文件夹id，文件夹名，文件放入回收站的时间，文件删除的时间
async def get_trash_folders(username: str) -> list:
    list = await db_operation.TrashTable_get_all_folder(username)
    for i in list:
        i["drop_time"] = await get_data_utils.convert_time_to_chinese(i["drop_time"])
        i["delete_time"] = await get_data_utils.convert_time_to_chinese(
            i["delete_time"]
        )
    return list


# 获取被删除的文件信息，包括文件id，文件名，文件放入回收站的时间，文件删除的时间
async def get_trash_files(username: str) -> list:
    list = await db_operation.TrashTable_get_all_file(username)
    for i in list:
        i["drop_time"] = await get_data_utils.convert_time_to_chinese(i["drop_time"])
        i["delete_time"] = await get_data_utils.convert_time_to_chinese(
            i["delete_time"]
        )
    return list


# 还原被删除的文件夹和文件
async def restore_files_and_folders(username: str, items: dict):
    for folder_uuid in items.get("folders"):
        # 还原文件夹
        await db_operation.FolderTable_restore_folder(username, folder_uuid)
        # 删除垃圾桶表中的文件夹记录
        await db_operation.TrashTable_delete_folder(username, folder_uuid)
    for file_uuid in items.get("files"):
        # 还原文件
        await db_operation.FileTable_restore_file(username, file_uuid)
        # 删除垃圾桶表中的文件记录
        await db_operation.TrashTable_delete_file(username, file_uuid)


# 永久删除被删除的文件夹和文件
async def delete_forever_files_and_folders(username: str, items: dict):
    folder_list = []
    file_list = []
    folder_list.extend(items.get("folders", []))
    file_list.extend(items.get("files", []))
    for folder_uuid in items.get("folders"):
        # 获取到文件夹下的所有文件夹id信息
        folder_list.extend(
            await db_operation.FolderTable_get_all_folder_id(username, folder_uuid)
        )  # 获取到文件夹下的所有文件夹id信息
        # 删除垃圾桶表中的文件夹记录
        await db_operation.TrashTable_delete_folder(username, folder_uuid)

    # 去重
    folder_list = list(set(folder_list))
    # 获取到文件夹下的所有文件id信息
    for folder_uuid in folder_list:
        file_list.extend(
            await db_operation.FileTable_get_all_file_id_from_parent_folder(
                username, folder_uuid
            )
        )
    # 文件去重
    file_list = list(set(file_list))
    print(file_list)
    for file_uuid in file_list:
        file_dict = await files_utils.verify_and_return_files_info(username, file_uuid)
        if not file_dict:  # 如果文件信息不存在就继续
            continue
        file_path = file_dict.get("file_path")
        if not file_path:  # 如果文件路径不存在就继续
            continue
        # 修改文件复制次数，减一
        await db_operation.FileTable_update_cpnums_minus_one(
            username, file_path
        )  # 修改所有文件的复制次数，减一
        # 如果为0就删除文件
        if not await db_operation.FileTable_get_cpnums(
            username, file_uuid
        ):  # 获取文件的复制次数，如果为0就删除文件
            # 删除文件
            if os.path.exists(file_path):
                os.remove(file_path)

        if file_uuid in items.get("files"):  # 如果文件id在删除列表中
            # 删除垃圾桶表中的文件记录
            await db_operation.TrashTable_delete_file(username, file_uuid)
