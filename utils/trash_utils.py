from db.connection import DatabaseOperation
from utils import get_data_utils

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
