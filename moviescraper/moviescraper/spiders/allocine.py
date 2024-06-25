import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import MoviescraperItem

class AllocineSpider(CrawlSpider):
    name = "allocine"
    allowed_domains = ["allocine.fr"]
    start_urls = [f"https://www.allocine.fr/film/meilleurs/?page={page}" for page in range(1, 2)]
    

    link_allo_details = LinkExtractor(restrict_xpaths="//h2/a")
    
    rule_allo_details= Rule(link_allo_details, callback='parse_item', follow=True)
    
    rules = (
        rule_allo_details,
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url)

    def parse_item(self, response):
        item = MoviescraperItem()
        print("ok")
