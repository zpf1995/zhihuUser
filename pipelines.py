# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class MongoDbPipeline(object):
    def __init__(self,mongoUrl,mongoDb):
        self.mongourl=mongoUrl
        self.mongodb=mongoDb
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongoUrl=crawler.settings.get('MONGOURL'),
            mongoDb=crawler.settings.get('MONGODB')
        )
    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongourl) #只要是用self都会设置一个全局的变量
        self.db=self.client[self.mongodb]
    def close_spider(self,spider):
        self.client.close()
    def process_item(self, item, spider):
        name=item.__class__.__name__
        self.db[name].update({'url_token':item['url_token']},{'$set':item},True)
        return item
