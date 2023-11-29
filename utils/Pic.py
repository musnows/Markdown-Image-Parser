import markdown
from bs4 import BeautifulSoup
import re
import hashlib



def get_pics_list_from_md_html(md_content: str):
    """
    通过转html获取一个markdown文档里的所有图片链接
    :param md_content: open的md文件内容
    :return: 图片列表
    """
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, features='html.parser')
    pics_list = []
    for img in soup.find_all('img'):
        pics_list.append(img.get('src'))

    return pics_list


def get_pics_list_from_md_regex(md_content: str):
    """
    通过正则获取一个markdown文档里的所有图片链接
    :param md_content: open的md文件内容
    :return: 图片列表
    """
    # 正则表达式匹配Markdown中的图片语法
    image_pattern = re.compile(r'!\[.*?\]\((.*?)\)', re.DOTALL)

    # 使用findall方法找到所有匹配的图片链接
    image_links = re.findall(image_pattern, md_content)

    return image_links


def calculate_md5_from_bytes(image_data):
    """
    计算图片文件的MD5值
    :return: MD5字符串
    """
    md5_hash = hashlib.md5()
    md5_hash.update(image_data)
    md5_hex = md5_hash.hexdigest()
    return md5_hex