# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from scrapy.pipelines.images import ImagesPipeline
from bmw.settings import IMAGES_STORE


# class BmwPipeline(object):
#     def __init__(self):
#         self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
#         if not os.path.exists(self.file_path):
#             os.mkdir(self.file_path)
#
#
#     def process_item(self, item, spider):
#         return item


class BMWPipleline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(BMWPipleline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(BMWPipleline, self).file_path(request, response, info)
        category = request.item.get('category')
        images_store = IMAGES_STORE
        category_path = os.path.join(images_store, category)
        if not category_path:
            os.mkdir(category_path)
        image_name = path.replace("full/",'')
        image_path = os.path.join(category_path, image_name)
        return image_path
