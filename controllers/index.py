from fastapi import APIRouter, Request, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/index")
async def index(
    request: Request,
):
    return {"message": "登录成功"}
