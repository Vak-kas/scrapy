import scrapy
from ..items import PracticeItem

class PracticeSpiderSpider(scrapy.Spider):
    name = "practice_spider"
    page_number = 2
    start_urls = [
        "https://www.scrapingcourse.com/ecommerce/page/1"
    ]

    def parse(self, response):
        # 제품 정보 추출
        product_names = response.css('.woocommerce-loop-product__title::text').extract()
        product_prices = response.css('span.price bdi::text').extract()
        image_links = response.css('.attachment-woocommerce_thumbnail::attr(src)').extract()

        for name, price, image in zip(product_names, product_prices, image_links):
            items = PracticeItem()
            items['product_name'] = name
            items['product_price'] = price
            items['image_link'] = image
            yield items

        next_page = f'https://www.scrapingcourse.com/ecommerce/page/{self.page_number}/'
        if self.page_number <= 12:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)