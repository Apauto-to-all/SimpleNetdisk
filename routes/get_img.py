import os
import random
from typing import Optional
from fastapi import APIRouter, Cookie, Response
from fastapi.responses import FileResponse
from captcha.image import ImageCaptcha  # 导入 ImageCaptcha 类，用于生成图片验证码
import string  # 导入 string 模块，用于生成验证码
from utils import get_data_utils, password_utils, user_utils
import config  # 导入配置文件

router = APIRouter()


@router.get("/captcha")  # 定义生成验证码的路由
async def getCaptcha():
    image_captcha = ImageCaptcha()  # 创建图片验证码对象
    captcha_text = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=4)
    )  # 生成随机验证码, 长度为 4，包含大写字母和数字
    data = image_captcha.generate(captcha_text)  # 生成图片验证码
    data.seek(0)  # 移动指针到文件开头
    response = Response(content=data.read(), media_type="image/png")  # 创建响应对象
    captcha_text = captcha_text.lower()  # 将验证码转换为小写
    response.set_cookie(
        key="hashed_captcha", value=await password_utils.encrypt_password(captcha_text)
    )  # 设置 cookie，存储加密后的验证码
    return response  # 返回图片验证码


@router.get("/user/avatar")  # 获取用户头像
async def get_avatar(access_token: Optional[str] = Cookie(None)):
    username = await user_utils.isLogin_getUser(access_token)  # 从 JWT 中获取用户名
    if username:  # 判断用户名是否存在
        img_path = await get_data_utils.get_avatar_path(username)  # 获取用户头像路径
        if not img_path or not os.path.exists(img_path):  # 判断头像是否存在
            img_path = f"{config.user_avatar_path}/default.jpg"  # 默认头像路径
        return FileResponse(img_path)  # 返回头像


@router.get("/thumbnail/{file_type}")  # 获取缩略图
async def get_thumbnail(file_type: str):
    if file_type == "folder":  # 判断文件类型是否为文件夹
        return FileResponse(f"{config.thumbnail_path}/default/folder.png")
    if file_type == "unknown":  # 判断文件类型是否为未知文件
        return FileResponse(f"{config.thumbnail_path}/default/unknown.png")

    img_path = await get_data_utils.get_thumbnail_path(file_type)  # 缩略图路径
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
