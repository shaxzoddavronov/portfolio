import scrapy
from carscraper.items import CarItem
import random
class CarspiderSpider(scrapy.Spider):
    name = "carspider"
    allowed_domains = ["www.cars.com"]
    start_urls = ["https://www.cars.com"]

    #user_agent_list = [
    #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    #'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    #'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
        #]

    def parse(self, response):
        first_page='https://www.cars.com/shopping/results/?stock_type=all&makes%5B%5D=&models%5B%5D=&list_price_max=&maximum_distance=all&zip='
        yield response.follow(first_page,callback=self.parse_next_page)

    def parse_next_page(self,response):
        next_page_href=response.css('a#next_paginate ::attr(href)').get()
        if next_page_href is not None:
            next_page_url='https://www.cars.com'+next_page_href
            yield response.follow(next_page_url,callback=self.parse_next_page)

        cars=response.css('div.vehicle-card')

    

        for car in cars:
            relative_href=car.css('a.vehicle-card-link ::attr(href)').get()
            if relative_href is not None:
                relative_url='https://www.cars.com'+relative_href
                yield response.follow(relative_url,callback=self.parse_car_page)

    def parse_car_page(self,response):
        table_rows=response.css('dl.fancy-description-list dd')

        car_item=CarItem()

        car_item['url']=response.url
        car_item['brand']=response.css('h1.listing-title ::text').get().split(' ')[1]
        car_item['model']=' '.join(response.css('h1.listing-title ::text').get().split(' ')[2:]) 
        car_item['mileage']=table_rows[9].css('::text').get()
        car_item['price']=response.css('div.price-section span.primary-price ::text').get()
        car_item['year']=response.css('h1.listing-title ::text').get().split(' ')[0]           
        #car_item['title']=response.css('h1.listing-title ::text').get()
        car_item['exterior']=table_rows[0].css('::text').get()
        car_item['interior']=table_rows[1].css('::text').get()
        car_item['drive_train']=table_rows[2].css('::text').get()
        car_item['mpg']=table_rows[3].css('span[data_qa="mpg"] ::text').get()
        car_item['fuel_type']=table_rows[4].css('::text').get()
        car_item['transmission']=table_rows[5].css('::text').get()
        car_item['engine']=table_rows[6].css('::text').get()
        car_item['vin']=table_rows[7].css('::text').get()
        car_item['stock']=table_rows[8].css('::text').get()
        
        yield car_item
        