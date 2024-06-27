# Brief_Scrapping

```
scrapy startproject moviescraper
```
```
scrapy genspider allocine allocine.fr
```
```
cd moviescraper/ 
scrapy crawl allocine
scrapy crawl allocine -O myscrapeddata.csv
```