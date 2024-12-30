# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AmidynecrawlerPipeline:
    def process_item(self, item, spider):
        return item

from scrapy.exporters import CsvItemExporter
import csv

class CustomCsvItemExporter(CsvItemExporter):
    def __init__(self, file, **kwargs):
        kwargs['delimiter'] = ','
        kwargs['qoutechar'] = '"'
        kwargs['quoting'] = csv.QUOTE_MINIMAL
        super().__init__(file, **kwargs)
        # super(CustomCsvItemExporter, self).__init__(*args, **kwargs)
        
class CsvPipeline:
    def open_spider(self, spider):
        self.file = open('output.csv', 'wb')
        self.exporter = CustomCsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item