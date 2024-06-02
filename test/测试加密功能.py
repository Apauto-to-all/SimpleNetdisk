from utils import jwt_token, password_utils, uuid_utils

# 生成uuid
uuid = await uuid_utils.get_uuid()
print(uuid)

# 加密密码
password = "123456"
hashed_password = await password_utils.encrypt_password(password)
print(hashed_password)

# 解密密码
print(password_utils.verify_password(hashed_password, password))

# 生成JWT
user = "test"
access_token = await jwt_token.get_access_jwt(user)
print(access_token)

# 验证JWT
print(jwt_token.get_user_from_jwt(access_token))
