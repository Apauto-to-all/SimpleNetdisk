from fastapi import APIRouter, Request, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    username: Optional[str] = Form(""),
    password: Optional[str] = Form(""),
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
        return {"message": "登录成功"}
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
