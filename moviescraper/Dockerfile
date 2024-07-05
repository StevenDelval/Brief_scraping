FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y locales && \
    echo "fr_FR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen fr_FR.UTF-8 && \
    update-locale LANG=fr_FR.UTF-8

# Set the locale environment variables
ENV LANG=fr_FR.UTF-8 \
    LANGUAGE=fr_FR:fr \
    LC_ALL=fr_FR.UTF-8

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install-deps && \
    playwright install

COPY . .

EXPOSE 8000

WORKDIR /app/moviescraper

CMD scrapy crawl allocine 