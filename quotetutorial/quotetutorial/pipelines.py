# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class QuotetutorialPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='@Dmsdnjf12#',
            database='myquotes',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.curr.execute("""CREATE TABLE quotes_tb (
                title VARCHAR(255),
                author VARCHAR(255),
                tag VARCHAR(255)
                )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""INSERT INTO quotes_tb (title, author, tag) VALUES (%s, %s, %s)""", (
            item['title'][0],
            item['author'][0],
            item['tag'][0]
        ))
        self.conn.commit()