from fastapi import APIRouter, Request, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(
    request: Request,
    username: Optional[str] = Form(""),
    password: Optional[str] = Form(""),
    confirm_password: Optional[str] = Form(""),
):
    if not username or not password or not confirm_password:
        error_message = "用户名或密码不能为空"
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error_message": error_message,
                "username": username,
            },
        )
    if password != confirm_password:
        error_message = "两次密码不一致"
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error_message": error_message,
                "username": username,
            },
        )
    # 在这里添加你的用户注册逻辑
    return {"message": "注册成功"}
