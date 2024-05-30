import os
from typing import Optional
from fastapi import APIRouter, Cookie, Form, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import config
from utils import password_utils, user_utils, files_utils

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 下载文件的路由
@router.get("/download")
async def download_file(
    file_id: Optional[str] = None,  # 添加查询参数
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    # 判断是否登录
    username = user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    file_dict = files_utils.verify_and_return_files_info(username, file_id)
    if not file_dict:
        return {"error": "文件不存在"}
    file_path = file_dict.get("file_path")
    file_name = file_dict.get("file_name")
    # 使用原始文件路径拼接文件路径
    down_file_path = os.path.join(config.user_files_path, file_path)
    if not os.path.exists(down_file_path):
        return {"error": "因无法预料的原因，文件消失了"}

    return FileResponse(
        path=down_file_path,
        filename=file_name,
    )


# 删除文件的路由
@router.get("/delete")
async def delete_file(
    file_id: Optional[str] = None,  # 添加查询参数
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    # 判断是否登录
    username = user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    # 获取被删除文件的父级文件夹id
    parent_folder_id = files_utils.delete_file_get_parent_folder_id(username, file_id)
    if parent_folder_id:
        return RedirectResponse(url=f"/index/{parent_folder_id}", status_code=303)
    return {"error": "删除失败"}


# 重命名文件的路由
@router.post("/rename")
async def rename_file(
    file_id: Optional[str] = None,  # 添加查询参数
    folder_id: Optional[str] = None,  # 添加查询参数
    new_file_name: Optional[str] = Form(None),  # 读取表单数据
    new_folder_name: Optional[str] = Form(None),  # 读取表单数据
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    # 判断是否登录
    username = user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    if file_id and new_file_name:  # 重命名文件
        parent_folder_id = files_utils.rename_file_get_parent_folder_id(
            username,
            file_id,
            new_file_name,
        )
        if parent_folder_id:
            return RedirectResponse(url=f"/index/{parent_folder_id}", status_code=303)
    if folder_id and new_folder_name:  # 重命名文件夹
        parent_folder_id = files_utils.rename_folder_get_parent_folder_id(
            username,
            folder_id,
            new_folder_name,
        )
        if parent_folder_id:
            return RedirectResponse(url=f"/index/{parent_folder_id}", status_code=303)

    return {"error": "重命名失败"}


# 加密文件夹
@router.post("/encrypt")
async def encrypt_folder(
    folder_id: Optional[str] = None,  # 添加查询参数
    password: Optional[str] = Form(None),  # 读取表单数据
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    # 判断是否登录
    username = user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    if folder_id and password:
        parent_folder_id = files_utils.encrypt_folder_get_parent_folder_id(
            username,
            folder_id,
            password,
        )
        if parent_folder_id:
            return RedirectResponse(url=f"/index/{parent_folder_id}", status_code=303)
    return {"error": "加密失败"}


# 解密文件夹
@router.post("/decrypt")
async def decrypt_folder(
    # 临时解密还是删除加密
    folder_id: Optional[str] = None,  # 添加查询参数
    is_temporary: Optional[bool] = Form(False),  # 读取表单数据
    password: Optional[str] = Form(None),  # 读取表单数据
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    # 判断是否登录
    username = user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    if folder_id and password:
        parent_folder_id = files_utils.decrypt_folder_get_parent_folder_id(
            username,
            folder_id,
            password,
            is_temporary,
        )
        if parent_folder_id:
            response = RedirectResponse(
                url=f"/index/{parent_folder_id}", status_code=303
            )
            if is_temporary:
                response.set_cookie(
                    key=f"folder-{folder_id}",
                    value=password_utils.encrypt_password(folder_id),
                )
            return response
    return {"error": "解密失败"}
