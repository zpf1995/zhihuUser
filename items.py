# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    avatar_url=Field()
    headline=Field()
    id=Field()
    name=Field()
    type=Field()
    url=Field()
    url_token=Field()

