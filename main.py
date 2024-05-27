from fastapi import FastAPI, Cookie  # 导入 FastAPI 框架
from fastapi.responses import (
    HTMLResponse,  # 用于返回 HTML 响应
    RedirectResponse,  # 用于重定向
)
from fastapi.staticfiles import StaticFiles  # 静态文件目录
from routes import login, register, index, upload, down, text, captcha, logout, user
import config  # 导入配置文件
from typing import Optional
from utils import user_utils

app = FastAPI()  # 创建 FastAPI 实例
app.mount("/static", StaticFiles(directory="static"), name="static")  # 静态文件目录


@app.get("/", response_class=HTMLResponse)
async def root(
    access_token: Optional[str] = Cookie(None),
):
    if user_utils.isLogin_getUser(access_token):  # 判断是否登录
        return RedirectResponse(url="/index", status_code=303)  # 重定向到首页
    else:
        return RedirectResponse(url="/login", status_code=303)  # 重定向到登录页面


app.include_router(login.router)  # 注册登录路由
app.include_router(register.router)  # 注册注册路由
app.include_router(index.router)  # 注册首页路由
app.include_router(upload.router)  # 注册上传文件路由
app.include_router(down.router)  # 注册下载文件路由
app.include_router(captcha.router)  # 注册验证码路由
app.include_router(text.router)  # 注册测试路由
app.include_router(logout.router)  # 注册注销路由
app.include_router(user.router)  # 注册用户信息路由

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.host, port=config.port)  # 启动 FastAPI 服务
