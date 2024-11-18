import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BraySpider(CrawlSpider):
    name = "bray"
    allowed_domains = ["www.bray.com"]
    start_urls = ["https://www.bray.com/solutions/industry/power/power-products?page=1"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="details-btn product-cta"]')), callback="parse_item", follow=False),
        )

    def parse_item(self, response):
        item = {}
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        return item
