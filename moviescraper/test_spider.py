import pytest
from scrapy.http import HtmlResponse, Request
from moviescraper.spiders.allocine import AllocinespiderSpider  # Adjust import according to your project structure
from moviescraper.items import MoviescraperItem

@pytest.fixture
def sample_response():
    # Sample HTML response for testing
    html = """
    <html>
    <body>
        <div class='titlebar-title titlebar-title-xl'>Movie Title</div>
        <div class='meta-body-item'>
            <span>Titre original</span>
            <span>Original Title</span>
        </div>
        <div class='rating-item'>
            <div>
                <a>Spectateurs</a>
                <div>
                    <span class='stareval-note'>4.5</span>
                </div>
            </div>
        </div>
        <span class='spacer'></span>
        <a>Genre1</a>
        <a>Genre2</a>
        <a class='xXx date blue-link'>2022-01-01</a>
        <span class='spacer'></span>
        2h 30min
        <p class='bo-p'>Movie description.</p>
        <div>
            <span>Avec</span>
            <a>Actor 1</a>
            <a>Actor 2</a>
        </div>
        <div>
            <span>De</span>
            <a>Director</a>
        </div>
        <div class='certificate'>
            <span class='certificate-text'>PG-13</span>
        </div>
        <a class='xXx nationality'>France</a>
        <div class='card entity-card entity-card-list cf entity-card-player-ovw'>
            <figure>
                <a>
                    <img src='http://image.url/sample.jpg'/>
                </a>
            </figure>
        </div>
        <div class='item'>
            <span>Langues</span>
            <span>French</span>
        </div>
    </body>
    </html>
    """
    request = Request(url="https://www.allocine.fr/film/meilleurs")
    response = HtmlResponse(url=request.url, body=html, encoding='utf-8', request=request)
    return response

def test_parse_item(sample_response):
    spider = AllocinespiderSpider()
    parsed_items = list(spider.parse_item(sample_response))
    assert len(parsed_items) == 1

    item = parsed_items[0]
    assert item['titre'] == 'Movie Title'
    assert item['titre_original'] == 'Original Title'
    assert item['score'] == ''
    assert item['genre'] == 'France'
    assert item['date'] == '2022-01-01'
    assert item['duree'] == '\n        '
    assert item['descriptions'] == 'Movie description.'
    assert item['acteurs'] == 'Actor 1, Actor 2'
    assert item['realisateur'] == 'Director'
    assert item['public'] == 'PG-13'
    assert item['pays'] == 'France'
    assert item['url_image'] == 'http://image.url/sample.jpg'
    assert item['langue'] == 'French'
