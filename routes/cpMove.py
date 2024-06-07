import json
from typing import Optional
from fastapi import APIRouter, Cookie, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import user_utils, cpMove_utils

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# 进入文件树页面
@router.get("/cpMove")
async def cpMove(
    request: Request,  # 请求
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    return templates.TemplateResponse(
        "test-folders.html", {"request": request}
    )  # 返回文件树页面


# 获取父类文件夹下的所有子类文件夹
@router.get("/getfolders")
async def get_folders(
    parent_folder_id: Optional[str] = None,  # 添加查询参数
    folders_id: Optional[str] = Cookie(None),  # 读取 Cookie，获取需要操作的文件夹id列表
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    if not parent_folder_id:
        return {}
    username = await user_utils.isLogin_getUser(access_token)
    if not username:  # 判断是否登录
        return {}
    """
    {
        "uuid1": "folder_name1",
        "uuid2": "folder_name2",
    }
    """
    dict_folders = await cpMove_utils.get_all_folder_from_parent_folder_id(
        username,
        parent_folder_id,
    )
    # 将JSON字符串解析为Python列表
    folders_id_list = json.loads(folders_id) if folders_id else []
    # 如果需要复制或移动的文件夹在当前文件夹下，删掉
    dict_folders = {
        folder_id: folder_info
        for folder_id, folder_info in dict_folders.items()
        if folder_id not in folders_id_list
    }
    return dict_folders


# 移动文件夹，设置cp_or_move的cookie为False
@router.get("/set_cookie_move")
async def move_folder(
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    response = RedirectResponse(url="/cpMove", status_code=303)
    response.set_cookie(key="cp_or_move", value=False)
    return response


# 复制文件夹，设置cp_or_move的cookie为True
@router.get("/set_cookie_cp")
async def cp_folder(
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    response = RedirectResponse(url="/cpMove", status_code=303)
    response.set_cookie(key="cp_or_move", value=True)
    return response


# 移动还是复制判断
@router.get("/get_cp_or_move")
async def get_cp_or_move(
    cp_or_move: Optional[bool] = Cookie(None),  # 移动为False，复制为True
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    if cp_or_move == None:
        return {"error": "操作未知"}
    return (
        {"info": "复制 ： 选择目标文件夹"}
        if cp_or_move
        else {"info": "移动 ： 选择目标文件夹"}
    )


# 移动文件或文件夹到此文件夹
@router.get("/move_to_folder")
async def move_to_folder(
    target_folder_id: Optional[str] = None,  # 添加查询参数，移动的目标文件夹id
    files_id: Optional[str] = Cookie(None),  # 读取 Cookie，获取需要操作的文件id列表
    folders_id: Optional[str] = Cookie(None),  # 读取 Cookie，获取需要操作的文件夹id列表
    cp_or_move: Optional[str] = Cookie(None),  # 移动为False，复制为True
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    if cp_or_move == None:
        return {"error": "操作未知"}
    if not target_folder_id:
        return {"error": "未选择目标文件夹"}
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    # 将JSON字符串解析为Python列表
    files_id_list = json.loads(files_id) if files_id else []
    folders_id_list = json.loads(folders_id) if folders_id else []
    # await cpMove_utils.move_files_and_folders(
    #     username, target_folder_id, files_id_list, folders_id_list
    # )
    return (
        RedirectResponse(url="/index", status_code=303)
        if target_folder_id == "/"
        else RedirectResponse(url=f"/index/{target_folder_id}", status_code=303)
    )


# 复制文件或文件夹到此文件夹
@router.get("/copy_to_folder")
async def copy_to_folder(
    target_folder_id: Optional[str] = None,  # 添加查询参数，复制的目标文件夹id
    files_id: Optional[str] = Cookie(None),  # 读取 Cookie，获取需要操作的文件id列表
    folders_id: Optional[str] = Cookie(None),  # 读取 Cookie，获取需要操作的文件夹id列表
    cp_or_move: Optional[str] = Cookie(None),  # 移动为False，复制为True
    access_token: Optional[str] = Cookie(None),  # 读取 Cookie
):
    if cp_or_move == None:
        return {"error": "操作未知"}
    if not target_folder_id:
        return {"error": "未选择目标文件夹"}
    username = await user_utils.isLogin_getUser(access_token)
    if not username:
        return {"error": "未登录"}
    # 将JSON字符串解析为Python列表
    files_id_list = json.loads(files_id) if files_id else []
    folders_id_list = json.loads(folders_id) if folders_id else []
    # await cpMove_utils.copy_files_and_folders(
    #     username, target_folder_id, files_id_list, folders_id_list
    # )
    return (
        RedirectResponse(url="/index", status_code=303)
        if target_folder_id == "/"
        else RedirectResponse(url=f"/index/{target_folder_id}", status_code=303)
    )
