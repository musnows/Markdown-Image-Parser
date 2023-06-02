import misaka
import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo # python 3.9+
import time
import traceback

TARGET_DIR ='./files/img/' 
"""存放下载好的本地图片的目录"""
MD_FILES_DIR = './files'
"""存放md文件的文件夹 """


def open_file(path):
    """打开json文件"""
    with open(path, 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    return tmp

def write_file(path: str, value):
    """写入json文件"""
    with open(path, 'w', encoding='utf-8') as fw2:
        json.dump(value, fw2, indent=2, sort_keys=True, ensure_ascii=False)

def get_time(format_str='%y-%m-%d-%H%M%S'):
    """获取当前时间，格式为 `23-01-01-000000`"""
    a = datetime.now(ZoneInfo('Asia/Shanghai'))  # 返回北京时间
    return a.strftime(format_str)

err_img = {}
"""保存错误的图片dict"""
ERR_FILE_PATH = f"{get_time()}-err.json"
"""保存错误图片的路径"""

def write_err_file():
    """写入日志文件"""
    print(f"\n[file] err_img\n{err_img}") # 保存之前打印，避免保存失败
    write_file(ERR_FILE_PATH,err_img) # 写入文件
    print(f"[file] write file | {ERR_FILE_PATH}") # 写入成功


def get_files_list(dir):
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


def get_pics_list(md_content):
    """
    获取一个markdown文档里的所有图片链接
    :param md_content: open的md文件
    :return: 图片列表
    """
    md_render = misaka.Markdown(misaka.HtmlRenderer())
    html = md_render(md_content)
    soup = BeautifulSoup(html, features='html.parser')
    pics_list = []
    for img in soup.find_all('img'):
        pics_list.append(img.get('src'))

    return pics_list


def download_pics(url):
    if 'http' not in url:
        print('不处理本地图片: ', url)
        return
    img_data = requests.get(url).content # 获取到的图片url
    filename = url[url.rfind('/')+1:] # 图片源文件名
    print('图片文件名：',filename)
    # 如果目标文件目录不存在，创建文件目录
    if not os.path.exists(TARGET_DIR):
        os.mkdir(TARGET_DIR)
    
    # 保存本地，用图片文件名命名
    # 原作者用的是uuid随机命名，其实这样更好，但是：前提得替换md文件中的图片链接
    # 可原作者并没有写这部分的代码，本人对本项目用到的模块并不了解，所以没有进行此功能开发
    with open(os.path.join(TARGET_DIR, filename), 'w+') as f:
        f.buffer.write(img_data)
    


if __name__ == '__main__':
    print("开始处理\n")
    # 获取MD_FILES_DIR路径下的所有md文件列表
    files_list = get_files_list(os.path.abspath(os.path.join('.', MD_FILES_DIR)))

    for file in files_list:
        print(f'正在处理：{file}')
        # utf-8会有编码报错。所以使用如下编码
        with open(file, encoding='ISO-8859-1') as f:
            md_content = f.read()
        # 获取图片列表
        pics_list = get_pics_list(md_content)
        print(f'发现图片 {len(pics_list)} 张')

        md_file_name = "" # 初始化为空
        for index, pic in enumerate(pics_list):
            try:
                print(f'正在下载第 {index + 1} 张图片...')
                md_file_name = os.path.basename(file) # 当前处理的md文件的名字
                # 处理图片
                download_pics(pic)
                time.sleep(0.3) # 避免下载超速
            except KeyboardInterrupt:
                write_err_file() # 写入日志文件
                os.abort() # 避免无法ctrl+c
            except:
                print(traceback.format_exc()) # 打印错误
                # 判断err_img，如果文件名不在里面，则新增键值
                if md_file_name not in err_img:
                    err_img[md_file_name]=[]
                # 添加err图片
                err_img[md_file_name].append(pic)
                print("图片获取错误：",pic)
                time.sleep(1)
        # 处理完毕单个文件
        print(f'处理完毕：{file}\n')
    
    # 结束后保存err
    print('\n全部处理完成。')
    write_err_file()