from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter()


@router.get("/logout")  # 退出登录
async def logout():
    response = RedirectResponse(url="/login", status_code=303)  # 重定向到登录页面
    response.delete_cookie("access_token")  # 删除 Cookie
    return response
