import misaka
import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo # python 3.9+
import time
import traceback

###########################################################################################

# 以下你可以根据自己的需要进行修改
IS_REPLACE_LINK = True
"""是否修改md文件中的链接？"""
DEFUALT_IMG_TYPE = '.png'
"""
给无后缀的图片url新增文件扩展名
（建议测试一下到底是什么类型的图片，一般都是png）
"""

def img_url_check(img_url:str):
    """
    你可以修改这个函数，比如只下载某一部分url中的图片。
    返回值为True代表需要下载当前图片
    """
    return True


###########################################################################################

TARGET_DIR ='./files/img/'
"""存放下载好的本地图片的目录"""
MD_FILES_DIR = './files'
"""存放md文件的文件夹 """
err_img = {}
"""保存错误的图片dict"""

def open_json_file(path):
    """打开json文件"""
    with open(path, 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    return tmp

def write_json_file(path: str, value):
    """写入json文件"""
    with open(path, 'w', encoding='utf-8') as fw2:
        json.dump(value, fw2, indent=2, sort_keys=True, ensure_ascii=False)

def get_time(format_str='%y-%m-%d-%H%M%S'):
    """获取当前时间，格式为 `23-01-01-000000`"""
    a = datetime.now(ZoneInfo('Asia/Shanghai'))  # 返回北京时间
    return a.strftime(format_str)

def write_err_file():
    """写入日志文件"""
    ERR_FILE_PATH = f"{get_time()}-err.json"
    """保存错误图片的路径"""

    print(f"\n[file] err_img\n{err_img}") # 保存之前打印，避免保存失败
    write_json_file(ERR_FILE_PATH,err_img) # 写入文件
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


def download_pics(url:str):
    """
    下载图片并保存到本地

    Returns:
    - 空字符串：非网络图片，处理失败
    - 非空字符串：图片本地文件名
    """
    if 'http' not in url:
        print('不处理本地图片: ', url)
        return ""
    if not img_url_check(url):
        print('用户自定义图片url检查失败：',url)
        return ""

    img_data = requests.get(url).content # 获取到的图片url文件data
    filename = url[url.rfind('/')+1:] # 图片源文件名
    # 如果filename中不包含.认为其没有文件后缀，给他添加上一个
    if '.' not in filename:
        filename += DEFUALT_IMG_TYPE

    print('图片文件名：',filename)

    # 保存本地，用图片文件名命名
    # 原作者用的是uuid随机命名，其实这样更好，但是：前提得替换md文件中的图片链接
    # 可原作者并没有写这部分的代码，本人对本项目用到的模块并不了解，所以没有进行此功能开发
    with open(os.path.join(TARGET_DIR, filename), 'w+') as f:
        f.buffer.write(img_data)
    return filename



if __name__ == '__main__':
    try:
        print("开始处理\n")
        # 获取MD_FILES_DIR路径下的所有文件列表
        files_list = get_files_list(os.path.abspath(os.path.join('.', MD_FILES_DIR)))
        # 如果目标文件目录不存在，创建文件目录
        if not os.path.exists(TARGET_DIR):
            os.mkdir(TARGET_DIR)

        md_content = ""
        for file in files_list:
            if '.md' not in file:
                print(f"不处理非md文件: {file}")
                continue

            print(f'正在处理md文件：{file}')
            # utf-8会有编码报错。所以使用如下编码读取md文件
            with open(file, encoding='ISO-8859-1') as f:
                md_content = f.read()
            # 获取图片列表
            pics_list = get_pics_list(md_content)
            print(f'发现图片 {len(pics_list)} 张')

            md_file_name = "" # 初始化为空
            for index, pic in enumerate(pics_list):
                try:
                    print(f'正在下载第 {index + 1} 张图片...\n图片链接：', pic)
                    md_file_name = os.path.basename(file) # 当前处理的md文件的名字
                    # 处理图片
                    new_img_file_name = download_pics(pic)
                    # 修改md文件内容
                    if IS_REPLACE_LINK and new_img_file_name != "":
                        new_img_file_path = os.path.abspath(os.path.join('.',TARGET_DIR,new_img_file_name))
                        new_img_file_path = new_img_file_path.replace('\\','/') # 路径转linux风格
                        md_content = md_content.replace(pic,new_img_file_path)

                    time.sleep(0.3) # 避免下载超速
                except KeyboardInterrupt:
                    write_err_file() # 写入日志文件
                    os.abort() # 避免无法ctrl+c
                except Exception as result:
                    print(traceback.format_exc()) # 打印错误
                    # 判断err_img，如果文件名不在里面，则新增键值
                    if md_file_name not in err_img:
                        err_img[md_file_name]=[]
                    # 添加err图片
                    err_img[md_file_name].append(pic)
                    print("图片获取错误：",pic)
                    time.sleep(1)

            # 修改后的md写入文件
            with open(file, encoding='ISO-8859-1',mode='w') as f:
                f.write(md_content)
            # 处理完毕单个文件
            print(f'处理完毕md文件：{file}\n')

        # 结束后保存err
        print('\n全部处理完成。')
        write_err_file()
    except Exception as result:
        print(traceback.format_exc())
        print("\n错误图片输出：\n",err_img)
        os.abort()