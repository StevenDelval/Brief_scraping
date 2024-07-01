FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install-deps && \
    playwright install

EXPOSE 8000

WORKDIR /app/moviescraper

CMD scrapy crawl allocine -O ./data/myscrapeddata.csv