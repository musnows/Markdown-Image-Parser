import logging # 采用logging来替换所有print
import shutil,os
from time import time

LOGGER_NAME = "img-parse-log"
LOGGER_FILE = "img-parse.log" # 如果想修改log文件的名字和路径，修改此变量

# 检查是否已有日志文件，如果有将其移动走
if os.path.exists(LOGGER_FILE):
    new_path = LOGGER_FILE + "." + str(int(time())) +  ".bak"
    shutil.move(LOGGER_FILE, new_path) # 移动文件
    print(f"[log] Previous log moved to {new_path}")


# 初始化日志模块
# 只打印info以上的日志（debug低于info）
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s:%(filename)s:%(funcName)s:%(lineno)d | %(message)s",
                    datefmt="%y-%m-%d %H:%M:%S")
# 获取一个logger对象
_log = logging.getLogger(LOGGER_NAME)
"""自定义的logger对象"""
# 1.实例化控制台handler和文件handler，同时输出到控制台和文件
file_handler = logging.FileHandler(LOGGER_FILE, mode="a", encoding="utf-8")
fmt = logging.Formatter(fmt="[%(asctime)s] %(levelname)s:%(filename)s:%(funcName)s:%(lineno)d | %(message)s",
                    datefmt="%y-%m-%d %H:%M:%S")
file_handler.setFormatter(fmt)
# 添加handler
_log.addHandler(file_handler)