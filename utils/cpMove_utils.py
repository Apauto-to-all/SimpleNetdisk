from db.connection import DatabaseOperation

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
