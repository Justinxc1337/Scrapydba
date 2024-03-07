# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydbaItem(scrapy.Item):
    bilbillede = scrapy.Field()
    bilpris = scrapy.Field()
    bilmodel = scrapy.Field()
    bilregnr = scrapy.Field()
    bilårgang = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
