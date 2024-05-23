Scrapy


Settings.py

- BOT_NAME : 크롤링을 자동화 해주는 봇의 이름 정도라고 생각. 프로젝트 이름과 같음.
- USER_AGENT : 구글같은 곳에 접속할 때 내가 누구인지 알려주는 것. 나는 단지 Firebox 브라우저 이다….도메인 이름도 직접 지정할 수 있다. 많은 웹 사이트에서 웹 스크래핑에 많은 제한을 두게 되므로 앞으로는 책임감을 갖고 스크래핑을 해야한다.
- ROBOTSTXT_OBEY : 로봇.txt에서 제한하고 있는 스크래핑 설정을 따를 것이냐? True면 자동적으로 해당 규칙에 맞춰서 따라가고, 아니라면 무시함
- Concurrent_request : 동시에 얼마나 많은 요청을 할 수 있는가?에 대한 설정. 기본 요청수는 16개. 초당 16개의 요청을 보내는데, 이거 수 많아지면 디도스 보내는 것과 똑같다고 생각하면 된다.
- AUTOTHOTTLE :  데이터 오버로드 되지 않게 하는?

Items.py
튜로리얼 항목이 존재하는데, 항목에 대한 필드를 정의하라고 나온다


quotes.toscrape.com에 일단 가보자.
첫번째로 스파이더에서 스크랩할 웹 사이트인데, 우리가 마음대로 해도됨. 하라고 만들어놓은 곳임.

이 웹사아ㅣ트에는 많은 코드가 있고, 해당 코스에 대한 작성자가 있는데 
스크랩할 때마다 특정 항목 필드가 있다. 이거를 items에서 정의한다고 생각하면 된다?

Pipelines.py : JSON파일 같은 거를 데이터베이스 에 저장할 수 있도록 하는 곳. 웹에서 스크랩한 데이터 또는 스크립트가 제대로 처리되고 의도한 위치로 이동하는지 확인해야한다.


middlewares.py : request 요청을 보낼 때 몇가지 요청을 보낼 때 항목을 추가할 수 있다.
프로시를 추가할 경우 요청 프록시는 기본적으로 웹 사이트의 웹 스크래핑에 대한 제한을 우회하는 악마다. 요청에 프록시를 추가할 때마다 미들웨어를 통해 수행하게 함. 웹 사이트에서 응답을 다시 보내면 해당 응답을 처리할 수도 있다.


Spider 디렉터리 밑에 아무 이름.py 파일을 만들고 아래와 같이 작성하자


import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quotes' #이름 변수, 스파이더 내부에서 사용할
    start_urls = [ #url 리스트가 필요함
        'https://quotes.toscrape.com/' #스크랩할 url
    ]

    def parse(self, response):
        title = response.css('title').extract()
        yield  {'titletext' : title}


Name, start_urls, parse 이 세 개는 반드시 저대로 지어야함

그 다음에, 현재 parse에서는, title을 뽑아오는 것을 하고 있는데, 일단 왜 response.css(‘title) 에서 css가 들어가는 이유를 잘 모르겠음.

지피티한테 물어보니까 css 선택자를 이용해서 가져온다 라고 되어 있는데 css 선택자가 <> 이것도 들어가는 거여서, title을 잘 가져 올 수 있는 것 

yield 문은 Scrapy에서 아이템을 비동기적으로 반환하는 데 사용되며, 이는 데이터가 후속 처리 단계로 넘어가도록 합니다. 여기서 생성된 아이템({'titletext': title})은 파이프라인에서 후속 처리를 위해 사용될 수 있습니다.
라고하는데, 대충 후속처리이다. Yield	는 반복가능한 객체를 만드는 데 사용된다


yield는 제너레이터를 만드는데, 스크래피에서 scenes를 만드는데 쓰인다?


Pip install —upgrade twists, pip install —upgrade scrapy를 해주고
Scrapy crawl “이름” 이때 이름은 아까 class QuoteSpider에서 설정한 이름을 설정해주고 실행하면
잘 나온다

{'titletext': ['<title>Quotes to Scrape</title>']}
이렇게 나오는데, 우리가 원하는 건 태그 말고 단어만 나오고 싶다?

        title = response.css('title::text').extract()
이렇게 바꿔주면 된다.

{'titletext': ['Quotes to Scrape']}
이렇게 나온다.

ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

scrapy shell "https://quotes.toscrape.com/"

이렇게 하면, 해당 사이트에서 shell로 크롤링을 할 수가 있는데
아까 본 명령어들 사용가능하다
response.css("title::text").extract()
이렇게 가능한데

response.css(“title::text”)[0].extract() 이거나
response.css(“title:text”).extract_first() 나 같은 거 나온다

