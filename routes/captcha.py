from fastapi import APIRouter, Response
from captcha.image import ImageCaptcha
import random
import string
from utils import password_utils

router = APIRouter()


@router.get("/captcha")  # 定义生成验证码的路由
async def getCaptcha():
    image_captcha = ImageCaptcha()  # 创建图片验证码对象
    captcha_text = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=4)
    )  # 生成随机验证码, 长度为 4，包含大写字母和数字
    data = image_captcha.generate(captcha_text)  # 生成图片验证码
    data.seek(0)  # 移动指针到文件开头
    response = Response(content=data.read(), media_type="image/png")  # 创建响应对象
    captcha_text = captcha_text.lower()  # 将验证码转换为小写
    response.set_cookie(
        key="hashed_captcha", value=password_utils.encrypt_password(captcha_text)
    )  # 设置 cookie，存储加密后的验证码
    return response  # 返回图片验证码
