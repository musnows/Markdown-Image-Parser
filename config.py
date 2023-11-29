################## 以下你可以根据自己的需要进行修改 ##################

IS_REPLACE_LINK = True
"""
是否修改md文件中的链接？
- True: 修改
- False: 维持原样
"""

REPLACE_LINK_OPTIONS = 1
"""
如何修改md文件中的链接？
- 1：相对路径
- 2：绝对路径
"""


HANDLER_OPTIONS = 2
"""
图片处理方式选择
- 1：统一下载到IMG_FIX_DIR路径
- 2：在每个包含md文件的文件夹下，创建一个目录用于存放资源文件，该目录名字可通过IMG_REL_DIR修改
"""

HANDLER_TARGET_OPTIONS = 3
"""
图片处理目标
- 1：只处理网络图片
- 2：只处理本地图片（移动文件）
- 3：同时处理网络和本地图片
"""

IMG_RENAME_OPTIONS = 2
"""
图片重命名方式选择
说明：如果一个网络图片没有文件后缀，则始终会采用 `图片md5 + DEFUALT_IMG_TYPE` 格式命名，和本选项无关
选项：
- 1：不重命名，采用图片原始名字（如果你的md文件中会出现两个同名图片，请不要选择此选项）
- 2: 使用图片md5进行重命名（这样可以保持图片名不冲突，普通用户遇到md5碰撞的可能性极低极低）
"""


################## 如果你不知道下面配置项说的是什么，请不要修改 ##################


MD_FILES_DIR = './files'
"""存放md文件的文件夹 """

IMG_FIX_DIR ='./files/img/'
"""存放下载好的本地图片的目录（仅对HANDLER_OPTIONS 1启用）"""

IMG_REL_DIR = "img"
"""存放下载好的本地图片的相对目录名（仅对HANDLER_OPTIONS 2启用）"""

DEFUALT_IMG_TYPE = '.png'
"""
给无后缀的图片网络url新增文件扩展名
- 建议测试一下到底是什么类型的图片，一般都是png
"""
MD_ENCODING_OPTIONS = "UTF-8"
"""
md文件编码
注：UTF-8可能会有编码报错，如果出现错误，尝试更为ISO-8859-1
"""

NET_IMG_DOWNLOAD_INTERVAL = 0.3
"""
网络图片处理间隔（休眠时间，避免下载超速）
- 单位：秒
- 设置为0不休眠
"""

def custom_net_img_url_check(img_url:str):
    """
    你可以修改这个函数，比如只下载某一部分url中的图片。
    - 返回值为True代表需要下载当前图片
    - 该函数只对网络图片生效
    """
    return True
