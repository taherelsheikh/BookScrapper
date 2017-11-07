
import scrapy
import time
import datetime



class litcharts(scrapy.Spider):

    """
    This spider scrapes litcharts.com
    to run this script you will have to go to it's directory and from the
    terminal run "scrapy runspider litcharts.py -o file_name.json"
    to save the data into a json file in the current directory
    """

    name = 'litcharts'
    start_urls = ['http://www.litcharts.com/']


    def parse(self, response):
        for quote in response.css('div.content'):
            items = {
                 'Title': quote.css('div.title::text').extract_first(),
                 'Author' : quote.css('div.author::text').extract_first(),
                 'Source' : response.urljoin(''),
                 'Timestamp' : datetime.datetime.now(),
                  }
            yield items