맨 앞에 있는 게 [0]을 사용한다면 오류가 발생하는데, extract_first()를 사용하면 null이 나온다
그래서 인덱스를 쓰는 것 보단 first() 이런식으로 사용하는 것을 추천한다

만약
<span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>
이렇게 생긴 거 가져오고 싶다?
response.css(“span.text::text”)
하면 된다.

Class 를 가져오는 거기 때문에 span 에서의 클래스 . 을 붙여서 사용한다




Selector gadget chrome을 이용해서, 해당 스타일 부분 추출가능

ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
셀렉터에는 두 가지가 있다
하나는 이전까지 썼던 css 셀렉터
두 번째는 xpath 셀렉터이다

response.xpath("//title").extract()
이렇게 사용한다
response.xpath("//title/text()").extract()
text만 추출할려면, css선택자를 사용했을 때에는 ::text를 붙였었지만, xpath 선택자를 사용할려면 /text() 를 붙여주어야한다.

그렇다면 아까처럼, span.text::text 	를 하고 싶으면?

response.xpath("//span[@class='text']/text()").extract()
좀 복잡해졌다.
//span 뒤에 [] 이렇게 들어가는데, 클래스임을 명시해주기 위해 @class가 붙고 @class=‘text’ 가 들어간다. 이걸 text로 출력하기 위해 /text()가 붙는다

얘도 인덱스 가능
Id 할 경우 @id”text” 이렇게 하면 된다

큰따옴표, 작은따옴표 조심할 것!

response.css("li.next a").xpath("@href").extract()
이렇게 하면
<li class="next">
                <a href="/page/2/">Next <span aria-hidden="true">→</span></a>
            </li>
여기서
href에서 연결된 링크를 가져올 수 있음

response.css("a").xpath("@href").extract()
이렇게 쓰면 모든 연결된 링크를 싹 가져올 수 있음
xpath는 유니크한 거 가져올때 사용함

ㅇㅋ 이제 잘 됐는데
문제는 만약에 1ㄷ1 이면 상관이 없는데 1ㄷ다 이런 관계라면, 무엇에 무엇이 있는지 매칭이 안 될 것이기에
for 문으로 실행한다

import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quotes' #이름 변수, 스파이더 내부에서 사용할
    start_urls = [ #url 리스트가 필요함
        'https://quotes.toscrape.com/' #스크랩할 url
    ]

    def parse(self, response):
        
        all_div_quotes = response.css("div.quote")

        for quotes in all_div_quotes:

            title =  quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()
            yield {
                'title' : title,
                'author' : author,
                'tag' : tag
            }

        


이런식으로 설정을 하면 된다.

ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

추출된 데이터 -> 임시 컨테이너(items) -> 데이터베이스에 저장
추출된 데이터를 바로 데이터베이스에 저장하는 것은 오류가 많고 힘들기에, 임시 컨테이너에 데이터를 저장하고 이를 저장해야한다.

items.py 에서 작성을 하는 데
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotetutorialItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    

이러식으로 작성했다.

그다음, quotes_spider.py 를
import scrapy
from ..items import QuotetutorialItem
class QuoteSpider(scrapy.Spider):
    name = 'quotes' #이름 변수, 스파이더 내부에서 사용할
    start_urls = [ #url 리스트가 필요함
        'https://quotes.toscrape.com/' #스크랩할 url
    ]

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

        

이렇게 수정하면 items에 저장하는 방식으로 설정이 되었고, 임시 저장소에 저장하는 방식으로 되었다. 이제 이걸 데이터베이스에 저장해야한다.
어떻게 추출된 데이터를 JSON 파일이나 CSV 파일이나 XML 파일에 저장하는가 부터 배우고, 이걸 이제 나중에 SQLite 에 저장하는 법을 배운다.
일단 파일로 저장하는 법 부터 확인하다...


scrapy crawl quotes -o items.json
이렇게 하면 items.json으로 저장이 됨
맨 뒤에 .json/.xml/.csv 로 설정해주면 됨
와 ! 매우 쉽다!

ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
데이터 베이스에 저장하기 전에 itmes에 저장을 했는데, 이 다음 한 가지 단계가 더 있다.
파이프 라인 설정을 해야한다.

ITEM_PIPELINES = {
   "quotetutorial.pipelines.QuotetutorialPipeline": 300,
}
settings.py 에서 해당 라인을 킨다. 맨 뒤에 300 이건 우선순위를 의미한다. 낮으면 우선순위가 더 높음!

ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

데이터 베이스를 만들자
database.py 파일을 만들고
import sqlite3

conn = sqlite3.connect('myquotes.db')
이렇게 하고 실행을 하며 데이터베이스가 만들어진다.

