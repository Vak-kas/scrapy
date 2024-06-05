import pytesseract
import re
import scrapy
from io import BytesIO
from PIL import Image
from scrapy.http import Request
from urllib.parse import urljoin
from collections import deque, Counter
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
from get_words.items import GetWordsItem

class GetwordsSpider(scrapy.Spider):
    name = "getwords"
    custom_settings = {
        'ITEM_PIPELINES': {
            'get_words.pipelines.SQLitePipeline': 300,
        }
    }

    def __init__(self, *args, **kwargs):
        super(GetwordsSpider, self).__init__(*args, **kwargs)
        self.divide_file = open('divide.txt', 'w', encoding='utf-8')
        self.image_file = open('image.txt', 'w', encoding='utf-8')
        self.hosts_queue = deque(open('hosts.txt', 'r', encoding='utf-8').read().strip().split("\n"))

        pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
        os.environ['TESSDATA_PREFIX'] = '/opt/homebrew/opt/tesseract/share/tessdata/'

    def start_requests(self):
        if self.hosts_queue:
            current_url = self.hosts_queue.popleft()
            yield scrapy.Request(url=current_url, callback=self.parse, errback=self.errback, dont_filter=True, meta={'original_url': current_url})

    def parse(self, response):
        original_url = response.meta.get('original_url')
        redirected_url = response.url

        texts = self.extract_with_scrapy(response)
        total_words = set(texts)

        if len(total_words) < 10:
            texts.extend(self.extract_with_selenium(response))

        image_texts = list(self.extract_in_image(response, original_url))
        for future in image_texts:
            res = yield future
            if res and 'gettext' in res.meta:
                texts.extend(res.meta['gettext'])

        count_words = self.extract_words_count(texts)

        for word, count in count_words.items():
            item = GetWordsItem()
            item['host'] = original_url
            item['redirect'] = redirected_url if redirected_url != original_url else None
            item['words'] = word
            item['count'] = count
            yield item

        if self.hosts_queue:
            next_url = self.hosts_queue.popleft()
            yield scrapy.Request(url=next_url, callback=self.parse, errback=self.errback, dont_filter=True, meta={'original_url': next_url})

    def extract_with_selenium(self, response):
        try:
            url = response.url
            options = Options()
            options.add_argument("headless")
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            all_tags = driver.find_elements(By.XPATH, '//*[@content]')
            contents = [tag.get_attribute("content") for tag in all_tags]
            contents_words = []
            for content in contents:
                content_word = re.findall(r'[\uAC00-\uD7A3]+', content)
                contents_words.extend(content_word)

            body_element = driver.find_element(By.TAG_NAME, 'body')
            body_text = body_element.text
            body_words = re.findall(r'\b\w+\b', body_text)
            combined_list = body_words + contents_words

            return combined_list

        except Exception as e:
            return []

        finally:
            driver.quit()

    def extract_with_scrapy(self, response):
        cleaned_html = re.sub(r'<(script|style).*?>.*?</\1>', '', response.text, flags=re.DOTALL)
        selector = Selector(text=cleaned_html)
        texts = selector.css('body *::text').getall()
        cleaned_texts = [word for text in texts for word in self.clean_text(text)]
        return cleaned_texts

    def clean_text(self, text):
        words = re.findall(r'\b\w+\b', text)
        return words

    def extract_in_image(self, response, original_url):
        self.image_file.write(f"{original_url}\n")
        img_urls = response.css('img::attr(src)').extract()
        for img_url in img_urls:
            if not img_url.startswith(('http', 'https')):
                img_url = urljoin(response.url, img_url)
            yield Request(img_url, callback=self.parse_image, meta={'img_url': img_url, 'current_url': original_url})

    def parse_image(self, response):
        img_url = response.meta['img_url']
        current_url = response.meta['current_url']

        try:
            img = Image.open(BytesIO(response.body))
            if img.format not in ['JPEG', 'PNG', 'GIF']:
                return

            min_image_width = 50
            min_image_height = 50
            width, height = img.size

            if width > min_image_width and height > min_image_height:
                text = pytesseract.image_to_string(img, lang='kor+eng')
                gettext = self.process_text(text)
                if gettext:
                    self.image_file.write(f"{img_url} : {', '.join(gettext)}\n")
                    current_texts = getattr(response.meta, 'gettext', [])
                    current_texts.extend(gettext)
                    response.meta['gettext'] = current_texts
                    return Request(url=current_url, callback=self.continue_parse, meta=response.meta, dont_filter=True)
        except Exception as e:
            return

    def continue_parse(self, response):
        original_url = response.meta['current_url']
        redirected_url = response.url

        texts = response.meta.get('gettext', [])
        count_words = self.extract_words_count(texts)

        for word, count in count_words.items():
            item = GetWordsItem()
            item['host'] = original_url
            item['redirect'] = redirected_url if redirected_url != original_url else None
            item['words'] = word
            item['count'] = count
            yield item

    def process_text(self, text):
        text = re.sub(r'\b[ㄱ-ㅎㅏ-ㅣ]\b', '', text)
        text = re.sub('[0-9]', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text)
        word_list = text.strip().split()
        cleaned_word_list = [re.sub(r'[ㄱ-ㅎㅏ-ㅣ]', '', word) for word in word_list]
        filtered = [word for word in cleaned_word_list if len(word) > 1]
        return filtered

    def extract_words_count(self, words):
        return dict(Counter(words))

    def errback(self, failure):
        if self.hosts_queue:
            next_url = self.hosts_queue.popleft()
            yield scrapy.Request(url=next_url, callback=self.parse, errback=self.errback, dont_filter=True, meta={'original_url': next_url})

    def closed(self, reason):
        self.divide_file.close()
        self.image_file.close()
