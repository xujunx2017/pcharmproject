#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
import urllib.request
import os

class XiaoHuaSpider(scrapy.spiders.Spider):
    """
        name:scrapy唯一定位实例的属性，必须唯一
        allowed_domains：允许爬取的域名列表，不设置表示允许爬取所有
        start_urls：起始爬取列表
        start_requests：它就是从start_urls中读取链接，然后使用make_requests_from_url生成Request，
                        这就意味我们可以在start_requests方法中根据我们自己的需求往start_urls中写入
                        我们自定义的规律的链接
        parse：回调函数，处理response并返回处理后的数据和需要跟进的url
        log：打印日志信息
        closed：关闭spider
        """

    name = "xiaohua"   #爬虫名
    allowed_domains = ["xiaohuar.com"]
    start_urls = []
    for i in range(2):
        url = "http://www.xiaohuar.com/list-1-%s.html" % i
        start_urls.append(url)


    def parse(self, response):
        #print(response.url)
        div_list = Selector(response).xpath('//div[@class="img"]/a/img/@src').extract()
        offset =0
        for url in div_list:
            #print(url)
            if '/d/file' in url:
                url1 = 'http://www.xiaohuar.com'+url
                id = url1.split('/')[-1]
                urllib.request.urlretrieve(url1, filename=os.getcwd()+'\\校花'+'\\'+id)
            else:
                id2 = url.split('/')[-1]
                urllib.request.urlretrieve(url, filename=os.getcwd() + '\\校花' + '\\' + id2)

