import csv
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

#Test spider for DBA Biler, (kan nemt ændres til anden hjemmeside eller produkt)
#Test Bil Peugeot 108 (A.R)
#https://www.dba.dk/biler/biler/maerke-peugeot/modelpeugeot-108/

class BilspiderSpider(scrapy.Spider):
    name = "bilspider"

    def start_requests(self):
        URL = 'https://www.dba.dk/biler/biler/maerke-peugeot/modelpeugeot-108/'
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        for selector in response.css('td.mainContent'):
            yield {
                'pris': selector.css('.price::text').extract_first(),
                'dato': selector.css('.date::text').extract_first(),
                'lokation': selector.css('li > span::text').extract_first(),
                'modelaar': selector.css('td[title="Modelår"]::text').extract_first()             
            }

        #problem med at finde næste side, mulig grund li.next/næste (både og)
        next_page_link = response.css('li.next a::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.response_parser)
            
def bil_spider_result():
    biler_results = []

    def crawler_results(item):
        biler_results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(BilspiderSpider)
    crawler_process.start()
    return biler_results


if __name__ == '__main__':
    bil_data=bil_spider_result()

    keys = bil_data[0].keys()
    with open('bil_data.csv', 'w', newline='', encoding='utf-8') as output_file_name:
        writer = csv.DictWriter(output_file_name, keys)
        writer.writeheader()
        writer.writerows(bil_data)