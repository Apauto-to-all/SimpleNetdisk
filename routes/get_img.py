import os
from typing import Optional
from fastapi import APIRouter, Cookie, Response
from fastapi.responses import FileResponse

from utils import user_utils
import config  # 导入配置文件

router = APIRouter()


@router.get("/user/avatar")  # 获取用户头像
async def get_avatar(access_token: Optional[str] = Cookie(None)):
    username = await user_utils.isLogin_getUser(access_token)  # 从 JWT 中获取用户名
    if username:  # 判断用户名是否存在
        img_path = f"{config.user_avatar_path}/{username}.jpg"  # 头像路径
        if not os.path.exists(img_path):  # 判断头像是否存在
            img_path = f"{config.user_avatar_path}/default.jpg"  # 默认头像路径
        return FileResponse(img_path)  # 返回头像


@router.get("/thumbnail/{file_type}")  # 获取缩略图
async def get_thumbnail(file_type: str):
    if file_type == "folder":  # 判断文件类型是否为文件夹
        return FileResponse(f"{config.thumbnail_path}/default/folder.png")
    if file_type == "unknown":  # 判断文件类型是否为未知文件
        return FileResponse(f"{config.thumbnail_path}/default/unknown.png")
    img_path = f"{config.thumbnail_path}/default/{file_type}.png"  # 缩略图路径
    if os.path.exists(img_path):  # 判断缩略图是否存在
        return FileResponse(img_path)  # 返回缩略图

    return FileResponse(
        f"{config.thumbnail_path}/default/default.png"
    )  # 返回默认缩略图


@router.get("/folder/{lock_str}")  # 获取文件夹锁/解锁图标
async def get_folder_lock(lock_str: str):
    if lock_str == "lock":
        return FileResponse(f"{config.folder_lock_path}/lock.png")
    else:
        return FileResponse(f"{config.folder_lock_path}/unlock.png")


@router.get("/favicon.ico")  # 获取网站图标
async def get_favicon():
    return FileResponse("static/favicon.ico", media_type="image/x-icon")  # 返回网站图标
