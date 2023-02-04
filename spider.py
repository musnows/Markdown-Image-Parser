import misaka
import os
import requests
import uuid
import json
from bs4 import BeautifulSoup
import time
import traceback

assert_dir = 'img' # 本地图片存放目录
targer_dir ='./files/img/' # 存放下载好的本地图片的目录


def open_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    return tmp

err_img = open_file('err.json')

def write_file(path: str, value):
    with open(path, 'w', encoding='utf-8') as fw2:
        json.dump(value, fw2, indent=2, sort_keys=True, ensure_ascii=False)



def get_files_list(dir):
    """
    获取一个目录下所有文件列表，包括子目录
    :param dir:
    :return:
    """
    files_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for file in files:
            files_list.append(os.path.join(root, file))

    return files_list


def get_pics_list(md_content):
    """
    获取一个markdown文档里的所有图片链接
    :param md_content:
    :return:
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
    filename = url[url.rfind('/')+1:] # 源文件名
    print('图片文件名：',filename)
    # 如果目标文件目录不存在，创建文件目录
    if not os.path.exists(targer_dir):
        os.mkdir(targer_dir)
    
    # 保存本地（用文件名命名，原作者用的是uuid随机命名）
    with open(os.path.join(targer_dir, filename), 'w+') as f:
        f.buffer.write(img_data)
    


if __name__ == '__main__':
    files_list = get_files_list(os.path.abspath(os.path.join('.', 'files')))

    for file in files_list:
        print(f'正在处理：{file}')
        # utf-8会有编码报错
        with open(file, encoding='ISO-8859-1') as f:
            md_content = f.read()

        pics_list = get_pics_list(md_content)
        print(f'发现图片 {len(pics_list)} 张')

        for index, pic in enumerate(pics_list):
            try:
                print(f'正在下载第 {index + 1} 张图片...')
                MDfilename = os.path.basename(file) # 当前处理的md文件的名字
                download_pics(pic)
                time.sleep(0.5) # 避免下载超速
            except KeyboardInterrupt:
                os.abort() # 避免无法ctrl+c
            except:
                print(traceback.format_exc()) # 打印错误
                # 判断err_img，如果文件名不在里面，则新增键值
                if MDfilename not in err_img:
                    err_img[MDfilename]=[]
                # 添加err图片
                err_img[MDfilename].append(pic)
                print("图片获取错误：",pic)
                time.sleep(1)
    
    # 结束后保存err
    print(f'处理完成。')
    write_file('err.json',err_img)
    print(f'写入err完成')