import sys
from scrapy.crawler import CrawlerProcess
from SIEX.catalogo import CatalogoSpider

scraper = sys.argv[1].lower() if len(sys.argv) > 1 else ""
browser = sys.argv[2].lower() if len(sys.argv) > 2 else "firefox"
crawlerDict = {
    "catalogo": CatalogoSpider
}
help = """
- Métodos de uso -
Lanzar _scraper_ con el navegador por defecto (Firefox)
python3 main.py <scraper>

Lanzar _scraper_ con el _navegador_ indicado
python3 main.py <scraper> <navegador>

- Scrapers disponibles -"""

if __name__ == "__main__":
    if scraper not in crawlerDict:
        for crawler in crawlerDict:
            help += '\n'+crawler
        print(help)
        exit(0)

    process = CrawlerProcess()
    process.crawl(crawlerDict.get(scraper), browser=browser)
    process.start()