커서(cursor)는 데이터베이스에서 SQL 쿼리를 실행하고 그 결과를 처리하는 객체
커서 연결하고, SQL 언어를 execute 내부에 넣는다
import sqlite3

conn = sqlite3.connect('myquotes.db')
curr = conn.cursor()

# curr.execute("""create table quotes_tb(
#              title text,
#              author text,
#              tag text
#             )""")

curr.execute("""insert into quotes_tb values ('a', 'b', 'c')""")


conn.commit()
conn.close()

이런식으로. 마지막 커밋은 저장, 클로즈는 닫기

이제 SQLite에 저장하기 위해서
database.py와 디비는 삭제하고, pipline을 수정한다

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class QuotetutorialPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("myquotes.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes""")
        self.curr.execute("""create table quotes_tb(
                title text,
                author text,
                tag text
                )""")



    def process_item(self, item, spider):
        self.store_db(item)
        # print("Pipeline : " + item['title'][0])
        return item
    
    def store_db(self, item):
        self.curr.execute("""insert into quotes_tb values (?, ?, ?)""",(
            item['title'][0],
            item['author'][0],
            item['tag'][0]
        ))
        self.conn.commit()


sqlite3언어에 맞춰서 클래스 내부에다가 데베 생성, 연결, 테이블 생성등의 역할을 하고, 받아온 item을 사용해서 넘겨주는 역할이다
실제로 잘 작동하는데, 문제는 tag같은 경우에는 여러개가 있기 때문에 이를 전부 저장하려면 태그 데이터베이스 테이블을 새로 만들고 여기에 저장하는 방식으로 설정해야한다


다음은 MySQL 데이터베이스 저장하는 방식이다.

mysql 맥에서 왜 안 돌아가는지 몰라서 일단 패스;;;
가상환경 떄문인가;;;
몽고 디비도 패스

아 됐다! 행복하네
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
그 다음, 이제 타고타고 넘어가는...페이지가 여러 개일 때 2번 페이지 3번페이지 4번페이지...이렇게 넘어가야한다
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

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

맨 아래쪽에 next_page 부터 시작해서, 다음으로 넘어가는 주소를 불어오고, 만약에 다음페이지가 존재한다면
yield 를 해서 response.follow()를 사용한다.
다음으로 넘어간다는 의미인데
어디로? next_page로, 찾으면 다시 재귀적으로 parse함수를 실행하라는 의미이다.


만약에 multiple 페이지라면....? 1, 2, 3, 4, 5...1000 중에서 선택하는 그런 상태라면?
즉, 페이지가 1칸씩 올라가는 게 아니라면이라는 의미이다.
&page=5 막 이런식으로...


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


page_number 변수 생성되고, 직접적으로 주소로 접근하는 방식으로 변경되었다.

        


        

ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
이미 무엇을 가져올 지 확실히 알고 있는 것을 가져오는 것은 스크래피를 할 수 있다.

우리가 필요한 것은 링크 (메인페이지) 첫페이지에 있는 html, 최상위 링크가 무엇인지 두 개를 수집을 해야함.


보편적으로 링크를 수집할 수 있는 .... 그런 게 필요하다.

리다이렉트 태그들이나 속성들이 있을텐데
링크들이 생기면 링크들을 큐에 쌓아가지고 크롤러는 큐에서 링크를 하나 받아와가지고, 추가적으로 검색을 하고...
찾으면 다시 큐에다가 쌓고...하는 과정의 반복이 필요하다.



request 에서 html 코드 가져오고, 슬라이스로 싹다 짤라버려서 단어들을 뽑아오고

['도박', '경마'] 이런식으로 이 단어들이 포함되는가? 
하면 일단은 도박 사이트다! 이렇게 나눠갈 수 있을 것 같다.


1. 링크 기반으로 링크가 하나 들어왔을 때, 링크를 넘어가고 넘어가고 큐에 넣기
2. 키워드 뽑아내고
3. 키워드를 토대로 무슨무슨 단어가 포함되어있으면 무슨 사이트다! 라고 분류
4. 어떤 사이트는 되게 많이 참조가 될 것이고, 어떤 사이트는 참조가 거의 되지 않을 것이다.
악성 사이트여도 가장 많이 참조되는 것이 있을 것이고, 아닌 사이트도 있을 것인데, 그것들을 모아보면은 어떤 링크가 중요한 링크고(그들에게)
어떤 링크가 그들에게 중요하지 않은 링크도 나올 수 있을 것이니까, 
#딕셔너리로 링크 : 개수 이런식으로 하면 되지 않을까?
-> 각 urls 들의 중요도 체크

pageRank - 이걸로 중요도






