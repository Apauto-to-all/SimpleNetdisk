from utils import uuid_utils

print(uuid_utils.get_uuid())

uuid_str = ""
for i in range(10):
    uuid_str += uuid_utils.get_uuid()

print(uuid_utils.split_uuids(uuid_str))
