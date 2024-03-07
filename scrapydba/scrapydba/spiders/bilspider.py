import csv
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

#Test Car Peugeot 108 (active)
#https://www.dba.dk/peugeot-108-10-vti-69-active/id-510005139/

class BilspiderSpider(scrapy.Spider):
    name = "bilspider"

    def start_requests(self):
        URL = 'https://www.dba.dk/peugeot-108-10-vti-69-active/id-510005139/'
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        for selector in response.css('div.vip-matrix-data'):
            yield {
                'bilmodel': selector.css('dl > dt::attr(div)').extract_first(),
                'bilmodelinfo': selector.css('dl > dd::attr(div)').extract_first(),
                #'bilpris': selector.css('.price_color::text').extract_first()
            }

        #next_page_link = response.css('li.next a::attr(href)').extract_first()
        #if next_page_link:
            #yield response.follow(next_page_link, callback=self.response_parser
            
def bil_spider_result():
    biler_results = []

    def crawler_results(item):
        biler_results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(BilSpider)
    crawler_process.start()
    return biler_results


if __name__ == '__main__':
    bil_data=bil_spider_result()

    keys = bil_data[0].keys()
    with open('bil_data.csv', 'w', newline='') as output_file_name:
        writer = csv.DictWriter(output_file_name, keys)
        writer.writeheader()
        writer.writerows(bil_data)