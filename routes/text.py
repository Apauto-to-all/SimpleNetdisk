from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

router = APIRouter()
templates = Jinja2Templates(directory="templates")

data = [
    {"text": "Button 1", "value": "value1"},
    {"text": "Button 2", "value": "value2"},
    {"text": "Button 3", "value": "value3"},
    {"text": "测试文本", "value": "测试"},
]


@router.get("/text", response_class=HTMLResponse)
async def text(request: Request):
    return templates.TemplateResponse(
        f"test-dynamic.html", {"request": request, "data": data}
    )
