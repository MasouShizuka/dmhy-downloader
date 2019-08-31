> #  dmhy downloader
---
## 批量下载动漫花园种子的脚本
---
## 说明
本工程使用python scrapy模块编写

---

## 用法

![screenshot 01](https://github.com/MasouShizuka/dmhy-downloader/blob/master/screenshot/screenshot%2001.jpg)

打开工程中的`settings.py`，按照注释填好，然后再运行`main.py`即可

#### 例如

```python
#文件保存路径
FILES_STORE = r'D:/torrents'
#下载页面的url
start_url = r'https://share.dmhy.org/topics/list?keyword=jojo'
#匹配下载文件名称的正则表达式
feature = r'.*\[简日双语\]'
#起始页面数
start = 1
#终止页面数
end = 2
```

*(提示：动漫花园镜网站 dmhy.ye1213.com 也可以)*



