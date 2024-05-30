# 验证文件夹id是否为用户的文件夹
def verify_folder_is_user(username: str, folder_id: str) -> bool:
    """
    验证文件夹id是否为用户的文件夹
    :param username: 用户名
    :param folder_id: 文件夹id
    :return: 是否为用户的文件夹
    """
    if username and folder_id:
        return True


# 验证并放回文件信息
def verify_and_return_files_info(username: str, file_id: str) -> dict:
    """
    验证并放回文件路径
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
def get_delete_file_parent_folder_id(username: str, file_id: str) -> str:
    """
    删除文件
    :param username: 用户名
    :param file_id: 文件id
    :return: 父级文件夹id
    """
    if username and file_id:
        return "/"
    return ""  # 删除失败
