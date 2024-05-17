import scrapy
from  scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import QuotetutorialItem


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://quotes.toscrape.com/login'
    ]
    page_number = 2 #페이지 넘버를 저장할 변수

    def parse(self, response):
        token = response.css('form input ::attr(value)'). extract_first()
        # print("token : " , token)
        return FormRequest.from_response(response, formdata={
            'csrf_token' : token, 
            'username' : '1111', 
            'password' : '2222'
        },callback = self.start_scraping) #폼 네임, 폼 데이터, 클릭데이터
    

    def start_scraping(self, response):
        open_in_browser(response)
        items = QuotetutorialItem()
        
        all_div_quotes = response.css("div.quote")

        for quotes in all_div_quotes:

            title =  quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items



    
