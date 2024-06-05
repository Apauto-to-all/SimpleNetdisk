from typing import Optional
from fastapi import APIRouter, Cookie, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import password_utils, user_utils, files_utils

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 加密文件夹
@router.post("/encrypt")
async def encrypt_folder(
    response: Response,
    folder_id: Optional[str] = None,  # 添加查询参数
    password: Optional[str] = Form(None),  # 读取表单数据
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
    unlock_folder: Optional[str] = Cookie(None),  # 解密文件夹
):
    # 判断是否登录
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    # 加密文件夹下如果有文件夹，不允许加密
    if await files_utils.is_folder_has_folder(username, folder_id):
        return {"error": "文件夹下有文件夹，无法加密"}
    if await files_utils.is_folder_encrypted(username, folder_id):  # 文件夹被加密
        if not unlock_folder:
            return {"error": "文件夹被加密，请先解密再使用"}
        if not await password_utils.verify_password(unlock_folder, folder_id):
            return {"error": "该文件夹未解密，请先解密再使用"}
    if folder_id and password:
        if await files_utils.encrypt_folder(
            username,
            folder_id,
            password,
        ):
            response = Response(content="成功", status_code=200)
            response.delete_cookie("unlock_folder")  # 删除加密文件夹的 Cookie
            return response

    return {"error": "加密失败"}


# 解密文件夹
@router.post("/decrypt")
async def decrypt_folder(
    response: Response,
    # 临时解密还是删除加密
    folder_id: Optional[str] = None,  # 添加查询参数
    password: Optional[str] = Form(None),  # 读取表单数据
    is_permanent: Optional[bool] = Form(False),  # 是否永久解密，删除密码
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    # 判断是否登录
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    if folder_id and password:  # 解密文件夹
        if await files_utils.decrypt_folder(
            username,
            folder_id,
            password,
            is_permanent,
        ):
            response = Response(content="成功", status_code=200)
            if not is_permanent:
                response.set_cookie(
                    key=f"unlock_folder",
                    value=await password_utils.encrypt_password(folder_id),
                )
            return response
    return {"error": "解密失败"}


# 创建文件夹
@router.post("/create_folder")
async def create_folder(
    folder_id: Optional[str] = None,  # 添加查询参数
    folder_name: Optional[str] = Form(None),  # 读取表单数据
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    # 判断是否登录
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    if folder_id and folder_name:  # 创建文件夹
        if await files_utils.is_folder_encrypted(username, folder_id):  # 文件夹被加密
            return {"error": "加密的文件夹下无法创建文件夹"}
        await files_utils.create_folder_get_folder_id(username, folder_id, folder_name)
        return {"success": "创建成功"}
    return {"error": "创建失败"}


# 删除文件或文件夹的路由
@router.get("/delete")
async def delete_file_folder(
    file_id: Optional[str] = None,  # 添加查询参数
    folder_id: Optional[str] = None,  # 添加查询参数
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
    unlock_folder: Optional[str] = Cookie(None),  # 解密文件夹
):
    # 判断是否登录
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    if file_id and not folder_id:  # 删除文件
        lock_folder_id = await files_utils.get_parent_folder_id_is_locked(
            username, file_id
        )
        if lock_folder_id:  # 文件的父类文件夹被加密
            if not unlock_folder:
                return {"error": "文件所属的文件夹被加密，请先解密再使用"}
            if not await password_utils.verify_password(unlock_folder, lock_folder_id):
                return {"error": "文件所属的文件夹未解密，请先解密再使用"}
        # 获取被删除文件的父级文件夹id
        if await files_utils.delete_file(username, file_id):
            return {"success": "删除成功"}
    if folder_id and not file_id:  # 删除文件夹
        if await files_utils.is_folder_encrypted(username, folder_id):  # 文件夹被加密
            if not unlock_folder:
                return {"error": "文件夹被加密，请先解密再使用"}
            if not await password_utils.verify_password(unlock_folder, folder_id):
                return {"error": "该文件夹未解密，请先解密再使用"}
        if await files_utils.delete_folder(username, folder_id):
            return {"success": "删除成功"}

    return {"error": "删除失败"}


# 重命名文件的路由
@router.post("/rename")
async def rename_file(
    file_id: Optional[str] = None,  # 添加查询参数
    folder_id: Optional[str] = None,  # 添加查询参数
    new_file_name: Optional[str] = Form(None),  # 读取表单数据
    new_folder_name: Optional[str] = Form(None),  # 读取表单数据
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
    unlock_folder: Optional[str] = Cookie(None),  # 解密文件夹
):
    # 判断是否登录
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    if file_id and new_file_name:  # 重命名文件
        lock_folder_id = await files_utils.get_parent_folder_id_is_locked(
            username, file_id
        )
        if lock_folder_id:  # 文件的父类文件夹被加密
            if not unlock_folder:
                return {"error": "文件所属的文件夹被加密，请先解密再使用"}
            if not await password_utils.verify_password(unlock_folder, lock_folder_id):
                return {"error": "文件所属的文件夹未解密，请先解密再使用"}
        if await files_utils.rename_file(
            username,
            file_id,
            new_file_name,
        ):
            return {"success": "重命名成功"}
    if folder_id and new_folder_name:  # 重命名文件夹
        if await files_utils.is_folder_encrypted(username, folder_id):  # 文件夹被加密
            if not unlock_folder:
                return {"error": "文件夹被加密，请先解密再使用"}
            if not await password_utils.verify_password(unlock_folder, folder_id):
                return {"error": "该文件夹未解密，请先解密再使用"}
        if await files_utils.rename_folder(
            username,
            folder_id,
            new_folder_name,
        ):
            return {"success": "重命名成功"}

    return {"error": "重命名失败"}
