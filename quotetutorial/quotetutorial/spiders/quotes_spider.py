import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quotes' #이름 변수, 스파이더 내부에서 사용할
    start_urls = [ #url 리스트가 필요함
        'https://quotes.toscrape.com/' #스크랩할 url
    ]

    def parse(self, response):
        all_div_quotes = response.css("div.quote")[0]
        title =  all_div_quotes.css('span.text::text').extract()
        author = all_div_quotes.css('.author::text').extract()
        tag = all_div_quotes.css('.tags::text').extract()
        yield {
            'title' : title,
            'author' : author,
            'tag' : tag
        }

        


        



        
