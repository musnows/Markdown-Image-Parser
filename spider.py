import os
import time
import requests

# 自定义包
import config
from utils import Pic, Files, ConfigType
from utils.Logger import _log

###########################################################################################

RelDirList = {}
"""
相对路径创建时的文件夹列表
如果某个文件不在这里面，则创建文件夹后，添加进去
"""

def handler_network_pics(url: str, file_path: str):
    """
    下载网络图片并保存到本地

    Returns:
    - 空字符串：处理失败
    - 非空字符串：(图片绝对路径，图片文件名)
    """
    if 'http' not in url:
        _log.warning(f'[download] 不处理非http网络图片: {url}')
        return ("","")
    if not config.custom_net_img_url_check(url):
        _log.warning(f'[download] 用户自定义图片url检查失败：{url}')
        return ("","")

    img_data = requests.get(url).content  # 获取到的图片url文件data
    file_name = os.path.basename(url)  # 图片源文件名
    # 如果filename中不包含.认为其没有文件后缀
    # 给他添加上一个默认的图片文件后缀（否则无法识别为图片）
    if '.' not in file_name:
        file_md5 = Pic.calculate_md5_from_bytes(img_data)
        file_name = file_md5 + config.DEFUALT_IMG_TYPE
        _log.warning(f"[download] {url} 图片不存在扩展名，使用md5并添加扩展名：{file_name}")
    if config.IMG_RENAME_OPTIONS == ConfigType.ImgRenameType.MD5:
        file_md5 = Pic.calculate_md5_from_bytes(img_data)
        file_extension = os.path.splitext(file_name)[1] # 图片扩展名
        file_name = file_md5 + file_extension

    _log.info(f'[downlaod] {url} 处理后图片文件名：{file_name}')
    # 保存本地
    img_file_path = os.path.join(file_path, file_name)
    with open(img_file_path, 'w+') as f:
        f.buffer.write(img_data)
    return (img_file_path,file_name)


def handler_local_pics(url: str, file_path: str):
    """
    将本地图片也进行移动

    Returns:
    - 空字符串：处理失败
    - 非空字符串：(图片绝对路径，图片文件名)
    """
    return ("","")


def genarte_path(md_file_path:str):
    """根据配置的策略，创建一个文件的基础path(绝对路径)"""
    # 固定文件路径，直接返回设置好的文件路径
    if config.HANDLER_OPTIONS == ConfigType.HandlerType.FIX_DIR:
        return os.path.abspath(config.IMG_FIX_DIR)

    # 相对文件路径
    global RelDirList
    return RelDirList[md_file_path]


def handler_pics(md_file_path:str,url: str) ->tuple[str, str]:
    """图片处理函数，所有不带http的图片都认为是本地图片
    :return (图片绝对路径，图片文件名)
    """
    options = config.HANDLER_TARGET_OPTIONS
    img_file_base_path = genarte_path(md_file_path)
    if 'http' not in url and (options >= ConfigType.HandlerTarget.LOCAL_IMG_ONLY):
        return handler_local_pics(url,img_file_base_path)
    # 是否只处理本地图片
    if (options != ConfigType.HandlerTarget.LOCAL_IMG_ONLY):
        if config.NET_IMG_DOWNLOAD_INTERVAL != 0:
            time.sleep(config.NET_IMG_DOWNLOAD_INTERVAL)  # 避免网络图片下载超速
        return handler_network_pics(url,img_file_base_path)


#############################################################################################



