import scrapy


class enotes(scrapy.Spider):

    """
    This spider scrapes e-notes.com
    to run this script you will have to go to it's directory and from the
    terminal run "scrapy runspider enotes.py -o file_name.json"
    to save the data into a json file in the current directory
    """

    name = 'enotes'


    def start_requests(self):
        url = 'https://www.enotes.com/topics/alpha/'
        yield scrapy.Request(url=url, callback=self.get_urls)


    def get_urls(self, response):
        letters = ['a', 'b', 'c', 'd', 'e', 'f',
        'g', 'h', 'i', 'j', 'k', 'l', 'm','n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y','z']
        next_page_url = ['https://www.enotes.com/topics/alpha/%s' % page for page in letters]

        for pages in next_page_url:
            yield scrapy.Request(url=pages, callback=self.get_pages)


    def get_pages(self, response):
        pages = len(response.css(" li.pagination-list__item > a::text").extract()) - 2
        for i in range(2, pages):
            i = str(i)
            next_page_url = response.url + "?pg=" + i
            yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parse(self, response):
        authors = response.xpath("//div[contains(@class, 'resetContent')] / ol / li/text()")
        length = len(authors) - 1
        authorz =  []

        for i in range(length):
            if i % 2 == 0:
                authorz.append(authors.extract()[i])

        for author, quote in zip(authorz, response.xpath('//div[contains(@class, "resetContent")]//li')):
            items = {
            'Title': quote.css('a > span::text').extract_first(),
            'Author': author,
            'Source': response.urljoin(''),
            }

            yield items
