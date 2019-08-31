# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
from dmhy_downloader.settings import FILES_STORE
import os

if not os.path.exists(FILES_STORE):
    os.mkdir(FILES_STORE)

class DmhyDownloaderPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['torrent'], meta={'name': item['name']})

    def file_path(self, request, response=None, info=None):
        name = request.meta['name']
        return name + '.torrent'

    def item_completed(self, results, item, info):
        ok, x = results[0]
        if ok:
            print('下载完成: ' + item['name'])
        else:
            print('失败: ' + item['name'])
