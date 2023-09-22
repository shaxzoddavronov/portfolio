# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CarscraperPipeline:
    def process_item(self, item, spider):

        adapter=ItemAdapter(item)

        field_names=adapter.field_names()
        for field_name in field_names:
            #if field_name!='price':
                value=adapter.get(field_name)
                if value is not None :
                    #value[0]=value[0].replace('–',' ') 
                    adapter[field_name]=value.strip()
                else:
                    adapter[field_name]=None

        value_price=adapter.get('price')      
        if value_price!='Not Priced':  
            value_price=value_price[1:]
            if value_price is not None:
            
                final_price=int(value_price.replace(',',''))
                adapter['price']=final_price
        else:
            adapter['price']=None

        value_drive=adapter.get('drive_train')
        value_splitted=value_drive.split('-')
        adapter['drive_train']=value_splitted[0].title()    

        value_vin=adapter.get('vin') 
        if len(value_vin)<15:
              adapter['mileage']=value_vin
              adapter['vin']=adapter.get('transmission')
              adapter['transmission']=None

        value_mileage=adapter.get('mileage')
        if value_mileage is not None or value_mileage!='–':
            value_splitted=value_mileage.split(' ') 
            #value_prep=int(value_splitted[0].replace(',',''))
            adapter['mileage']=value_splitted[0]
                
        value_year=adapter.get('year')
        #value_title_splitted=value_title.split(' ')
        adapter['year']=int(value_year)

        value_transmis=adapter.get('transmission')
        transmis_types=['Automatic','Manual']
        if value_transmis is not None:
            for n in transmis_types:
                if n in value_transmis: 
                    adapter['transmission']=n
        return item

import psycopg2
class SaveToPostreSqlPipeline:
     def __init__(self):
        self.conn=psycopg2.connect(
            dbname='books_db',
            user='postgres',
            password='qwerty20-2',
            host='localhost',
            port='5432')
        
        self.cur=self.conn.cursor()

        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS book_table(
                         id BIGSERIAL NOT NULL, url VARCHAR(250),brand VARCHAR(30),model VARCHAR(50),
                         mileage VARCHAR(15),price INT,year INT,exterior VARCHAR(30),
                         interior VARCHAR(30),drive_train VARCHAR(10),mpg VARCHAR(10),
                         fuel_type VARCHAR(15),transmission VARCHAR(30),engine VARCHAR(50),
                         vin VARCHAR(20),stock VARCHAR(15)
                        )
                    """)
        
     def process_item(self,item,spider):
     
        self.cur.execute(""" insert into books (
            url, brand, model, mileage, price,year,exterior,interior,
            drive_train,mpg,fuel_type,transmission,engine,vin,stock
            ) values (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                )""", (
            item["url"],item["brand"],item["model"],item["mileage"],
            item["price"],item["year"],item["exterior"],item["interior"],
            item["drive_train"],item["mpg"],item["fuel_type"],
            item["transmission"],item["engine"],item["vin"],item["stock"]
        ))

        self.conn.commit()
        return item

    
     def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        