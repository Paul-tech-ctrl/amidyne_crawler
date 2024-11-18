import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import your spider here
from AmidyneCrawler.spiders.emerson import EmersonSpider
from AmidyneCrawler.spiders.cranefs import CranefsSpider

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(EmersonSpider)
    process.start()

if __name__ == "__main__":
    run_spider()