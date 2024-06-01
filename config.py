from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

# 全局配置文件

# 项目运行的主机和端口
host = "localhost"
port = 19764

# 数据库配置
db_name = "PostgreSQL"
db_host = "47.121.25.171"
db_port = 5432

# 数据库
database = "SimpleCloud"

# 数据库root用户名和密码
# root_uesr = "postgres"
# root_password = "password"

# 数据库操作用户名和密码
"""
只用于查询，更新，插入操作，无删除权限
"""
connect_user = "user"
connect_user_password = "password"

# 保存登入的时间，单位为min
login_time = 30

# 储存路径，以path结尾
# 用户头像路径
user_avatar_path = "files/avatars"
# 文件缩略图路径
thumbnail_path = "files/thumbnails"
# 文件夹锁/解锁图标路径
folder_lock_path = "files/lock"
# 用户文件存放路径
user_files_path = "files/files_all"
# 用户文件夹路径
log_path = "log"


# 日志
current_date = datetime.now().strftime("%Y-%m-%d")  # 获取当前的日期


# 创建一个handler，用于写入日志文件，每天创建一个新的日志文件，保留30天的日志文件
def setup_logger():
    # 创建一个logger
    logger = logging.getLogger()  # 获取日志记录器
    logger.setLevel(logging.DEBUG)  # 设置日志记录器的级别

    # 创建一个handler，用于写入日志文件，每天创建一个新的日志文件，保留30天的日志文件
    fh = TimedRotatingFileHandler(
        f"{log_path}/{current_date}.log",  # 日志文件名
        when="midnight",  # 每天创建一个新的日志文件
        interval=1,  # 每天创建一个新的日志文件
        backupCount=30,  # 保留30天的日志文件
        encoding="utf-8",  # 日志文件编码
    )
    fh.setLevel(logging.DEBUG)

    # # 再创建一个handler，用于输出到控制台
    # ch = logging.StreamHandler(sys.stdout)  # 输出到控制台
    # ch.setLevel(logging.DEBUG)  # 输出到控制台

    # 定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    # ch.setFormatter(formatter)  # 输出到控制台

    # 给logger添加handler
    logger.addHandler(fh)
    # logger.addHandler(ch)  # 输出到控制台


setup_logger()


# 测试前缀
isTest = True  # 是否为测试模式
test_prefix = ""  # 测试前缀
if isTest:  # 如果为测试模式，使用有测试前缀的测试文件
    test_prefix = "test-"  # 测试前缀
