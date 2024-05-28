from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,
    Request,
    Form,
    HTTPException,
    status,
    Cookie,  # 功能：用于操作 Cookie
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数
from utils import user_utils
import config

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/index", response_class=HTMLResponse)
async def index(
    request: Request,
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    if not user_utils.isLogin_getUser(access_token):  # 如果未登录，或者登录状态过期
        return RedirectResponse(url="/login", status_code=303)  # 重定向到登录页面

    return templates.TemplateResponse(
        f"{config.test_prefix}index.html", {"request": request}
    )  # 否则进入网盘首页
