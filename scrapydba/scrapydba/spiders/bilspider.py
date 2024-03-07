import csv
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher


class BilspiderSpider(scrapy.Spider):
    name = "bilspider"

    def start_requests(self):
        URL = 'https://www.dba.dk/'
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        for selector in response.css('article.product_pod'):
            yield {
                'bilmodel': selector.css('h3 > a::attr(title)').extract_first(),
                'bilpris': selector.css('.price_color::text').extract_first()
            }

        next_page_link = response.css('li.next a::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.response_parser