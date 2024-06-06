import config
from typing import Optional
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


# 恢复被删除的文件
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
