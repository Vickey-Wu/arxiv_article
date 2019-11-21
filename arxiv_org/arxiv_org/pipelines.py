# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
import redis
from twisted.enterprise import adbapi


class ArxivOrgPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict('MYSQL_SETTINGS')
        dbparms = dict(
            host = db_settings['DB_HOST'],
            port = db_settings['DB_PORT'],
            db = db_settings['DB_DB'],
            user = db_settings['DB_USER'],
            passwd = db_settings['DB_PASSWD'],
            charset=db_settings['DB_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item


    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        logging.log(logging.INFO, 'insert failed' + str(failure))

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql, params = item.get_insert_sql()
        logging.log(logging.INFO, 'insert_sql, params' + insert_sql + str(params))
        cursor.execute(insert_sql, params)
