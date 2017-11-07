import scrapy
import time
import datetime


class bookrags(scrapy.Spider):

    """
    This spider scrapes bookrags.com
    to run this script you will have to go to it's directory and from the
    terminal run "scrapy runspider bookrags.py -o file_name.json"
    to save the data into a json file in the current directory
    """

    name = 'bookrags'
    start_urls = ['http://www.bookrags.com/browse/studyguides/0-9/#gsc.tab=0']

    def parse(self, response):
        for quote in response.css('tr.oddRow'):
            items = {
                 'Title': quote.css('div.browseResultInfo > h2 > a::text').extract_first(),
                 'Author': quote.css('div.browseResultInfo > h3 > a::text').extract_first(),
                 'Source': response.urljoin(''),
                  }
            yield items

        items = items
        for quote in response.css('tr.evenRow'):
            items =  {
                 'Title': quote.css('div.browseResultInfo > h2 > a::text').extract_first(),
                 'Author': quote.css('div.browseResultInfo > h3 > a::text').extract_first(),
                 'Source': response.urljoin(''),
                  }
            yield items

        next_page_url = response.css('a[id=browseNextLink]::attr(href)').extract_first()
        # Check and see if theres a next page or not
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
