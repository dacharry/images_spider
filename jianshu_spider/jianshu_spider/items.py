# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuSpiderItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    author_img = scrapy.Field()
    publish_time = scrapy.Field()
    words = scrapy.Field()
    views_count = scrapy.Field()
    comments = scrapy.Field()
    likes_count = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()

