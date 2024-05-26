from fastapi import APIRouter, Request, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse, RedirectResponse  # 功能：用于返回 HTML 响应
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional

from utils import user_utils, password_utils

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    isUseCapthca = False
    if await user_utils.isUseCapthca():  # 判断是否使用验证码
        isUseCapthca = True
    return await registerHtml(request, isUseCapthca=isUseCapthca)  # 返回注册页面


@router.post("/register")
async def register(
    request: Request,
    username: Optional[str] = Form(""),  # 获取用户名
    password: Optional[str] = Form(""),  # 获取密码
    confirm_password: Optional[str] = Form(""),  # 获取确认密码
    regCode: Optional[str] = Form(""),  # 获取注册码
    captcha: Optional[str] = Form(""),  # 获取验证码
):
    isUseCapthca = False
    if await user_utils.isUseCapthca():  # 判断是否使用验证码
        isUseCapthca = True
        if not captcha:  # 判断验证码是否为空
            error_message = "验证码不能为空"
            return await registerHtml(
                request,
                error_message,
                username,
                regCode,
                isUseCapthca=isUseCapthca,
            )
        if not await user_utils.verifyCaptcha(captcha):  # 验证验证码
            error_message = "验证码错误"
            return await registerHtml(
                request,
                error_message,
                username,
                regCode,
                isUseCapthca=isUseCapthca,
            )
    if not regCode:  # 判断注册码是否为空
        error_message = "注册码不能为空"
        return await registerHtml(
            request,
            error_message,
            username,
            regCode,
            isUseCapthca=isUseCapthca,
        )
    if not await user_utils.verifyRegCode(regCode):  # 验证注册码
        error_message = "注册码错误"
        return await registerHtml(
            request,
            error_message,
            username,
            regCode,
            isUseCapthca=isUseCapthca,
        )

    if not username or not password or not confirm_password:  # 判断用户名或密码是否为空
        error_message = "用户名或密码不能为空"
        return await registerHtml(
            request,
            error_message,
            username,
            regCode,
            isUseCapthca=isUseCapthca,
        )
    if password != confirm_password:  # 判断两次密码是否一致
        error_message = "两次密码不一致"
        return await registerHtml(
            request,
            error_message,
            username,
            regCode,
            isUseCapthca=isUseCapthca,
        )
    usernameFormat = user_utils.verify_username_format(username)  # 验证用户名格式
    if usernameFormat:  # 如果用户名格式错误，这里的 usernameFormat 是用户名格式要求信息
        error_message = usernameFormat  # 错误信息，提示用户名格式
        return await registerHtml(
            request,
            error_message,
            username,
            regCode,
            isUseCapthca=isUseCapthca,
        )
    if not await user_utils.verifyUsername(username):  # 验证用户名是否存在
        error_message = "用户名已存在，请更换用户名"
        return await registerHtml(
            request,
            error_message,
            username,
            regCode,
            isUseCapthca=isUseCapthca,
        )
    passwordFormat = password_utils.verify_get_password_format(password)  # 验证密码格式
    if passwordFormat:  # 如果密码格式错误，这里的 passwordFormat 是密码格式要求信息
        error_message = passwordFormat  # 错误信息，提示密码格式
        return await registerHtml(
            request,
            error_message,
            username,
            regCode,
            isUseCapthca=isUseCapthca,
        )
    # 注册成功
    return await registerSuccess(username, password, regCode)


async def registerSuccess(username, password, regCode):
    """
    注册成功，将用户信息写入数据库，返回注册成功页面
    :param username: 用户名
    :param password: 密码
    :param regCode: 注册码
    :return: 注册成功页面响应，重定向到登录页面
    """
    # 写入数据库
    await user_utils.registerSuccess(
        username, password, regCode
    )  # 注册成功，写入数据库
    await user_utils.login_or_register_success()  # 注册成功，访问者错误次数清零
    return RedirectResponse(url="/login", status_code=303)  # 重定向到登录页面


async def registerHtml(
    request: Request,  # 用于接收请求
    error_message="",  # 错误信息，默认为 ""
    username="",  # 用户名，默认为 ""
    regCode="",  # 注册码，默认为 ""
    isUseCapthca=False,  # 是否使用验证码，默认为 False
):
    """
    注册页面
    :param request: 请求
    :param error_message: 错误信息
    :param username: 用户名
    :param regCode: 注册码
    :param isUseCapthca: 是否使用验证码
    :return: 注册页面响应
    """
    if error_message:  # 如果有错误信息，说明注册失败
        await user_utils.login_or_register_failed(request)  # 注册失败，访问者错误次数+1
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "error_message": error_message,
            "username": username,
            "regCode": regCode,
            "isUseCapthca": isUseCapthca,
        },
    )
