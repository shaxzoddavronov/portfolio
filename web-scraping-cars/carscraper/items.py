# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CarItem(scrapy.Item):
    url=scrapy.Field()
    #title=scrapy.Field()
    exterior=scrapy.Field()
    interior=scrapy.Field()
    drive_train=scrapy.Field()
    mpg=scrapy.Field()
    fuel_type=scrapy.Field()
    transmission=scrapy.Field()
    engine=scrapy.Field()
    vin=scrapy.Field()
    stock=scrapy.Field()
    mileage=scrapy.Field()
    price=scrapy.Field()
    year=scrapy.Field()
    brand=scrapy.Field()
    model=scrapy.Field()