from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sreality.spiders.sreality_spider import SrealitySpider
 
def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(SrealitySpider)
    process.start()

if __name__ == '__main__':
    run()