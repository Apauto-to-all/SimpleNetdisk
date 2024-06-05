from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,
    Request,
    Cookie,  # 功能：用于操作 Cookie
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数
from utils import password_utils, user_utils, get_data_utils, files_utils
import config

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/index", response_class=HTMLResponse)
@router.get("/index/{folder_id}", response_class=HTMLResponse)
async def index(
    request: Request,  # 请求
    folder_id: Optional[str] = "/",  # 文件夹id，默认为根目录
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
    unlock_folder: Optional[str] = Cookie(None),  # 解密文件夹
):
    username = await user_utils.isLogin_getUser(access_token)  # 从 JWT 中获取用户名
    if not username:  # 判断是否登录
        response = RedirectResponse(url="/login", status_code=303)
        response.delete_cookie("access_token")  # 删除 Cookie
        return response
    if folder_id != "/" and not await files_utils.verify_folder_is_user(
        username, folder_id
    ):  # 判断文件夹id是否为用户的文件夹
        return RedirectResponse(url="/index", status_code=303)

    if folder_id != "/" and await files_utils.is_folder_encrypted(
        username, folder_id
    ):  # 判断文件夹是否被加密
        if not unlock_folder:
            return RedirectResponse(url="/index", status_code=303)
        if not await password_utils.verify_password(unlock_folder, folder_id):
            return RedirectResponse(url="/index", status_code=303)

    all_user = await get_data_utils.get_all_user(username)  # 获取用户的所有信息
    all_dict = await get_data_utils.get_all(
        username, folder_id
    )  # 获取所有文件夹和文件信息

    if unlock_folder:
        for i in all_dict.get("folders"):
            if i.get("password") and await password_utils.verify_password(
                unlock_folder, i.get("uuid")
            ):  # 判断文件夹是否被加密，并且被解密
                i["password"] = ""  # 解密文件夹
                break
    return templates.TemplateResponse(
        f"{config.test_prefix}index.html",
        {
            "request": request,
            "all_user": all_user,
            "all_dict": all_dict,
            "folder_id": folder_id,
        },
    )  # 否则进入网盘首页
