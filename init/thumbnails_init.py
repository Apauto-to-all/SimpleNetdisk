from db.connection import DatabaseOperation
import config
import os
import asyncio

db_operation = DatabaseOperation()

all_thumbnails = config.thumbnail_path + "/all"

# 初始化缩略图文件夹
# 如果不存在则创建
if not os.path.exists(all_thumbnails):
    os.makedirs(all_thumbnails)

# 获取路径下所有文件缩略图
all_thumbnails_files = os.listdir(all_thumbnails)
# ['data.png', 'ico.png', 'jpg.png', 'mp3.png', 'mp4.png', 'png.png', 'rar.png', 'zip.png']


async def init_thumbnails():
    await db_operation.connectPool()
    for i in all_thumbnails_files:
        # 将所有缩略图文件插入数据库
        # 获取到文件名
        name = i.split(".")[0]
        path = os.path.join(all_thumbnails, i)
        # 插入数据库
        if not await db_operation.ShrinkTable_insert(name, path):
            print(f"插入{name}缩略图失败")


# 运行初始化缩略图
asyncio.run(init_thumbnails())
