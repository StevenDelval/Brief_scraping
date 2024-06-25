# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviescraperItem(scrapy.Item):
    titre = scrapy.Field()
    titre_original = scrapy.Field()
    score = scrapy.Field()
    genre = scrapy.Field()
    date = scrapy.Field()
    duree = scrapy.Field()
    descriptions = scrapy.Field()
    acteurs = scrapy.Field()
    realisateur = scrapy.Field()
    public = scrapy.Field()
    pays = scrapy.Field()
    url = scrapy.Field()
    langue = scrapy.Field()
