# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FilmprojectItem(scrapy.Item):
	# 电影名称
	name = scrapy.Field()
	# 图片链接
	img_url = scrapy.Field()
	# 电影评分
	score = scrapy.Field()

	# 导演姓名
	director = scrapy.Field()
