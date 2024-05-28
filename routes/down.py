import os
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import config

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/down")
async def down(request: Request):
    return templates.TemplateResponse(
        f"{config.test_prefix}down.html", {"request": request}
    )


# 生成临时链接并下载文件的路由
@router.get("/download")
async def download_file(file_path: str | None = None):
    # 使用原始文件路径拼接文件路径
    file_path = os.path.join("./files", file_path)

    return FileResponse(
        path=file_path,
        filename="图片.exe",
    )
