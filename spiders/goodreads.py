import scrapy
import datetime
import json
import re

# file = open('urls.json')
# urls = json.load(file)

class goodreads(scrapy.Spider):
    name = "awards"

    def start_requests(self):
        url = 'https://www.goodreads.com/award'
        yield scrapy.Request(url=url, callback=self.get_urls)

    def get_urls(self, response):
        urls = []
        for url in response.xpath('//div[@class="left"]/a/@href').extract():
            url = response.urljoin(url)
            urls.append(url)

        next_page = response.css('a.next_page::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.get_urls)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for book in response.xpath('//tr[@itemtype="http://schema.org/Book"]'):
            title = book.xpath('td[@width="100%"]/a[@class="bookTitle"]/span[@itemprop="name"]/text()').extract_first()
            author = book.xpath('td[@width="100%"]/span[@itemprop="author"]//a[@class="authorName"]/span[@itemprop="name"]/text()').extract_first()
            # not all books have awards listed
            try:
                award = book.xpath('td[@width="100%"]/i/text()').extract_first()
                award_year = re.search(r'\(([0-9]*)\)', award)
                if award_year:
                    year = award_year.group(0)
                    year = year.strip('(').rstrip(')')
                    if year == '0':
                        year = ''
                else:
                    year = ''
            except:
                award = ''
                year = ''

            yield{
            'Title': title,
            'Author': author,
            'Award': award,
            'Year': year,
            'Source': response.urljoin(''),
            }

        next_page = response.css('a.next_page::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
