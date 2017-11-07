import scrapy
import time
import datetime



class shmoop(scrapy.Spider):

    """
    This spider scrapes Shmoop.com
    to run this script you will have to go to it's directory and from the
    terminal run "scrapy runspider shmoop.py -o file_name.json"
    to save the data into a json file in the current directory
    """

    name = 'shmoop'
    def start_requests(self):
        urls = [
            'https://www.shmoop.com/literature/study-guides/sort-title.html',
            'https://www.shmoop.com/bestsellers/'
        ]

        for url in urls:
            if url == 'https://www.shmoop.com/bestsellers/':
                yield scrapy.Request(url=url, callback=self.bestseller)
            elif url == 'https://www.shmoop.com/literature/study-guides/sort-title.html':
                yield scrapy.Request(url=url, callback=self.literature)



    def bestseller(self, response):
        books = response.css('div.nameBio')
        authors = response.css('div.birthBio')

        for book, author in zip(books, authors):
            items = {
                 'Title': book.css('a::text').extract_first(),
                 'Author' : author.css('::text').extract_first(),
                 'Source' : response.urljoin(''),
                  }
            yield items

    def literature(self, response):
        books = response.css('div.nameBio')
        authors = response.css('div.birthBio')

        for book, author in zip(books, authors):
            items = {
                 'Title': book.css('a::text').extract_first(),
                 'Author': author.css('::text').extract_first(),
                 'Source' : response.urljoin(''),
                  }
            yield items
