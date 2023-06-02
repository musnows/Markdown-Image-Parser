## 背景

本项目主要用于解析markdown文件中的图片链接，并将图片下载到本地。方便进行图床迁移

原作者的博客：[如何导出简书中的全部文章（包括图片）？](https://zhuanlan.zhihu.com/p/121155268)

### 运行

在当前路径创建 `files` 文件夹，并在 `files` 文件夹下创建 `img` 目录；当前仓库已创建[占位目录](./files/)

将md文件放入 `files` 文件夹（可以包含子文件夹，但是子文件夹名不能为 `img`）

> 执行之前，请务必备份原有md文件！一定要留备份！一定要留备份！

安装 `python3.9` 以上版本 ，执行如下命令

```bash
# 安装依赖项
pip install -r requirements.txt

# 执行程序
python spider.py
```

请保持网络稳定，耐心等待程序执行完成；

执行完毕后，程序会生成以 `当前时间+err.json` 命名的错误图片文件，内部包含异常的图片链接。

### 图片保存说明

> 如果md文件中的图片有重名，无法正常保存，会发生冲突

解释一下当前项目保存图片的逻辑，假设有如下图片链接

```
https://example.com/23/01/01/234aa23.jpg
```

保存图片的时候，会以 `234aa23.jpg` 命名图片，保存到 [./files/img](./files/img/) 中；

脚本执行结束后，您只需要使用 `notepad++`、`vscode` 等可以批量替换文本的编辑器，将原有md文件中的 `https://example.com/23/01/01/` 部分替换为本地路径，即可看到图片。

个人使用本项目，主要是迁移、备份图床里面的图片（同时还能规避掉那些没有被md文件引用的图片）

所以**默认**您的图片是已经采用过诸如 **hash、md5、uuid、时间戳** 等各类保证文件名不重复的命名方式。

如果你的md文件中的图片外链，采用的是图片原始名字作为外链名字，那么本项目并不适合您使用。因为保存图片的时候，会因为最终图片文件名相同，而导致大量冲突。

----

## 代码思路

首先是要解析markdown文档，然后获取到其中的所有图片，再把图片按md文件分好目录保存。

### 解析markdown文档
这里我用了misaka模块，据说是python的markdown解析器里性能最好的，不过这个的文档着实是精简，太少内容了，写得不清不楚的，基本功能看来就是把markdown文档解析为html文档，但是好像没有直接操作markdown元素的方法。

没事，我可以像平时写爬虫那样解析html呀，不就曲线救国拿到图片了吗~
这里就用BeautifulSoup啦

### 下载图片
很简单，就是requests，没啥好说的。

## 实现
### 遍历文件
首先要遍历文件夹里面的所有md文档：
```python
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
```

### 解析md文档 获取所有图片
先用misaka把markdown转换成html，然后再拿出所有img。
```python
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
```

### 下载图片
```python
def download_pics(url, file):
    img_data = requests.get(url).content
    filename = os.path.basename(file)
    dirname = os.path.dirname(file)
    targer_dir = os.path.join(dirname, f'{filename}.assets')
    if not os.path.exists(targer_dir):
        os.mkdir(targer_dir)

    with open(os.path.join(targer_dir, f'{uuid.uuid4().hex}.jpg'), 'w+') as f:
        f.buffer.write(img_data)
```

## 欢迎与我交流

- [慕雪的寒舍](https://blog.musnow.top)