import scrapy
import time
import datetime


class sparknotes(scrapy.Spider):

    """
    This spider scrapes sparknotes.com
    to run this script you will have to go to it's directory and from the
    terminal run "scrapy runspider sparknotes.py -o file_name.json"
    to save the data into a json file in the current directory
    """

    name = 'sparknotes'
    letters = ['a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm','n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y']
    start_urls = ['http://www.sparknotes.com/lit/index_%s.html' % page for page in letters]


    def parse(self, response):
        for quote in response.css('p.clearfix'):
            if not quote.css('p.clearfix a.right-link::text').extract_first():
                items = {
                'Title': quote.css('p.clearfix span.left::text').extract_first(),
                'Author' : quote.css('p.clearfix a span.right.text-color::text').extract_first(),
                'Source' : response.urljoin(''),
                }
            else:
                items = {
                 'Title': quote.css('p.clearfix span.left::text').extract_first(),
                 'Author' : quote.css('p.clearfix a.right-link::text').extract_first(),
                 'Source' : response.urljoin(''),
                  }
            yield items
