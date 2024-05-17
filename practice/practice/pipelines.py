# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class PracticePipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()


    def create_connection(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='@Dmsdnjf12#',
            database='practice',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS practice_tb""")
        self.curr.execute("""CREATE TABLE practice_tb (
                product_name VARCHAR(255),
                product_price VARCHAR(255),
                image_link VARCHAR(255)
                )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item
    

    def store_db(self, item):
        self.curr.execute("""INSERT INTO practice_tb (product_name, product_price, image_link) VALUES (%s, %s, %s)""", (
            item['product_name'],
            item['product_price'],
            item['image_link']
        ))
        self.conn.commit()

