import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import MoviescraperItem

class AllocineSpider(CrawlSpider):
    name = "allocine"
    allowed_domains = ["allocine.fr"]
    start_urls = [f"https://www.allocine.fr/film/meilleurs/?page={page}" for page in range(1, 4)]
    

    link_allo_details = LinkExtractor(restrict_xpaths="//h2/a")
    
    rule_allo_details= Rule(link_allo_details, callback='parse_item', follow=False)
    
    rules = (
        rule_allo_details,
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url)

    def parse_item(self, response):
        item = MoviescraperItem()
        item["titre"] = ''.join(response.xpath("//div[@class='titlebar-title titlebar-title-xl']/text()").extract())
        item["titre_original"] = ""
        item["score"] = ""
        item["genre"] = ""
        item["date"] = ""
        item["duree"] = ""
        item["descriptions"] = ""
        item["acteurs"] = ""
        item["realisateur"] = ""
        item["public"] = ""
        item["pays"] = ""
        item["url_image"] = ""
        item["langue"] = ""
        
        yield item
