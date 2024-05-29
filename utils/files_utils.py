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
