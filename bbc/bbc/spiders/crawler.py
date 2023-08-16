import scrapy
from bs4 import BeautifulSoup

class BBCSpider(scrapy.Spider):
    name = 'bbc'
    start_urls = ['https://www.bbc.com/news']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        titles = soup.find_all('h3', '.gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')
        for title in titles:
            print(title)