from pydantic import BaseModel
import config
from typing import List, Optional
from fastapi import APIRouter, Cookie, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import user_utils, trash_utils

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# 打开垃圾桶页面
@router.get("/trash")
async def open_trash_page(
    request: Request,  # 请求
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:  # 判断是否登录
        response = RedirectResponse(url="/login", status_code=303)
        response.delete_cookie("access_token")  # 删除 Cookie
        return response

    return templates.TemplateResponse(
        f"{config.test_prefix}trash.html", {"request": request}
    )  # 否则进入网盘首页


# 获取被删除的文件夹
@router.get("/trash/folder")
async def get_trash_folder(
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
) -> list:
    """
    获取所有被删除的文件夹
    """
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return []
    """
    return [
        {
            "uuid": "uuid",
            "folder_name": "文件夹名",
            "drop_time": "2024年6月5日",
            "delete_time": "2024年6月15日",
        },
        ……
    ]
    """
    return await trash_utils.get_trash_folders(username)  # 获取所有被删除的文件夹


# 获取被删除的文件
@router.get("/trash/file")
async def get_trash_file(
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    """
    获取所有被删除的文件
    """
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return []
    """
    return [
        {
            "uuid": "uuid",
            "file_name": "文件名",
            "drop_time": "2024年6月5日",
            "delete_time": "2024年6月15日",
        }，
        ……
    ]
    """
    return await trash_utils.get_trash_files(username)


class FItems(BaseModel):
    folders: List[str]
    files: List[str]


# 还原文件和文件夹
@router.post("/restore")
async def restore_items(
    items: FItems,
    access_token: Optional[str] = Cookie(None),
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "请先登录"}
    if not items.folders and not items.files:
        return {"error": "请选择要还原的文件或文件夹"}
    try:
        await trash_utils.restore_files_and_folders(
            username, {"folders": items.folders, "files": items.files}
        )  # 还原文件和文件夹
        return {"success": "还原成功"}
    except Exception as e:
        return {"error": "还原失败"}


# 永久删除文件和文件夹
@router.post("/delete_forever")
async def delete_forever_items(
    items: FItems,
    access_token: Optional[str] = Cookie(None),
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "请先登录"}
    if not items.folders and not items.files:
        return {"error": "请选择要删除的文件或文件夹"}
    try:
        await trash_utils.delete_forever_files_and_folders(
            username, {"folders": items.folders, "files": items.files}
        )  # 永久删除文件和文件夹
        return {"success": "删除成功"}
    except Exception as e:
        return {"error": "删除失败"}
