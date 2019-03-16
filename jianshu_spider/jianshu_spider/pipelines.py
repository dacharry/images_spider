# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi


class JianshuSpiderPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'jianshudb',
            'charset': 'utf8',
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['author'], item['author_img'],
                                       item['publish_time'], item['words'], item['views_count'],
                                       item['comments'], item['likes_count'], item['content'], item['url'])
                            )
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
            insert into jianshu(id,title,author,author_img,publish_time,
            words,views_count,comments,likes_count,content,url) value(null,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            return self._sql
        return self._sql


class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'jianshudb',
            'charset': 'utf8',
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
                        insert into jianshu(id,title,author,author_img,publish_time,
                        words,views_count,comments,likes_count,content,url) value(null,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        '''
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['author'], item['author_img'],
                                  item['publish_time'], item['words'], item['views_count'],
                                  item['comments'], item['likes_count'], item['content'], item['url']
                                  )
                       )

    def handle_error(self, error, item, spider):
        print('*' * 40)
        print(error)
