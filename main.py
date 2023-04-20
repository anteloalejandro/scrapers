import sys
from scrapy.crawler import CrawlerProcess
from SIEX.catalogo import CatalogoSpider

scraper = sys.argv[1] if len(sys.argv) > 1 else ""
crawlerDict = {
    "catalogo": CatalogoSpider
}
help = """
- Método de uso -
python3 main.py {scraper}

- Scrapers disponibles -"""

if __name__ == "__main__":
    if scraper not in crawlerDict:
        for crawler in crawlerDict:
            help += '\n'+crawler
        print(help)
        exit(0)

    process = CrawlerProcess()
    process.crawl(crawlerDict.get(scraper))
    process.start()
