from fastapi import FastAPI, Cookie  # 导入 FastAPI 框架
from fastapi.responses import (
    HTMLResponse,  # 用于返回 HTML 响应
    RedirectResponse,  # 用于重定向
)
from fastapi.staticfiles import StaticFiles  # 静态文件目录
from routes import (
    files,
    get_img,
    login_out,
    register,
    index,
    folders,
    users,
    trash,
)  # 导入路由
import config  # 导入配置文件
from typing import Optional
from utils import user_utils
from db.connection import DatabaseOperation  # 导入数据库操作类
import logging

# 获取logger
logger = logging.getLogger(__name__)  # 获取日志记录器

app = FastAPI()  # 创建 FastAPI 实例
app.mount("/static", StaticFiles(directory="static"), name="static")  # 静态文件目录

db_operation = DatabaseOperation()


async def startup_event():  # 连接数据库
    await db_operation.connectPool()
    logger.info("连接数据库")


app.add_event_handler("startup", startup_event)  # 注册事件，项目启动时连接数据库


async def shutdown_event():  # 关闭数据库连接池
    await db_operation.pool.close()
    logger.info("关闭数据库连接池")


app.add_event_handler("shutdown", shutdown_event)  # 项目关闭时关闭数据库连接池


@app.get("/", response_class=HTMLResponse)
async def root(
    access_token: Optional[str] = Cookie(None),
):
    if await user_utils.isLogin_getUser(access_token):  # 判断是否登录
        return RedirectResponse(url="/index", status_code=303)  # 重定向到首页
    else:
        return RedirectResponse(url="/login", status_code=303)  # 重定向到登录页面


app.include_router(login_out.router)  # 注册与登录相关的路由
app.include_router(register.router)  # 注册注册路由
app.include_router(index.router)  # 注册首页路由
app.include_router(files.router)  # 注册下载文件路由
app.include_router(get_img.router)  # 注册获取图片路由
app.include_router(folders.router)  # 注册文件夹路由
app.include_router(users.router)  # 注册用户路由
app.include_router(trash.router)  # 注册垃圾桶路由

if __name__ == "__main__":
    import uvicorn

    try:
        uvicorn.run(app, host=config.host, port=config.port)  # 启动 FastAPI 服务
    except KeyboardInterrupt:
        logger.info("关闭 FastAPI 服务")
