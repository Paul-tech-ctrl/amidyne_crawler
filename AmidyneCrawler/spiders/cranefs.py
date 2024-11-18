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
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="next page-numbers"]')), follow=True),
        )

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        item = {}
        
        # extract product url
        item['Product url'] = response.url
        
        # extract product title
        item["title"] = ' '.join(soup.select_one("h1").stripped_strings)
        
        # extract product subtitle
        item["subtitle"] = soup.select_one(".product__title").get_text(strip=True)
        
        # extract product details
        product_details = soup.select_one(".product__details").get_text().strip()
        stripped_prod_details = re.split(r'\n+', product_details)
        item['Product details'] = stripped_prod_details
        
        # extract product description
        specs = soup.select(".product__specification")
        item["specifications"] = {
            _itm.select_one("label").get_text(): _itm.select_one("div").get_text().replace("\n", " ")
            for _itm in specs
        }
        
        # extract product downloads
        download_links_tag = soup.find_all('a', attrs={'data-download-type': True})
        dl_dict = {}
        for dl_item in download_links_tag:
            dl_dict[dl_item.get_text(strip=True)] = dl_item.get('href')
        item["download_links"] = dl_dict
        
        # extract product images
        images = soup.select(".product__image-thumbnails a img")
        item["images"] = [img_link.get('src') for img_link in images]
        # yield item
        return item
