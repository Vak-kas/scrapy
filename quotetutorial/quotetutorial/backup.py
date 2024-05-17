import scrapy
from ..items import QuotetutorialItem
class QuoteSpider(scrapy.Spider):
    name = 'quotes' #이름 변수, 스파이더 내부에서 사용할
    start_urls = [ #url 리스트가 필요함
        # 'https://quotes.toscrape.com/' #스크랩할 url
        'https://quotes.toscrape.com/page/1/'
    ]
    page_number = 2 #페이지 넘버를 저장할 변수

    def parse(self, response):
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

        # next_page = response.css('li.next a::attr(href)').get()
        next_page = f'https://quotes.toscrape.com/page/{str(QuoteSpider.page_number)}/'

        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

        if QuoteSpider.page_number < 11:
            QuoteSpider.page_number+=1
            yield response.follow(next_page, callback=self.parse)


        


        



        
