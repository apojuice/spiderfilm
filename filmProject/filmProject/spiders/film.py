# -*- coding: utf-8 -*-
import scrapy
import urllib.parse

class FilmSpider(scrapy.Spider):
    name = 'film'
    allowed_domains = ['www.id97.com/movie']
    start_urls = ['http://www.id97.com/movie/?page=1']

    page = 2
    def parse(self, response):
        div_list = response.xpath('//div[contains(@class,"movie-item-in")]')
        # 此处的for循环，解决是一页电影的解析功能
        for div in div_list:
            # 也可以使用itmes中的类创建对象，用字典对象也木有问题
            # 如果是使用items中的创建了对象，那么在使用item的时候有可能会涉及到类型转换的问题
            item = {}
            name = div.xpath('.//a[@style]/@title').extract_first()
            img_url = div.xpath('.//a[@style]/img/@data-original').extract_first()
            score = div.xpath('.//div[@class="meta"]//em/text()').extract_first()

            item = {
                'name':name,
                'img_url':img_url,
                'score':score
            }
            # 这里不返回item是因为这个item信息不完整，拿不到导演姓名
            # yield item
            # 想获取导演姓名，必须进入电影详情页，再进行解析
            # 解析电影详情页的网址
            detail_url = div.xpath('./a/@href').extract_first()
            # 返回一个request给引擎，这个request负责请求电影详情页的信息
            # callback函数是一个自定义的函数，它负责详情页里的导演姓名的解析
            # meta参数，使用用来在此函数和自定义函数parse_info之间传值的参数，以字典的形式设置
            # callback函数，在引擎获取到下载信息之后，就会触发调用，回传response对象，meta参数的内容也会封装在response对象中
            yield scrapy.Request(url=detail_url,callback=self.parse_info,meta={'item':item},dont_filter=True)

        # 爬取3页信息
        if self.page <= 3:
            # 解析完一页数据以后，再把新的网址传给引擎
            # 1. 先确定要提交的网址是啥
            data = {
                'page':self.page
            }
            data = urllib.parse.urlencode(data)

            next_url = 'http://www.id97.com/movie/?' + data

            self.page = self.page + 1
            # 2. 把新的url提交给引擎
            # dont_filter参数，设置不过滤此网址
            yield scrapy.Request(url=next_url,callback=self.parse,dont_filter=True)
    
    def parse_info(self, response):
        # 先从response中获取回传的item对象
        item = response.meta['item']
        # response.text 就是详情页的源代码
        # 所以就可以用详情页的解析逻辑来解析导演姓名
        director = response.xpath('//div[@class="row"]//div[@class="col-xs-8"]//tbody/tr[1]//a/text()').extract_first()
        # 拿到导演姓名，就可以把导演姓名写入到item对象中了
        item['director'] = director

        # 到此，item信息完整了，所以可以返回给itemp pipelines
        yield item
       
