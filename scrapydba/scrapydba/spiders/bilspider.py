import csv
import sqlite3
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from datetime import datetime

# Test spider for DBA Biler, (kan nemt ændres til anden hjemmeside eller produkt)
# Test Bil Peugeot 108 (A.R)
# https://www.dba.dk/biler/biler/maerke-peugeot/modelpeugeot-108/

class BilspiderSpider(scrapy.Spider):
    name = "bilspider"

    def start_requests(self):
        URL = 'https://www.dba.dk/biler/biler/maerke-peugeot/modelpeugeot-108/'
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        for selector in response.css('td.mainContent'):
            model = selector.css('.text::text').get()
            modelnavn = ' '.join(model.split()[:5])
            yield {
                'model': modelnavn,
                'pris': selector.css('.price::text').extract_first(),
                'dato': selector.css('.date::text').extract_first(),
                'lokation': selector.css('li > span::text').extract_first(),             
            }
            
        next_page_link = response.css('.trackClicks.pagination-modern-next.a-page-link::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.response_parser)

def create_database_table(data):
    table_name = datetime.now().strftime("bil_data_%Y%m%d_%H%M%S")
    connection = sqlite3.connect('bil_data.db')
    cursor = connection.cursor()
    
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                    (model TEXT, pris TEXT, dato TEXT, lokation TEXT)''')
    
    for item in data:
        
        model = item['model'].encode('utf-8')
        pris = item['pris'].encode('utf-8')
        dato = item['dato'].encode('utf-8')
        lokation = item['lokation'].encode('utf-8')

        cursor.execute(f'''INSERT INTO {table_name} (model, pris, dato, lokation)
                        VALUES (?, ?, ?, ?)''', (model, pris, dato, lokation))
    connection.commit()
    connection.close()

def bil_spider_result():
    biler_results = []

    def crawler_results(item):
        biler_results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(BilspiderSpider)
    crawler_process.start()
    
    create_database_table(biler_results)
    write_to_csv(biler_results)
    return biler_results

def write_to_csv(data):
    keys = data[0].keys()
    with open('bil_data.csv', 'w', newline='', encoding='utf-8') as output_file_name:
        writer = csv.DictWriter(output_file_name, keys)
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    bil_data = bil_spider_result()