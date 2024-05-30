import os
from typing import Optional
from fastapi import APIRouter, Cookie, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import config
from utils import user_utils, files_utils

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
    parent_folder_id = files_utils.get_delete_file_parent_folder_id(username, file_id)
    if parent_folder_id:
        if parent_folder_id == "/":
            return RedirectResponse(url="/index", status_code=303)
        return RedirectResponse(url=f"/index/{parent_folder_id}", status_code=303)
    return {"error": "删除失败"}
