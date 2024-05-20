from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import os
from typing import List

router = APIRouter()


def get_file_path(user_file_path="files"):
    file_path = Path.cwd() / user_file_path
    if not file_path.exists():
        os.makedirs(file_path)
    return file_path


@router.post("/upfile/")
async def upload_file(files: List[UploadFile] = File(...)):
    file_paths = []
    for file in files:
        contents = await file.read()
        file_path = get_file_path()  # 获取文件保存路径
        fp = file_path / file.filename
        with fp.open("wb") as f:
            f.write(contents)
        file_paths.append(str(fp))
    return {"file_paths": file_paths}
