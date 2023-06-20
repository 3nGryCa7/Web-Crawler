import scrapy


class MorningstarSpider(scrapy.Spider):
    name = "morningstar"
    allowed_domains = ["www.morningstar.com"]
    start_urls = ["https://www.morningstar.com/"]

    def parse(self, response):
        pass
