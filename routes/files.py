import os
from typing import List, Optional
from fastapi import APIRouter, Cookie, File, Form, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import config
from utils import password_utils, user_utils, files_utils

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 下载文件的路由
@router.get("/download")
async def download_file(
    file_id: Optional[str] = None,  # 添加查询参数
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
    unlock_folder: Optional[str] = Cookie(None),  # 解密文件夹
):
    # 判断是否登录
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    lock_folder_id = await files_utils.get_parent_folder_id_is_locked(username, file_id)
    if lock_folder_id:  # 文件的父类文件夹被加密
        if not unlock_folder:
            return {"error": "文件所属的文件夹被加密，请先解密再使用"}
        if not await password_utils.verify_password(unlock_folder, lock_folder_id):
            return {"error": "文件所属的文件夹未解密，请先解密再使用"}
    file_dict = await files_utils.verify_and_return_files_info(username, file_id)
    if not file_dict:
        return {"error": "文件不存在"}
    file_path = file_dict.get("file_path")
    file_name = file_dict.get("file_name")
    # 使用原始文件路径拼接文件路径
    if not os.path.exists(file_path):
        return {"error": "因无法预料的原因，文件消失了"}

    return FileResponse(
        path=file_path,
        filename=file_name,
    )


@router.post("/upfile")  # 上传文件
async def upload_file(
    folder_id: Optional[str] = None,  # 添加查询参数
    files: List[UploadFile] = File(...),
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
    unlock_folder: Optional[str] = Cookie(None),  # 解密文件夹
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    if folder_id and files:  # 上传文件
        if await files_utils.is_folder_encrypted(username, folder_id):  # 文件夹被加密
            if not unlock_folder:
                return {"error": "文件夹被加密，请先解密再使用"}
            if not await password_utils.verify_password(unlock_folder, folder_id):
                return {"error": "该文件夹未解密，请先解密再使用"}

        for file in files:  # 遍历上传的文件
            contents = await file.read()  # 读取文件内容
            file_name = file.filename  # 文件名
            file_size_bytes = len(contents)  # 文件大小（字节）
            file_size_kb = round(
                file_size_bytes / 1024, 2
            )  # 文件大小（KB），保留两位小数
            if await files_utils.verify_capacity_exceeded(username, file_size_kb):
                return {"error": "容量不足，请清理文件后再上传"}
            file_id = await files_utils.save_file_get_file_id(
                username, file_name, file_size_kb, folder_id
            )
            user_all_file_path = os.path.join(
                config.user_files_path, username
            )  # 用户的文件夹
            file_path = os.path.join(user_all_file_path, file_id)

            with open(file_path, "wb") as f:
                f.write(contents)  # 写入文件
        return RedirectResponse(url=f"/index/{folder_id}", status_code=303)

    return {"error": "上传失败"}


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
        parent_folder_id = await files_utils.delete_file_get_parent_folder_id(
            username, file_id
        )
        if parent_folder_id:
            if parent_folder_id == "/":
                return RedirectResponse(url="/index", status_code=303)
            return RedirectResponse(url=f"/index/{parent_folder_id}", status_code=303)
    if folder_id and not file_id:  # 删除文件夹
        if await files_utils.is_folder_encrypted(username, folder_id):  # 文件夹被加密
            if not unlock_folder:
                return {"error": "文件夹被加密，请先解密再使用"}
            if not await password_utils.verify_password(unlock_folder, folder_id):
                return {"error": "该文件夹未解密，请先解密再使用"}
        parent_folder_id = await files_utils.delete_folder_get_parent_folder_id(
            username, folder_id
        )
        if parent_folder_id:
            if parent_folder_id == "/":
                return RedirectResponse(url="/index", status_code=303)
            return RedirectResponse(url=f"/index/{parent_folder_id}", status_code=303)

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
        parent_folder_id = await files_utils.rename_file_get_parent_folder_id(
            username,
            file_id,
            new_file_name,
        )
        if parent_folder_id:
            return RedirectResponse(url=f"/index/{parent_folder_id}", status_code=303)
    if folder_id and new_folder_name:  # 重命名文件夹
        if await files_utils.is_folder_encrypted(username, folder_id):  # 文件夹被加密
            if not unlock_folder:
                return {"error": "文件夹被加密，请先解密再使用"}
            if not await password_utils.verify_password(unlock_folder, folder_id):
                return {"error": "该文件夹未解密，请先解密再使用"}
        parent_folder_id = await files_utils.rename_folder_get_parent_folder_id(
            username,
            folder_id,
            new_folder_name,
        )
        if parent_folder_id:
            return RedirectResponse(url=f"/index/{parent_folder_id}", status_code=303)

    return {"error": "重命名失败"}


# 加密文件夹
@router.post("/encrypt")
async def encrypt_folder(
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
        parent_folder_id = await files_utils.encrypt_folder_get_parent_folder_id(
            username,
            folder_id,
            password,
        )
        if parent_folder_id:
            response = RedirectResponse(
                url=f"/index/{parent_folder_id}", status_code=303
            )
            response.delete_cookie("unlock_folder")  # 删除加密文件夹的 Cookie
            return response

    return {"error": "加密失败"}


# 解密文件夹
@router.post("/decrypt")
async def decrypt_folder(
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
        parent_folder_id = await files_utils.decrypt_folder_get_parent_folder_id(
            username,
            folder_id,
            password,
            is_permanent,
        )
        if parent_folder_id:  # 解密成功
            response = RedirectResponse(
                url=f"/index/{parent_folder_id}", status_code=303
            )
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
        new_folder_id = await files_utils.create_folder_get_folder_id(
            username, folder_id, folder_name
        )
        if new_folder_id:
            return RedirectResponse(url=f"/index/{folder_id}", status_code=303)
    return {"error": "创建失败"}
