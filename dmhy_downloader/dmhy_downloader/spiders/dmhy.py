# -*- coding: utf-8 -*-
import scrapy
import re
from dmhy_downloader.items import DmhyDownloaderItem
from dmhy_downloader.settings import start_url, feature, start, end

#提取https://share.dmhy.org 或 http://dmhy.ye1213.com
url_part = re.match(r'^(.+\..+\.\w+)/?.*', start_url).group(1)

#判断url是否为https://share.dmhy.org(/) 或 http://dmhy.ye1213.com(/)
rule1 = re.compile(url_part + '(/?)$')
#判断url是否带有 /page/
rule2 = re.compile(r'.*/page/')
#提取url的各个部分
rule3 = re.compile(r'^(' + url_part + r'/topics/list/page/)(\d+)(.*)')
rule4 = re.compile(r'^(' + url_part + r'/topics/list)(.*)')

#将文件命名符合windows规范
def name_normalize(name):
    name = name.replace('\\', '')
    name = name.replace('/', '')
    name = name.replace(':', '：')
    name = name.replace('*', '')
    name = name.replace('?', '？')
    name = name.replace('"', '“')
    name = name.replace('<', '《')
    name = name.replace('>', '》')
    name = name.replace('|', ' ')
    return name

#返回需要下载的urls
def get_pages(url):
    temp = rule1.match(url)
    if temp:
        part = r'topics/list' if temp.group(1) == '/' else r'/topics/list'
        url += part
        print(url)

    if rule2.match(url):
        temp = rule3.match(url)
        pages = [temp.group(1) + str(i) + temp.group(3) for i in range(start, end + 1)]
    else:
        temp = rule4.match(url)
        pages = [temp.group(1) + '/page/' + str(i) + temp.group(2) for i in range(start, end + 1)]

    return pages

#匹配特征
rule = re.compile(feature)
#取得需要下载的urls
pages = get_pages(start_url)

class DmhySpider(scrapy.Spider):
    name = 'dmhy'
    allowed_domains = ['share.dmhy.org', 'dmhy.ye1213.com']
    start_urls = pages

    def parse(self, response):
        #解析页面上所有文件所在url以及名称
        torrents = response.xpath("//div[@class='clear']//table//tbody//tr//td[@class='title']//a[contains(@href,'html')]")

        for i in torrents:
            name_torrent = ''.join(i.xpath(".//text()").extract()).lstrip()
            #匹配名称
            if rule.match(name_torrent):
                item = DmhyDownloaderItem()
                item['name'] = name_normalize(name_torrent)
                #取得url
                url = response.urljoin(i.xpath("./@href").extract_first())
                yield scrapy.Request(url, meta={'item': item}, callback=self.get_torrent)


    def get_torrent(self, response):
        item = response.meta['item']
        #提取文件下载url
        item['torrent'] = 'https:' + response.xpath("//div[@id='tabs-1']//p[1]/a/@href").extract_first()

        yield item