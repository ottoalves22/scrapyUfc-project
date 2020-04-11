# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderufcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nickname = scrapy.Field()
    real_name = scrapy.Field()
    category_position = scrapy.Field()
    win_streak = scrapy.Field()
    win_ko = scrapy.Field()
    win_subm = scrapy.Field()
    strike_prec = scrapy.Field()
    grap_prec = scrapy.Field()
