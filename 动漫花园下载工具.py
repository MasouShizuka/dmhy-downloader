import requests
import re
import time
from bs4 import BeautifulSoup as bs

#输出路径
path_to = ''
#下载页面url
url = r''
#匹配文件名的正则表达式
name = r".*"
#起始页面数
start = 1
#种植页面数
end = 1
#下载间隔
interval = 3

url_part = re.match(r'^(.+\..+\..+?)\/.+', url).group(1)

#下载页面取得torrent的地址并下载
def download_url(url):
    try:
        res = requests.get(url)

    except Exception:
        print("下载页面错误: " + url)

    else:
        sp = bs(res.content, 'lxml')
        torrent = sp.find(name='a', attrs={'href': re.compile(r'\.torrent$')})
        url_torrent = 'https:' + torrent['href']

        try:
            file = requests.get(url_torrent)
            with open(path_to + '/' + torrent.string + '.torrent', 'wb') as f:
                f.write(file.content)
            print("下载完成: " + torrent.string + '.torrent')

        except Exception:
            print("下载错误: " + torrent.string + '.torrent')

#将页面上所有符合正则表达式的url组合成list，并传给download_url下载torrent
def download_page(page):
    try:
        res = requests.get(page)

    except Exception:
        print("打开页面错误: " + page)

    else:
        sp = bs(res.content, 'lxml')
        items = sp.find_all(name='a')
        items = list(filter(lambda x: re.match(name, x.get_text().lstrip()), items))
        for item in items:
            i = url_part + item['href']
            download_url(i)
            time.sleep(interval)

#由起始页面数和终止页面数以及url得到需要匹配的页面的url并通过download_page进行下载
def download_pages(url):
    if re.match(r'.*/page/', url):
        pages = re.match(r'^(' + url_part + r'/topics/list/page/)(\d+)(\?keyword=.+)', url)
        pages = [pages.group(1) + str(i) + pages.group(3) for i in range(start, end + 1)]
    else:
        pages = re.match(r'^(' + url_part + r'/topics/list)(\?keyword=.+)', url)
        pages = [pages.group(1) + '/page/' + str(i) + pages.group(2) for i in range(start, end + 1)]

    for page in pages:
        download_page(page)

if __name__ == '__main__':
    download_pages(url)