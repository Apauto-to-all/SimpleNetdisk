from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from controllers import login, register

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # 静态文件目录


@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/login")  # 重定向到登录页面


app.include_router(login.router)  # 注册登录路由
app.include_router(register.router)  # 注册注册路由
