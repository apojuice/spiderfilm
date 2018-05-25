# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import urllib.request

class FilmprojectPipeline(object):

    # 应该首次运行工程就打开文件
    def open_spider(self,spider):
        self.fp = open('film.json','w',encoding='utf-8')

    # 退出程序就关闭文件
    def close_spider(self,spider):
        self.fp.close()

    # 此处的item参数就是从film.py中的parse方法返回的
    # 每返回一个item，这个方法就调用一次
    def process_item(self, item, spider):

        string = json.dumps(item,ensure_ascii=False)
        self.fp.write(string + '\n')
        
        # 下载图片
        img_url = item['img_url']
        name = item['name']
        # img_path = r'C:\Users\ALIENWARE\Desktop\day7\filmimages\\' + name + '.jpg'
        # urllib.request.urlretrieve(img_url,img_path)

        return item
