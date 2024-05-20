from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,  # 功能：用于接收请求
    Request,  # 功能：用于接收请求
    Form,  # 功能：用于接收表单数据
    Response,  # 功能：用于返回响应
    Cookie,  # 功能：用于操作 Cookie
)  # 导入 FastAPI 框架
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import (
    HTMLResponse,  # 用于返回 HTML 响应
    RedirectResponse,  # 用于重定向
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # 模板目录


@router.get("/login", response_class=HTMLResponse)
async def login(
    request: Request,  # 用于接收请求
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    if access_token == "token":
        return RedirectResponse(url="/index", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    username: Optional[str] = Form(""),  # 获取用户名
    password: Optional[str] = Form(""),  # 获取密码
):
    if not username or not password:
        error_message = "用户名或密码不能为空"
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error_message": error_message,
                "username": username,
            },
        )
    if username == "admin" and password == "passwd":
        # 控制登入成功后的跳转，并设置 Cookie
        response = RedirectResponse(url="/index", status_code=303)
        response.set_cookie(
            key="access_token", value="token", max_age=10 * 24 * 60 * 60
        )
        return response
    else:
        error_message = "用户名或密码错误"
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error_message": error_message,
                "username": username,
            },
        )
