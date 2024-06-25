import scrapy


class AllocineSpider(scrapy.Spider):
    name = "allocine"
    allowed_domains = ["allocine.fr"]
    start_urls = ["https://allocine.fr/film/meilleurs/"]

    def parse(self, response):
        pass
