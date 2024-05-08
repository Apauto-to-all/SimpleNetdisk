from fastapi import FastAPI  # 导入 FastAPI 框架
from fastapi.responses import (
    HTMLResponse,  # 用于返回 HTML 响应
    RedirectResponse,  # 用于重定向
)
from fastapi.staticfiles import StaticFiles  # 静态文件目录
from controllers import login, register  # 导入登录和注册路由

app = FastAPI()  # 创建 FastAPI 实例
app.mount("/static", StaticFiles(directory="static"), name="static")  # 静态文件目录


@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/login")  # 重定向到登录页面


app.include_router(login.router)  # 注册登录路由
app.include_router(register.router)  # 注册注册路由
