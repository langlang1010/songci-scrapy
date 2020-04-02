# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 获得所有的URL和Name
class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # 词名（含词牌名）
    name = scrapy.Field()
    # 时期
    dynasty = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 内容
    content = scrapy.Field() 
    # 翻译
    explanation = scrapy.Field() 
    # 注释
    note = scrapy.Field()  