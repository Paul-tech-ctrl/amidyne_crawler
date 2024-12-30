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
        
        item['Product url'] = response.url
        item["title"] = ' '.join(soup.select_one("h1").stripped_strings)
        item["subtitle"] = soup.select_one(".product__title").get_text(strip=True)
        item["Product deatails"] = self.get_product_details(soup, item)
        item["images"] = self.get_images(soup, item)
        item["Specifications"] = self.get_specifications(soup, item)
        item["Downloads"] = self.get_download_links(soup, item)
        
        # yield item
        return item

    def get_product_details(self, soup, item):
        try:
            data = []
            product_details = soup.select_one(".product__details").get_text().strip()
            stripped_prod_details = re.split(r'\n+', product_details)
            for idx, detail in enumerate(stripped_prod_details):
                data.append(detail)
                # item[f"Product detail {str(idx + 1)}"] = detail
            return data
        except Exception as e:
            return None
        
    def get_specifications(self, soup, item):
        try:
            data = {}
            specs = soup.select(".product__specification")
            for spec_item in specs:
                specs_val = ''
                val = spec_item.select_one("div").get_text().split("\n")
                if len(val) >= 2:
                    specs_val = ' \n'.join(val)
                else:
                    specs_val = val[0]
                data[spec_item.select_one("label").get_text()] = specs_val
                # item[spec_item.select_one("label").get_text()] = spec_item.select_one("div").get_text().replace("\n", " ")
            return data
        except Exception as e:
            return None
        
    def get_download_links(self, soup, item):
        try:
            data = {}
            download_links_tag = soup.find_all('a', attrs={'data-download-type': True})
            for idx, dl_item in enumerate(download_links_tag):
                data[dl_item.get_text(strip=True)] = dl_item.get('href')
                # item[f"Dowload {str(idx + 1)}"] = {"title": dl_item.get_text(strip=True), "link": dl_item.get('href')}
            return data
        except Exception as e:
            return None
        
    def get_images(self, soup, item):
        try:
            data = []
            images = soup.select(".product__image-thumbnails a img") or soup.select(".product__image-main img")
            for idx, img_link in enumerate(images):
                data.append(img_link.get('src'))
                # item[f"Image {str(idx + 1)}"] = img_link.get('src')
            return data
        except Exception as e:
            return None