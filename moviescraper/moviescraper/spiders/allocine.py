import scrapy
from scrapy_splash import SplashRequest
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
        Rule(link_next_page, follow=True, process_request='process_splash_request'),  # Follow next page links
        Rule(link_allo_details, callback='parse_item', follow=False),  # Extract movie details
    )

    def process_splash_request(self, request):
        return SplashRequest(
            url=request.url,
            callback=self.parse_start_url,
            args={'wait': 5, 'html': 1}
        )

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_start_url, args={'wait': 5, 'html': 1})


    def parse_start_url(self, response):
        # Follow movie detail links
        links = self.link_allo_details.extract_links(response)
        print(response.xpath("//a[@class='xXx button button-md button-primary-full button-right']"))
        next_page = self.link_next_page.extract_links(response)
        print("un lien : \n\n\n\n",next_page)
        for link in links[0:1]:
            yield SplashRequest(link.url, self.parse_item, args={'wait': 5, 'html': 1})

        # Follow next page link
        if next_page:
            yield SplashRequest(response.urljoin(next_page), self.parse_start_url, args={'wait': 5, 'html': 1})

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
