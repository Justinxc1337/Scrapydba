import scrapy


class ScrapydbaItem(scrapy.Item):
    model = scrapy.Field()
    pris = scrapy.Field()
    dato = scrapy.Field()
    lokation = scrapy.Field()
    kilometer = scrapy.Field()
    farve = scrapy.Field()
    modelår = scrapy.Field()
    brændstof = scrapy.Field()
    pass