if __name__ == '__main__':
    file = ""
    md_file_count = 0
    try:
        _log.info("[run] 开始处理md文件")
        # 获取MD_FILES_DIR路径下的所有文件列表
        files_list = Files.get_files_list(os.path.abspath(os.path.join('.', config.MD_FILES_DIR)))
        # 判断当前使用的是否为fix策略
        if config.HANDLER_OPTIONS == ConfigType.HandlerType.FIX_DIR:
            Files.create_dir(config.IMG_FIX_DIR)
            _log.info(f"[run] 已创建 IMG_FIX_DIR | {config.IMG_FIX_DIR}")

        md_content = ""
        for file in files_list:
            if '.md' not in file:
                _log.warning(f"[run] 不处理非md后缀文件: {file}")
                continue
            # 判断是否采用相对路径图片存放策略，如果是，需要创建dir
            if config.HANDLER_OPTIONS == ConfigType.HandlerType.REL_DIR:
                cur_dir = os.path.dirname(file)
                dir_sep = "/" if "\\" not in file else "\\" # 文件路径分隔符
                new_rel_dir = cur_dir + dir_sep + config.IMG_REL_DIR
                Files.create_dir(new_rel_dir) # 创建文件夹
                RelDirList[file] = new_rel_dir # 插入进去
                _log.info(f"[run] 已创建 IMG_REL_DIR | {new_rel_dir}")

            # 开始处理当前md文件
            _log.info(f'[run] {file} 文件开始处理')
            md_file_count += 1
            # 打开md文件
            md_content = Files.open_md_file(file, config.MD_ENCODING_OPTIONS)
            # 获取图片列表
            pics_list = Pic.get_pics_list_from_md_html(md_content)
            _log.info(f'[run] {file} 文件中发现图片 {len(pics_list)} 张')

            # 开始处理图片
            md_file_name = ""  # 初始化为空
            for index, pic in enumerate(pics_list):
                try:
                    _log.info(f'[run] {file} 正在处理第 {index + 1} 张图片，图片链接：{pic}')
                    md_file_name = os.path.basename(file)  # 当前处理的md文件的名字
                    # 处理图片，包括下载或者将图片移动到本地
                    new_img_file_path,new_img_file_name = handler_pics(file,pic)
                    if new_img_file_name == "" or new_img_file_path == "":
                        Files.add_err_pic(file, pic,"图片处理失败")  # 添加错误图片
                        _log.error(f'[run] {file} 图片处理出错，返回值为空，图片链接：{pic}')
                        continue
                    # 不为空说明处理成功
                    _log.info(f'[run] {file} 图片处理成功！图片原始链接：{pic} | 处理后：{new_img_file_name} | 文件位置：{new_img_file_path}')
                    # 如果需要，修改md文件内容
                    if config.IS_REPLACE_LINK and new_img_file_name != "":
                        # 是什么方式的修改？相对路径还是绝对路径？
                        if config.REPLACE_LINK_OPTIONS == ConfigType.ImgRelaceFileType.REl:
                            # 是相对路径，还需要一层转换
                            fix_img_file_path = new_img_file_path
                            if config.HANDLER_OPTIONS == ConfigType.HandlerType.REL_DIR:
                                new_img_file_path = RelDirList[file] + "/" + new_img_file_name
                            else:
                                _log.info(f"[run] {file} 相对路径计算，图片文件：{new_img_file_path}")
                                new_img_file_path = os.path.relpath(new_img_file_path,os.path.dirname(file))

                            _log.info(f'[run] {file} 相对路径图片链接修改，图片绝对路径：{fix_img_file_path} | 相对路径：{new_img_file_path}')
                        # 修改md文件中的内容
                        new_img_file_path = new_img_file_path.replace('\\', '/')  # 路径转linux风格
                        md_content = md_content.replace(pic, new_img_file_path)
                        _log.info(f'[run] {file} 修改md文件，图片原始链接：{pic} | 修改后：{new_img_file_path}')

                except KeyboardInterrupt:
                    Files.write_err_img_log_file()
                    _log.critical(f"[run] 收到键盘中断信号，程序停止\n终止时正在处理：{file}\n")
                    os.abort()  # 避免无法ctrl+c终止
                except Exception as result:
                    _log.exception(f"[run] {file} 出现未知处理错误！pic:{pic}")
                    Files.add_err_pic(file, pic,f"图片处理出现异常 {str(result)}")  # 添加错误图片
                    time.sleep(0.6)

            # 修改后的md写入文件
            if config.IS_REPLACE_LINK:
                Files.write_md_file(file, md_content, config.MD_ENCODING_OPTIONS)
                _log.info(f'[run] {file} 重新写入文件')
            # 处理完毕单个文件
            _log.info(f'[run] {file} 文件结束处理')

        # 结束后保存err
        _log.info(f'[run] 全部md处理完成，共计：{md_file_count}个')
        Files.write_err_img_log_file()
    except Exception as result:
        _log.exception(f"[run] 出现未知处理错误！count:{md_file_count} | file:{file}")
        Files.write_err_img_log_file()
        _log.critical(f"[run] 出现未知处理错误，abort!\n")
        os.abort()
