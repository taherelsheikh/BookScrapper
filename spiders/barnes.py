import scrapy
import datetime
import time

class barnes(scrapy.Spider):

    """
    This spider scrapes barnesandnoble.com
    to run this script you will have to go to it's directory and from
    the terminal run "scrapy runspider barnes.py -o file_name.json"
    to save the data into a json file in the current directory
    """

    name = 'barnes&noble'
    quotes_base_url = 'https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=20&page=%s'
    start_urls = [quotes_base_url % 1]


    def parse(self, response):
        titles = response.css('h3.product-info-title')
        authors = response.css('div.product-shelf-author')
        dates = response.css('h3.product-info-title')
        ranks = response.css('div.col-lg-1.count')

        for title, author, date, rank in zip(titles, authors, dates, ranks):
            items = {
                 'Rank': rank.css('::text').extract_first(),
                 'Title': title.css('a::text').extract_first(),
                 'Author': author.css('a::text').extract_first(),
                 'Date_published': date.css('span::text').extract_first(),
                 'Source': response.urljoin(''),
                 }
            yield items

        # Scrape only 100 Bestsellers
        for i in range(2, 6):
            yield scrapy.Request(self.quotes_base_url % i)
