import scrapy, re
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CranefsSpider(CrawlSpider):
    name = "cranefs"
    allowed_domains = ["www.cranefs.com"]
    start_urls = ["https://www.cranefs.com/?s=valve"]

    rules = (
        Rule(LinkExtractor(allow=r"https://www.cranefs.com/product/"), callback="parse_item", follow=True),
        # Rule(LinkExtractor(restrict_xpaths=('//a[@class="next page-numbers"]')), follow=True),
        )

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        item = {}
        item['Product url'] = response.url
        item["title"] = ' '.join(soup.select_one(".product__title-wrapper").stripped_strings)
        # item["introduction"] = soup.select_one(".product__introduction").get_text(strip=True)
        # item["content"] = ', '.join(soup.select_one(".product__content").stripped_strings)
        product_details = soup.select_one(".product__details").get_text().strip()
        stripped_prod_details = re.split(r'\n+', product_details)
        item['Product details'] = stripped_prod_details
        specs = soup.select(".product__specification")
        item["specifications"] = {
            _itm.select_one("label").get_text(): _itm.select_one("div").get_text().replace("\n", " ")
            for _itm in specs
        }
        download_links = soup.select(".product__downloads-list li a")
        item["download_links"] = [link.get('href') for link in download_links]
        images = soup.select(".product__image-thumbnails a img")
        item["images"] = [img_link.get('src') for img_link in images]
        # yield item
        return item
