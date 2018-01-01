# -*- coding: utf-8 -*-
import json

import scrapy

from zhihuUser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user='excited-vczh'
    follow_url='https://www.zhihu.com/api/v4/members/{user}/{follow}?include={include}&offset={offset}&limit={limit}'
    follow_include='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    user_url='https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_include='allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    def start_requests(self): #这个就是刚开始的时候的url地址
        #<editor-fold desc="起始信息">
        #用户的详细信息
       # url='https://www.zhihu.com/api/v4/members/joan-84-74?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        #用户的关注列表信息
        # url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
        #</editor-fold>
        yield scrapy.Request(self.user_url.format(user=self.start_user, include=self.user_include),callback=self.parse_user)
        yield scrapy.Request(self.follow_url.format(user=self.start_user, follow='followers', include=self.follow_include, offset=0,limit=20), callback=self.parse_follow)
        yield scrapy.Request(self.follow_url.format(user=self.start_user,follow='followees',include=self.follow_include,offset=0,limit=20),callback=self.parse_follow)


    def parse_user(self, response):
        results=json.loads(response.text)
        item=UserItem()
        for field in item.fields:
            if field in results.keys():
                item[field]=results.get(field)
        yield item
        yield scrapy.Request(self.follow_url.format(user=results.get('url_token'), follow='followers', include=self.follow_include,offset=0, limit=20), callback=self.parse_follow)
        yield scrapy.Request(self.follow_url.format(user=results.get('url_token'),follow='followees',include=self.follow_include,offset=0,limit=20),callback=self.parse_follow)

    def parse_follow(self, response):
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_include),callback=self.parse_user)
        if 'paging' in results.keys():
            if results.get('paging').get('is_end')==False:
                next_page=results.get('paging').get('next')
                yield scrapy.Request(next_page,callback=self.parse_follow)
