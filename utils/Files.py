import json
import os

from . import ConfigType
from .Time import get_time
from .Logger import _log

ErrImgDict = {}
"""保存错误的图片dict"""
ErrImgCount = 0
"""错误图片计数器"""


def open_json_file(path: str):
    """打开json文件"""
    with open(path, 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    return tmp


def write_json_file(path: str, value):
    """写入json文件"""
    with open(path, 'w', encoding='utf-8') as fw2:
        json.dump(value, fw2, indent=2, sort_keys=True, ensure_ascii=False)


def open_md_file(path: str, encode):
    """打开md文件"""
    with open(path, encoding=encode) as f:
        md_content = f.read()
    return md_content

def write_md_file(path: str,md_content, encode):
    """写入md文件"""
    with open(path, encoding=encode,mode='w') as f:
        f.write(md_content)


def write_img_file(md_file_path: str, img_data, rename_options: ConfigType.ImgRenameType,
                   target_options: ConfigType.HandlerType):
    """保存md文件到本地
    :param dir: 文件路径

    :return 新的文件路径（根据
    """
    return

def get_files_list(dir: str):
    """
    获取一个目录下所有文件列表，包括子目录
    :param dir: 文件路径
    :return: 文件列表
    """
    files_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for file in files:
            files_list.append(os.path.join(root, file))

    return files_list


def add_err_pic(file_name: str, img_url: str,err_info:str = "None"):
    """
    添加处理错误的图片
    :param file_name 对应的md文件
    :param img_url 图片url链接
    :param err_info 错误原因
    """
    global ErrImgDict,ErrImgCount
    if file_name not in ErrImgDict:
        ErrImgDict[file_name] = []
    # 插入图片
    ErrImgDict[file_name][img_url] = err_info
    ErrImgCount += 1
    _log.error(f"[file] add err img '{img_url}' with file '{file_name}'")


def create_dir(dir: str):
    """创建文件夹"""
    # 如果目标文件目录不存在，创建文件目录
    if not os.path.exists(dir):
        os.mkdir(dir)
        _log.info(f"[file] create dir: {dir}")


def write_err_img_log_file(cur_time: str = get_time()):
    """
    将ErrImgDict写入日志文件
    :param cur_time 当前时间字符串，用于标定日志文件
    :return 返回日志文件路径
    """
    global ErrImgDict
    # 如果没有错误，不处理
    if not ErrImgDict:
        _log.info("[file] 本次处理没有错误图片，无需写入错误文件 | no error this time\n")
        return ""

    err_file_path = f"{cur_time}-err.json"  # 保存错误图片的路径
    try:
        _log.error(f"[file] write ErrImgDict | err count: {ErrImgCount}")
        write_json_file(err_file_path, ErrImgDict)  # 写入文件
        _log.error(f"[file] write ErrImgDict into file | {err_file_path}")  # 写入成功
    except Exception as result:
        _log.exception(f"[file] error while writing ErrImgDict | {err_file_path}")
        _log.error(f"\n---\n{ErrImgDict}\n---\n")  # 直接把dict打印出来做留档

    return err_file_path
