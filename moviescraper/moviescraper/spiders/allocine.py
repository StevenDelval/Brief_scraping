import os
from dotenv import load_dotenv
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import MoviescraperItem

class AllocinespiderSpider(CrawlSpider):
    name = 'allocine'
    allowed_domains = ["allocine.fr"]
    start_urls = ["https://www.allocine.fr/film/meilleurs"]
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h2/a"), callback='parse_item', follow=False, process_request='use_playwright'),
        Rule(LinkExtractor(restrict_xpaths="//span[@class='txt' and text()='Suivante']/.."), follow=True, process_request='use_playwright'),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})

    def use_playwright(self, request, response):
        request.meta.update({"playwright": True})
        return request

    def parse_item(self, response):
        item = MoviescraperItem()
        item["titre"] = ''.join(response.xpath("//div[@class='titlebar-title titlebar-title-xl']/text()").extract())
        item["titre_original"] = ''.join(response.xpath("//div[@class='meta-body-item']/span[contains(text(), 'Titre original')]/following-sibling::span[1]/text()").extract())
        item["score"] = ''.join(response.xpath("//div[@class='rating-item']/div/a[contains(text(), ' Spectateurs ')]/../div/span[@class='stareval-note']/text()").extract())
        item["genre"] = ', '.join(response.xpath("//span[@class='spacer'][2]/following-sibling::a/text()").extract())
        item["date"] = ''.join(response.xpath("//a[@class='xXx date blue-link']/text()").extract())
        if item["date"] == "":
            item["date"] = ''.join(response.xpath("//span[@class='date']/text()").extract())
        item["duree"] = ''.join(response.xpath("//span[@class='spacer'][1]/following-sibling::text()[1]").extract())
        item["descriptions"] = ''.join(response.xpath("//p[@class='bo-p']/text()").extract())
        item["acteurs"] = ', '.join(response.xpath("//div/span[contains(text(), 'Avec')]/../a/text()").extract())
        item["realisateur"] = ''.join(response.xpath("//div/span[contains(text(), 'De')]/../a/text()").extract())
        item["public"] = ''.join(response.xpath("//div[@class='certificate']/span[@class='certificate-text']/text()").extract())
        item["pays"] = ''.join(response.xpath("//a[@class='xXx nationality']/text()").extract())
        item["url_image"] = ''.join(response.xpath("//div[@class='card entity-card entity-card-list cf entity-card-player-ovw']/figure/a/img/@src").extract())
        item["langue"] = ''.join(response.xpath("//div[@class='item']/span[contains(text(), 'Langues')]/following-sibling::span[1]/text()").extract())
        
        yield item
