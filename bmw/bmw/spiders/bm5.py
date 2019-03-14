# -*- coding: utf-8 -*-
import scrapy

from bmw.items import BmwItem


class Bm5Spider(scrapy.Spider):
    name = 'bm5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/202.html#pvareaid=3454507']

    def parse(self, response):
        uiboxs = response.xpath('//div[@class="uibox"]')
        for uibox in uiboxs[1:]:
            category = uibox.xpath('./div[@class="uibox-title"]/a[1]/text()').get()
            imgs = uibox.xpath('.//ul/li//img/@src').getall()
            imgs = list(map(lambda url:response.urljoin(url), imgs))
            item = BmwItem(category=category, image_urls=imgs)
            yield item