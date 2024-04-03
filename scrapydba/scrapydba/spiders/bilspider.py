import sqlite3
import scrapy
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
        modelnavn = response.xpath('//*[@id="content"]/div[2]/article/div[4]/dl/dd[1]/text()').get()
        modelnavn = response.xpath('//*[@id="content"]/div[2]/article/div[5]/dl/dd[1]/text()').get() if not modelnavn else modelnavn
        pris = response.xpath('//div[@class="vip-heading-bar row-fluid"]/div[@class="span8"]/div/div[2]/span/text()').get()
        dato = response.xpath('//div[@class="vip-listing-info"]/span/text()').get()
        lokation = response.xpath('//*[@id="business-card"]/div[2]/div[2]/div[2]/div[1]/div/p/text()').get()
        kilometertal = response.xpath('//div[@class="vip-matrix-data"]/dl/dd[14]/text()').get()
        farve = response.xpath('//div[@class="vip-matrix-data"]/dl/dd[16]/text()').get()
        modelår = response.xpath('//div[@class="vip-matrix-data"]/dl/dd[12]/text()').get()
        brændstof = response.xpath('//*[@id="content"]/div[2]/article/div[5]/dl/dd[2]/text()').get()
        brændstof = response.xpath('//*[@id="content"]/div[2]/article/div[4]/dl/dd[2]/text()').get() if not brændstof else brændstof
        

        yield {
            'model': modelnavn.strip() if modelnavn else None,
            'pris': pris.strip() if pris else None,
            'dato': dato.strip() if dato else None,
            'lokation': lokation.strip() if lokation else None,
            'kilometertal': kilometertal.strip() if kilometertal else None,
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
    
    # Initialize the WebDriver outside of the spider
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    
    crawler_process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    })
    crawler_process.crawl(BilspiderSpider, driver=driver)
    crawler_process.start()
    
    # Close the WebDriver after crawling is done
    driver.close()
    
    create_database_table(biler_results)
    return biler_results


if __name__ == '__main__':
    bil_data = bil_spider_result()