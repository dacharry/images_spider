# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from boss.items import BossItem

from  scrapy.http.response.html import HtmlResponse
class ZhipingSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c100010000/?query=python&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'\?query=python&page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'job_detail/.*?\.html'), callback='parse_item'),
    )

    def parse_item(self, response):
        name = response.xpath('//div[@class="name"]/h1/text()').get()
        salary = response.xpath('//div[@class="name"]/span/text()').get().strip()
        job_info = response.xpath('//div[@class="info-primary"]/p/text()').getall()
        city = job_info[0]
        worked_years = job_info[1]
        education = job_info[2]
        company = response.xpath('//div[@class="company-info"]/a[1]/@title').get().strip()
        item = BossItem(name=name, salary=salary, city=city, worked_years=worked_years, education=education,
                        company=company)
        return item
