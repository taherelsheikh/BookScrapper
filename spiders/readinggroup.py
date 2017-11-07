# -*- coding: utf-8 -*-
import scrapy
import datetime

class readinggroup(scrapy.Spider):
		name = 'reading_group'

    # first method calls index page and delivers initial response
		def start_requests(self):
				url = 'http://www.readinggroupguides.com/reviews/index'
				yield scrapy.Request(url=url, callback=self.get_urls)

    # second method looks at response and gets all urls
		def get_urls(self, response):
		  urls = response.xpath('//span[@class="views-summary views-summary-unformatted"]/a/@href').extract()
		  alphabet = [response.urljoin(url) for url in urls]
		  for url in alphabet:
		    yield scrapy.Request(url=url, callback=self.parse)

    # receives responses from get_urls method and parses HTML
		def parse(self, response):
				for book in response.xpath('//div[@class="book-info"]'):
					title = book.xpath('span[@class="title"]/a[@href]/text()').extract_first() # every book has one title, return str
					author = book.xpath('span[@class="author"]/a[@href]/text()').extract() # book could have multiple authors, returns list
					delim = ', '
					yield {
						'Title': title,
						'Author': delim.join(author),
						'Source': response.urljoin(''),
					}

        # check bottom of each page for pagination links
				next_page = response.xpath('//li[@class="pager-next"]/a/@href').extract_first()
				if next_page is not None:
					next_page = response.urljoin(next_page)
					yield scrapy.Request(next_page, callback=self.parse)
