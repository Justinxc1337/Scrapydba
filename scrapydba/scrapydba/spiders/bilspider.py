import sqlite3
import scrapy
import re
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime


class BilspiderSpider(scrapy.Spider):
    name = "bilspider"
    
    def __init__(self, driver):
        super(BilspiderSpider, self).__init__()
        self.driver = driver

    def start_requests(self):
        URL = 'https://www.dba.dk/biler/biler/maerke-peugeot/modelpeugeot-108/'
        yield scrapy.Request(url=URL, callback=self.parse_front_page)

    def parse_front_page(self, response):
        # Extracting URLs of each advertisement on the front page
        ad_links = response.css('.listingLink')
        for ad_link in ad_links:
            ad_url = ad_link.css('a::attr(href)').extract_first()
            yield response.follow(ad_url, callback=self.parse_advertisement)

        # Follow next page link if available
        next_page_link = response.css('.trackClicks.pagination-modern-next.a-page-link::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse_front_page)

    def parse_advertisement(self, response):
        # Extracting model name = virker
        modelnavn = response.xpath('//*[@id="content"]/div[2]/article/div[4]/dl/dd[1]/text()').get()
        modelnavn = response.xpath('//*[@id="content"]/div[2]/article/div[5]/dl/dd[1]/text()').get() if not modelnavn else modelnavn

        # Extracting price = virker
        pris = response.xpath('//div[@class="vip-heading-bar row-fluid"]/div[@class="span8"]/div/div[2]/span/text()').get()

        # Extracting date = virker
        dato = response.xpath('//div[@class="vip-listing-info"]/span/text()').get()
        dato = dato.replace("Annonce oprettet:", "").strip() if dato else None

        # Extracting location = virker ikke da der er forskellige placeringer på siden
        lokation = response.xpath('//*[@id="business-card"]/div[2]/div[2]/div[2]/div[1]/div/p/text()').get()

        # Extracting kilometertal = virker ikke da der er forskellige placeringer på siden - hvor den blander kilometertal med modelår, farve og andre ting
        kilometertal = response.xpath('//*[@id="content"]/div[2]/article/div[5]/dl/dd[5]/text()').get()
        if kilometertal:
            match = re.search(r'\b(\d{1,3}(?:[.,\s]\d{3})+)\b', kilometertal)
            if match:
                kilometertal = int(match.group(1).replace('.', '').replace(',', '').replace(' ', ''))
                if kilometertal <= 5000:
                    return

        # Extracting color = virker ikke
        farve = response.xpath('//*[@id="content"]/div[2]/article/div[5]/dl/dd[6]/text()').get()

        # Extracting model year = virker ikke
        modelår = response.xpath('//*[@id="content"]/div[2]/article/div[5]/dl/dd[4]/text()').get()

        # Extracting fuel type = virker
        brændstof = response.xpath('//*[@id="content"]/div[2]/article/div[5]/dl/dd[2]/text()').get()
        brændstof = response.xpath('//*[@id="content"]/div[2]/article/div[4]/dl/dd[2]/text()').get() if not brændstof else brændstof

        yield {
            'model': modelnavn.strip() if modelnavn else None,
            'pris': pris.strip() if pris else None,
            'dato': dato,
            'lokation': lokation.strip() if lokation else None,
            'kilometertal': kilometertal,
            'farve': farve.strip() if farve else None,
            'modelår': modelår.strip() if modelår else None,
            'brændstof': brændstof.strip() if brændstof else None,
    }




def create_database_table(data):
    table_name = datetime.now().strftime("bil_data_%Y%m%d_%H%M%S")
    connection = sqlite3.connect('bil_data.db')
    cursor = connection.cursor()
    
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                    (model TEXT, pris TEXT, dato TEXT, lokation TEXT, kilometertal TEXT, farve TEXT, modelår TEXT, brændstof TEXT)''')
    
    for item in data:
        model = item['model']
        pris = item['pris']
        dato = item['dato']
        lokation = item['lokation']
        kilometertal = item['kilometertal']
        farve = item['farve']
        modelår = item['modelår']
        brændstof = item['brændstof']

        cursor.execute(f'''INSERT INTO {table_name} (model, pris, dato, lokation, kilometertal, farve, modelår, brændstof)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (model, pris, dato, lokation, kilometertal, farve, modelår, brændstof))
    connection.commit()
    connection.close()


def bil_spider_result():
    biler_results = []

    def crawler_results(item, response, spider):
        biler_results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    
    crawler_process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    })
    crawler_process.crawl(BilspiderSpider, driver=driver)
    crawler_process.start()
    
    driver.close()
    
    create_database_table(biler_results)
    return biler_results


if __name__ == '__main__':
    bil_data = bil_spider_result()