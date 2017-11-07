import scrapy
import time
import datetime


class nytimes(scrapy.Spider):

    """
    This spider scrapes nytimes.com
    to run this script you will have to go to it's directory and from the
    terminal run "scrapy runspider nytimes.py -o file_name.json"
    to save the data into a json file in the current directory
    """

    name = 'nytimes'
    def start_requests(self):
        fiction = 'https://www.nytimes.com/books/best-sellers/combined-print-and-e-book-fiction'
        nonfiction = 'https://www.nytimes.com/books/best-sellers/combined-print-and-e-book-nonfiction'
        children = 'https://www.nytimes.com/books/best-sellers/childrens-middle-grade-hardcover'
        monthly = 'https://www.nytimes.com/books/best-sellers/business-books'
        yield scrapy.Request(fiction, self.fiction)
        yield scrapy.Request(nonfiction, self.nonfiction)
        yield scrapy.Request(children, self.children)
        yield scrapy.Request(monthly, self.monthly)

    def fiction(self, response):
        for quote in response.css('article.book'):
            category = response.css('h1.page-heading::text').extract_first()
            category = ' '.join(category.split())
            author = quote.css('p.author::text').extract_first()
            author = author[3:]
            items = {
                 'Title': quote.css('h2.title ::text').extract_first(),
                 'Author' : author,
                 'Source' : response.urljoin(''),
                 'Category': category,
                  }
            yield items

        next_page = response.css('select#category-select-fiction ::attr(value)').extract()[2:]
        for url in next_page:
            next_page = 'https://www.nytimes.com' + url
            yield scrapy.Request(next_page, callback=self.fiction)

    def nonfiction(self, response):
        for quote in response.css('article.book'):
            category = response.css('h1.page-heading::text').extract_first()
            category = ' '.join(category.split())
            author = quote.css('p.author::text').extract_first()
            author = author[3:]
            items = {
                 'Title': quote.css('h2.title ::text').extract_first(),
                 'Author' : author,
                 'Source' : response.urljoin(''),
                 'Category': category,
                  }
            yield items

        next_page = response.css('select#category-select-nonfiction ::attr(value)').extract()[2:]
        for url in next_page:
            next_page = 'https://www.nytimes.com' + url
            yield scrapy.Request(next_page, callback=self.nonfiction)

    def children(self, response):
        for quote in response.css('article.book'):
            category = response.css('h1.page-heading::text').extract_first()
            category = ' '.join(category.split())
            author = quote.css('p.author::text').extract_first()
            author = author[3:]
            items = {
                 'Title': quote.css('h2.title ::text').extract_first(),
                 'Author' : author,
                 'Source' : response.urljoin(''),
                 'Category': category,
                  }
            yield items

        next_page = response.css('select#category-select-childrens ::attr(value)').extract()[2:]
        for url in next_page:
            next_page = 'https://www.nytimes.com' + url
            yield scrapy.Request(next_page, callback=self.children)

    def monthly(self, response):
        for quote in response.css('article.book'):
            category = response.css('h1.page-heading::text').extract_first()
            category = ' '.join(category.split())
            author = quote.css('p.author::text').extract_first()
            author = author[3:]
            items = {
                 'Title': quote.css('h2.title ::text').extract_first(),
                 'Author' : author,
                 'Source' : response.urljoin(''),
                 'Category': category,
                  }
            yield items

        next_page = response.css('select#category-select-monthly-lists ::attr(value)').extract()[2:]
        for url in next_page:
            next_page = 'https://www.nytimes.com' + url
            yield scrapy.Request(next_page, callback=self.monthly)
