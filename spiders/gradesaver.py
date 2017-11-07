import scrapy
import datetime
import re
import json

class gradesaver(scrapy.Spider):
    name = 'gradesaver'

    # first method calls index page and delivers initial response
    def start_requests(self):
        url = 'http://www.gradesaver.com/study-guides/newest'
        yield scrapy.Request(url=url, callback=self.get_urls)

    # second method looks at response and generates all urls
    def get_urls(self, response):
        x = response.xpath('//a[@class="pagination__forward"]/@href').extract_first()
        last = re.search('[0-9].*', x)
        num = last.group()

        urls = []
        for i in range(1, int(num) + 1):
            url = ''
            url = response.urljoin('') + '?page=' + str(i)
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for book in response.xpath('//h3[@class="excerpt__title"]'):
            title = book.xpath('a/span[@itemprop="name"]/text()').extract_first()
            author = book.xpath('span[@itemprop="author"]/a/text()').extract_first()
            yield {
        	   'Title': title,
        	   'Author': author,
        	   'Source': response.urljoin(''),
            }
