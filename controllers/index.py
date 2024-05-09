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

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/index", response_class=HTMLResponse)
async def index(request: Request, access_token: Optional[str] = Cookie(None)):
    if access_token != "token":
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("index.html", {"request": request})
