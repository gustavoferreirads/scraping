# import boto3
import scrapy
# from scrapy.crawler import CrawlerProcess


class TopMoviesSpider(scrapy.Spider):
    name = "imdb_top_movies"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/"]

    def parse(self, response):
        top_rated_movies = response.css('.titleColumn')
        for movie in top_rated_movies:
            yield {
                'title': movie.css('.titleColumn a::text').get(),
                'year': movie.css('.secondaryInfo ::text').get()[1: -1],
                'rate': response.css('strong::text').get(),
            }
        pass
