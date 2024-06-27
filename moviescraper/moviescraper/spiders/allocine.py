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
        # if next_page:
        #     yield scrapy.Request(next_page[0].url, self.parse_start_url, meta={"playwright": True})        

    def parse_item(self, response):
        item = MoviescraperItem()
        item["titre"] = ''.join(response.xpath("//div[@class='titlebar-title titlebar-title-xl']/text()").extract())
        item["titre_original"] = ''.join(response.xpath("//div[@class='meta-body-item']/span[contains(text(), 'Titre original')]/following-sibling::span[1]/text()").extract())
        item["score"] = ''.join(response.xpath().extract())
        item["genre"] = ''.join(response.xpath().extract())
        item["date"] = ''.join(response.xpath("//a[@class='xXx date blue-link']/text()").extract())
        item["duree"] = ''.join(response.xpath("//span[@class='spacer'][1]/following-sibling::text()[1]").extract())
        item["descriptions"] = ''.join(response.xpath().extract())
        item["acteurs"] = ''.join(response.xpath().extract())
        item["realisateur"] = ''.join(response.xpath().extract())
        item["public"] = ''.join(response.xpath("//div[@class='certificate']/span[@class='certificate-text']/text()").extract())
        item["pays"] = ''.join(response.xpath("//a[@class='xXx nationality']/text()").extract())
        item["url_image"] = ''.join(response.xpath().extract())
        item["langue"] = ''.join(response.xpath("//div[@class='item']/span[contains(text(), 'Langues')]/following-sibling::span[1]/text()").extract())
        
        yield item
