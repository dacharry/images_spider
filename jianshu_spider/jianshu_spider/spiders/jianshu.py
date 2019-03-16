# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from jianshu_spider.items import JianshuSpiderItem


class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath('//div[@class="article"]/h1/text()').get()
        author = response.xpath('//div[@class="author"]//span/a/text()').get()
        author_img = 'https:' + response.xpath('//div[@class="author"]/a[@class="avatar"]/img/@src').get()
        publish_time = response.xpath('//div[@class="meta"]/span[@class="publish-time"]/text()').get()
        words = response.xpath('//div[@class="meta"]/span[@class="wordage"]/text()').get()
        views_count = re.findall(r'"views_count":(\d+),',response.text)[0]
        print(views_count)
        comments = re.findall(r'"comments_count":(\d+),',response.text)[0]
        likes_count = re.findall(r'"likes_count":(\d+),',response.text)[0]
        content = response.xpath('//div[@class="show-content-free"]').get()
        url = response.url
        item = JianshuSpiderItem(
            title=title,
            author=author,
            author_img=author_img,
            publish_time=publish_time,
            words=words,
            views_count=views_count,
            comments=comments,
            likes_count=likes_count,
            content=content,
            url=url,
        )
        yield item

