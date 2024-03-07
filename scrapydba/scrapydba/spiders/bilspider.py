import scrapy


class BilspiderSpider(scrapy.Spider):
    name = "bilspider"
    allowed_domains = ["www.dba.dk"]
    start_urls = ["https://www.dba.dk/"]

    def parse(self, response):
        pass
