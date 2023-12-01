## 背景

本项目主要用于解析markdown文件中的图片链接，并将图片下载到本地。方便进行图床迁移，或者优化/修复md图片中的链接。

原作者的博客：[如何导出简书中的全部文章（包括图片）？](https://zhuanlan.zhihu.com/p/121155268)

## 配置项

在 [config.py](./config.py) 中列出了可选的配置项，并配备了注释，根据您的需求修改对应的配置文件即可。

## 运行

默认情况下，在当前路径创建 `files` 文件夹，并在 `files` 文件夹下创建 `img` 目录；

将md文件放入 `files` 文件夹（可以包含子文件夹，但是子文件夹名不能为 `img`）

> 执行之前，**请务必备份原有md文件**！一定要留备份！一定要留备份！

安装 `python3.10.x` 版本（其他版本不保证可以正常运行），执行如下命令

> 如果你对python不熟悉，可以直接去微软商店搜索python，安装python3.10版本。

```bash
# 安装依赖项
pip install -r requirements.txt
# 如果国内安装较慢，尝试使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

成功安装的结果应该显示的是`Successfully installed`，任何红字的Error错误输出都代表没有成功安装好依赖项。

![install-requirements](https://img.musnow.top/i/2023/12/65693e03284bd.png)

安装完毕依赖项，准备好md文件后，即可执行程序；再次提醒，**一定要留md文件备份**！

```
python spider.py
```

请保持网络稳定，耐心等待程序执行完成；

### 错误处理

执行完毕后，除了处理好的md和图片外，程序会生成以 `当前时间+err.json` 命名的错误图片文件，内部包含异常的图片链接，诸如无法下载、图片url无法解析等等问题。方便用户手动处理。

如有执行异常，程序会中止。如果需要帮助，请截图报错的详细内容，保留`img-parse.log`，并开启一个issue与我联系。

### 图片保存路径说明

如配置为绝对路径，图片将始终保存至config中IMG_FIX_DIR选项中的路径（默认为`./files/img`）

如配置为相对路径，脚本将自动在md文件同级文件夹下创建目录，并将图片保存其中。


## 欢迎与我交流

- [慕雪的寒舍](https://blog.musnow.top)