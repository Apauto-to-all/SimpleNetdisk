import os
from typing import Optional
from fastapi import APIRouter, Cookie, File, Form, UploadFile
from fastapi.responses import RedirectResponse
import config  # 导入配置文件
from PIL import Image
from io import BytesIO

from utils import password_utils, user_utils

router = APIRouter()


# 修改用户头像
@router.post("/change_user_avatar")
async def change_user_avatar(
    avatarFile: UploadFile = File(...),
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        response = RedirectResponse(url="/login", status_code=303)
        response.delete_cookie("access_token")  # 删除 Cookie
        return response

    file_contents = await avatarFile.read()
    if file_contents > 4 * 10240:  # 限制文件大小为 4MB
        return {"error": "文件大小不能超过 4MB"}
    # 将文件转化为jpg文件，100*100大小
    # 将文件内容转换为图像
    image = Image.open(BytesIO(file_contents))

    # 按比例缩放图像，保持宽高比
    max_size = (100, 100)
    image.thumbnail(max_size)

    # 将图像转换为jpg格式
    image = image.convert("RGB")

    # 保存到磁盘
    path = os.path.join(config.user_avatar_path, f"{username}.jpg")
    image.save(path, "JPEG")
    # 更新数据库中的头像路径
    await user_utils.change_user_avatar_path(username, path)


# 修改用户昵称
@router.post("/change_user_nickname")
async def change_user_nickname(
    nickname: Optional[str] = Form(None),  # 读取表单数据
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        response = RedirectResponse(url="/login", status_code=303)
        response.delete_cookie("access_token")
        return response
    if nickname:
        await user_utils.change_user_nickname(username, nickname)
        return {"success": "修改昵称成功"}
    return {"error": "修改昵称失败"}


# 修改用户密码
@router.post("/change_user_password")
async def change_user_password(
    old_password: Optional[str] = Form(None),  # 读取表单数据
    password: Optional[str] = Form(None),  # 读取表单数据
    confirm_password: Optional[str] = Form(None),  # 读取表单数据
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        response = RedirectResponse(url="/login", status_code=303)
        response.delete_cookie("access_token")
        return response
    if old_password and password and confirm_password:
        if password != confirm_password:
            return {"error": "两次输入的密码不一致"}
        passwordFormat = password_utils.verify_get_password_format(
            password
        )  # 验证密码格式
        if passwordFormat:  # 如果密码格式错误，这里的 passwordFormat 是密码格式要求信息
            return {"error": passwordFormat}
        if await user_utils.verifyLogin(username, old_password):
            return {"error": "原密码错误"}
        await user_utils.change_user_password(username, password)
        return {"success": "修改密码成功"}
    return {"error": "请输入完整信息"}


# 获取用户名
@router.get("/get_username")
async def get_username(
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return "用户未登入"
    return username  # 返回用户名
