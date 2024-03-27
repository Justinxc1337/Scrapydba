import scrapy


class ScrapydbaItem(scrapy.Item):
    model = scrapy.Field()
    pris = scrapy.Field()
    dato = scrapy.Field()
    lokation = scrapy.Field()
    kilometertal = scrapy.Field()
    #modelaar = scrapy.Field()
    pass