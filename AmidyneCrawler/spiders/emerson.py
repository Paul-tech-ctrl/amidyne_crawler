import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time, json

class EmersonSpider(CrawlSpider):
    name = "emerson"
    allowed_domains = ["www.emerson.com"]
    start_urls = [
        "https://www.emerson.com/en-us/catalog/valves-actuators-regulators",
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="product_name"]/a')), callback="parse_item", follow=False),
    )

    def __init__(self, *args, **kwargs):
        super(EmersonSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def __del__(self):
        self.driver.quit()

    def parse_start_url(self, response):
        self.driver.get(response.url)
        while True:
            selenium_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
            self.parse_page(selenium_response)
            try:
                accpt_btn = self.driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
                if accpt_btn:
                    accpt_btn.click()
                next_page = self.driver.find_element(By.XPATH, '//a[@title="Show next page"]')
                if next_page:
                    pass
                    # next_page.click()
                time.sleep(3)  # wait for the page to load
            except Exception as e:
                print(e)
                break

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.select('div.product_name a'):
            yield scrapy.Request(url=link['href'], callback=self.parse_item)

    def parse_item(self, response):
        self.driver.get(response.url)
        selenium_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        soup = BeautifulSoup(selenium_response.text, "html.parser")
        item = {}
        item["title"] = soup.select_one("h1").get_text(strip=True)
        images_tag = soup.select(".cm-teaser.cm-teaser--picture.cm-teaser--plain div img")
        images = []
        for img_item in images_tag:
            _json = json.loads(img_item.get('data-cm-responsive-media'))
            images.append(_json[-1]['linksForWidth']['400'])
        item["images"] = images
        item["description"] = soup.select_one('[itemprop="description"]').get_text(strip=True)
        specs_tag = soup.select('.specifications.section div dl')
        specs = {}
        for specs_item in specs_tag:
            key = specs_item.select_one('dt').get_text(strip=True)
            _val = specs_item.select_one('dd').get_text(strip=True)
            specs[key] = _val
        item["specifications"] = specs
        feature_tags = soup.select_one('.features.section div div').find('ul')
        feature_list_tags = feature_tags.select('li')
        feature = []
        for fet_item in feature_list_tags:
            feature.append(fet_item.get_text(strip=True))
        item["features"] = feature
        yield item
        return item