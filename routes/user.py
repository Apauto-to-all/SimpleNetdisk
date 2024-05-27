from typing import Optional
from fastapi import APIRouter, Cookie, Response

from utils import user_utils
import config

router = APIRouter()


@router.get("/user/avatar")
async def get_avatar(access_token: Optional[str] = Cookie(None)):
    username = user_utils.isLogin_getUser(access_token)  # 从 JWT 中获取用户名
    if username:  # 判断用户名是否存在
        img_path = f"{config.user_avatar_path}/{username}.jpg"  # 头像路径
        with open(img_path, "rb") as f:
            img_data = f.read()  # 读取头像
        return Response(content=img_data, media_type="image/jpeg")  # 返回头像
