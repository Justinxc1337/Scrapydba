# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydbaItem(scrapy.Item):
    pris = scrapy.Field()
    dato = scrapy.Field()
    lokation = scrapy.Field()
    #modelaar = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass