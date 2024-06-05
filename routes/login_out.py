from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,  # 功能：用于接收请求
    Request,  # 功能：用于接收请求
    Form,  # 功能：用于接收表单数据
    Cookie,  # 功能：用于操作 Cookie
)  # 导入 FastAPI 框架
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import (
    HTMLResponse,  # 用于返回 HTML 响应
    RedirectResponse,  # 用于重定向
)
from typing import Optional  # 功能：用于声明可选参数
from utils import user_utils  # 导入用户工具
import config  # 导入全局配置文件

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # 模板目录


@router.get("/logout")  # 退出登录
async def logout():
    response = RedirectResponse(url="/login", status_code=303)  # 重定向到登录页面
    response.delete_cookie("access_token")  # 删除 Cookie
    return response


@router.get("/login", response_class=HTMLResponse)
async def login(
    request: Request,  # 用于接收请求
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    if await user_utils.isLogin_getUser(access_token):  # 判断是否登录
        return RedirectResponse(url="/index", status_code=303)

    isUseCapthca = False  # 是否使用验证码，默认为 False
    if await user_utils.isUseCapthca(request):  # 判断是否使用验证码
        isUseCapthca = True  # 使用验证码
    return await loginHtml(request, isUseCapthca=isUseCapthca)


@router.post("/login")
async def login(
    request: Request,
    username: Optional[str] = Form(""),  # 获取用户名
    password: Optional[str] = Form(""),  # 获取密码
    captcha: Optional[str] = Form(""),  # 获取验证码
    hashed_captcha: Optional[str] = Cookie(None),  # 获取加密后的验证码
):
    isUseCapthca = False
    if await user_utils.isUseCapthca(request):  # 判断是否使用验证码
        isUseCapthca = True
        if not captcha:
            error_message = "验证码不能为空"
            return await loginHtml(
                request,
                error_message,
                username,
                isUseCapthca=isUseCapthca,
            )
        if not await user_utils.verifyCaptcha(captcha, hashed_captcha):  # 验证验证码
            error_message = "验证码错误"
            return await loginHtml(
                request,
                error_message,
                username,
                isUseCapthca=isUseCapthca,
            )
    if not username or not password:
        error_message = "用户名或密码不能为空"
        return await loginHtml(
            request,
            error_message,
            username,
            isUseCapthca=isUseCapthca,
        )

    if await user_utils.verifyLogin(username, password):  # 验证登录
        return await loginSuccess(username, request)  # 登录成功
    error_message = "用户名或密码错误"
    return await loginHtml(request, error_message, username, isUseCapthca=isUseCapthca)


async def loginSuccess(username, request):
    """
    登录成功后的操作
    :param username: 用户名
    :param password: 密码
    :return: 登录成功后的响应
    """
    await user_utils.login_or_register_success(request)  # 登录成功，访问者错误次数清零
    # 控制登入成功后的跳转，并设置 Cookie
    response = RedirectResponse(url="/index", status_code=303)  # 重定向到首页
    response.set_cookie(
        key="access_token",  # 设置 Cookie 的键
        value=await user_utils.get_token(username),  # 设置 Cookie 的值
        max_age=60 * config.login_time,  # 设置 Cookie 有效期为 config.login_time 分钟
    )
    return response


async def loginHtml(
    request: Request,  # 用于接收请求
    error_message="",  # 错误信息，默认为 ""
    username="",  # 用户名，默认为 ""
    isUseCapthca=False,  # 是否使用验证码，默认为 False
):
    """
    登录页面
    :param request: 请求
    :param error_message: 错误信息
    :param username: 用户名
    :param isUseCapthca: 是否使用验证码，默认为 False
    :return: 登录页面响应
    """
    if error_message:  # 如果有错误信息，说明登录失败
        await user_utils.login_or_register_failed(request)  # 登录失败，访问者错误次数+1
    return templates.TemplateResponse(
        f"{config.test_prefix}login.html",
        {
            "request": request,
            "error_message": error_message,
            "username": username,
            "isUseCapthca": isUseCapthca,
        },
    )
