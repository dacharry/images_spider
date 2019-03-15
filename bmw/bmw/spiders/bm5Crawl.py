# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from bmw.items import BmwItem


class Bm5crawlSpider(CrawlSpider):
    name = 'bm5Crawl'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/202.html']

    # 只是提取a标签的url
    rules = (
        Rule(LinkExtractor(allow=r'https://car\.autohome\.com\.cn/pic/series/202-.*?.html'), follow=True,
             callback="parse_item"),

    )

    def parse_item(self, response):
        img_urls = response.xpath('//div[@class="uibox"]//img/@src').getall()
        img_urls = list(map(lambda url:url.replace("t_",''),img_urls))
        img_urls = list(map(lambda url:response.urljoin(url),img_urls))
        category = response.xpath('//div[@class="uibox-title"]/text()').getall()
        category = [i.strip() for i in category if i.strip()][0]
        yield BmwItem(category=category,image_urls=img_urls)
        # return item
