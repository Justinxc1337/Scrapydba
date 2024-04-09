import scrapy


class ScrapydbaItem(scrapy.Item):
    model = scrapy.Field()
    pris = scrapy.Field()
    farve = scrapy.Field()
    #dato = scrapy.Field()
    #lokation = scrapy.Field()
    brændstof = scrapy.Field()
    modelår = scrapy.Field()
    service = scrapy.Field()
    pass