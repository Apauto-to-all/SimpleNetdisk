from typing import Optional
from fastapi import APIRouter, Cookie, Request
from fastapi.templating import Jinja2Templates
from utils import user_utils, cpMove_utils

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# 进入文件树页面
@router.get("/cpMove")
async def cpMove(
    request: Request,  # 请求
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    return templates.TemplateResponse(
        "test-folders.html", {"request": request}
    )  # 返回文件树页面


# 获取父类文件夹下的所有子类文件夹
@router.get("/getfolders")
async def get_folders(
    parent_folder_id: Optional[str] = None,  # 添加查询参数
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    if not parent_folder_id:
        return {}
    username = await user_utils.isLogin_getUser(access_token)
    if not username:  # 判断是否登录
        return {}
    """
    {
        "uuid1": "folder_name1",
        "uuid2": "folder_name2",
    }
    """
    return await cpMove_utils.get_all_folder_from_parent_folder_id(
        username,
        parent_folder_id,
    )
