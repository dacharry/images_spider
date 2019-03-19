# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
import re
from amazon.items import AmazonItem


class AmaSpider(RedisCrawlSpider):
    name = 'ama'
    allowed_domains = ['amazon.cn']
    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="leftNav"]/ul[1]/ul/div/li',))),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="leftNav"]/ul[2]/ul/div/li',))),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="resultsCol"]//ul/li//h2/..',)), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="pagn"]/span',)),),

    )

    # start_urls = [
    #     'https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=topnav_storetab_b?ie=UTF8&node=658390051',]
    redis_key = 'amazon'

    def parse_item(self, response):
        item = AmazonItem()
        item['name'] = response.xpath('//span[@id="productTitle"]/text()').extract_first()
        if item['name'] is None:
            item['name'] = response.xpath('//span[@id="ebooksProductTitle"]/text()').extract()
            item['name'] = "".join([i.strip() for i in item['name']])
            item['author'] = response.xpath('//div[@id="bylineInfo"]//a/text()').extract()
            item['author'] = (',').join([i.strip() for i in item['author'] if i.strip()])
            item['comments'] = response.xpath('//a[@id="cmrs-atf"]/text()').extract()
            item['img'] = response.xpath('//div[@id="ebooksImageBlockContainer"]//img/@data-a-dynamic-image').extract()
            item['pub_date'] = response.xpath('//div[@class="buying"]/span[2]/text()').extract_first()
            item['price'] = response.xpath('//span[@class="a-color-price"]//text()').extract_first()
            if item['price'] is None:
                item['price'] = response.xpath('//span[@class="a-size-base a-color-price a-color-price"]//text()').get()
            item['price'] = item['price'].strip()
            item['comments'] = response.xpath('//span[@id="acrCustomerReviewText"]/text()').get()
        else:
            item['pub_date'] = response.xpath('//h1[@id="title"]//span/text()').extract()
            item['pub_date'] = re.sub(' ', '', "".join(item['pub_date']))
            item['author'] = response.xpath('//div[@id="bylineInfo"]//a/text()').extract()
            item['author'] = (',').join([i.strip() for i in item['author'] if i.strip()])
            item['price'] = response.xpath('//span[@class="a-size-base a-color-price a-color-price"]//text()').get()
            if not item['price']:
                item['price'] = response.xpath('//span[contains(@class,"a-size-base")]/text()').get()
            item['price'] = item['price'].strip()
            item['comments'] = response.xpath('//span[@id="acrCustomerReviewText"]/text()').get()

            item['img'] = response.xpath('//div[@id="imageBlockContainer"]//img/@data-a-dynamic-image').extract()
        item['cate'] = response.xpath(
            '//ul[@class="a-unordered-list a-horizontal a-size-small"]//span[@class="a-list-item"]//text()').extract()
        item['cate'] = ">".join([i.strip() for i in item['cate']])
        item['url'] = response.url
        item['version'] = response.xpath('//li[@class="swatchElement selected"]//a/span/text()').extract_first()
        yield item
