import config
import os

# 遍历 config 中的属性。如果属性名以 path 结尾，说明是文件夹路径，如果文件夹不存在，创建文件夹
for attr in dir(config):
    if attr.endswith("path"):
        folder_path = getattr(config, attr)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
