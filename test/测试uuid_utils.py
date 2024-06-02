from utils import uuid_utils

print(await uuid_utils.get_uuid())

uuid_str = ""
for i in range(10):
    uuid_str += await uuid_utils.get_uuid()

print(await uuid_utils.split_uuids(uuid_str))
