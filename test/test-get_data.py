from utils.get_data_utils import get_all_user, get_all, get_all_trash, get_trash_files

print(await get_all_user("admin"))
print(await get_all("admin", "1"))
print(get_all_trash("admin"))
