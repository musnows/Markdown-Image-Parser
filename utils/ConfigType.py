# 修改此文件的时候，记得修改config.py中的文件注释！

class HandlerType:
    """图片文件存在哪里？"""
    FIX_DIR = 1
    """统一存放到固定文件夹"""
    REL_DIR = 2
    """创建专门的assets文件夹"""

class HandlerTarget:
    """处理什么类型的图片？"""
    NET_IMG_ONLY = 1
    """只处理网络图片"""
    LOCAL_IMG_ONLY = 2
    """只处理本地图片"""
    NET_LOCAL_BOTH = 3
    """同时处理本地和网络图片"""

class ImgRenameType:
    """图片文件是否需要重命名？"""
    BASE_NAME = 1
    """不进行重命名"""
    MD5 = 2
    """使用md5进行重命名"""

class ImgRelaceFileType:
    """如何如果需要修改md文件，依照什么方式修改文件链接？"""
    REl = 1
    """相对路径"""
    FIX = 2
    """绝对路径"""
