import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quotes' #이름 변수, 스파이더 내부에서 사용할
    start_urls = [ #url 리스트가 필요함
        'https://quotes.toscrape.com/' #스크랩할 url
    ]

    def parse(self, response):
        title = response.css('title::text').extract()
        yield  {'titletext' : title}