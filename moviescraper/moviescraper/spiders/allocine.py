import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import MoviescraperItem

class AllocineSpider(CrawlSpider):
    name = "allocine"
    allowed_domains = ["allocine.fr","localhost"]
    start_urls = ["https://www.allocine.fr/film/meilleurs/"]

    # Define link extractors for movie details and next page
    link_allo_details = LinkExtractor(restrict_xpaths="//h2/a")
    link_next_page = LinkExtractor(restrict_xpaths="//span[@class='txt' and text()='Suivante']/..")

    
    # Define rules for the spider
    rules = (
        Rule(link_next_page,callback="parse_start_url"),  # Follow next page links
        # Rule(link_allo_details, callback='parse_item', follow=False),  # Extract movie details
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})
    
    
    def parse_start_url(self, response):
        # Follow movie detail links
        links = self.link_allo_details.extract_links(response)
        next_page = self.link_next_page.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, self.parse_item, meta={"playwright": True})

        # Follow next page link
        if next_page:
            yield scrapy.Request(next_page[0].url, self.parse_start_url, meta={"playwright": True})        

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
