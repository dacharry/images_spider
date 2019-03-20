# -*- coding: utf-8 -*-
import re

import scrapy

from MaiTian.items import MaitianItem


class MaitionSpider(scrapy.Spider):
    name = 'maitian'
    # allowed_domains = ['bj.maitian.com']
    url = 'http://bj.maitian.cn/esfall/PG{}'
    page = 1
    start_urls = [url.format(page)]

    def parse(self, response):
        room_list = response.xpath('/html/body/section[2]/div[2]/div[2]/ul/li')
        # print(response.headers)
        if not room_list:
            return
        # print(room_list)
        for room in room_list:
            item = MaitianItem()
            item['title'] = room.xpath('.//h1/a/text()').extract_first()
            item['price'] = (',').join(room.xpath('.//div[@class="the_price"]//ol//text()').extract())
            item['price'] = re.findall(",(.*?)元",item['price'],re.S)[0]
            item['info'] = room.xpath('.//p//text()').extract()
            item['info'] = re.sub("\n|\s| ", '', "".join(item['info']))
            item['district'] = re.findall("\[(.*?)\]",item['info'],re.S)[0]
            item['area'] = room.xpath('.//p/span[1]/text()').extract_first()
            yield item
        print(response.request.headers)
        next_page = response.xpath('//div[@id="paging"]/a[text()="下一页"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page),callback=self.parse,dont_filter=True)


