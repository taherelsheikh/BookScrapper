import scrapy
from selenium import webdriver
import datetime
import time
import re
import json
import getpass
import os

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

fpath = find('bookbrowse_credentials.json', '/Users')
jstr = open(fpath)
data = json.load(jstr)

user = data['user']
password = data['password']

def getNumberPages(text_str):
    last_page = re.findall('[0-9].*', text_str)
    last_page_number = last_page[1].split()[-1]
    return last_page_number

class bookbrowse(scrapy.Spider):
    name = 'BookBrowse'
    allowed_domains = ['https://www.bookbrowse.com']

    start_urls = ['https://www.bookbrowse.com/']

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self,response):
            self.driver.get('https://www.bookbrowse.com/login/')
            # time.sleep(5)
            # self.driver.find_element_by_xpath('//div[@id="promopop-container"]/a[@class="close"]').click()
            self.driver.find_element_by_xpath('//input[@id="member_email"]').send_keys(user)
            self.driver.find_element_by_xpath('//input[@id="member_password"]').send_keys(password)
            self.driver.find_element_by_xpath('//input[@id="remember"]').click()
            self.driver.find_element_by_xpath('//input[@name="I1"]').click()

            pages = []

            self.driver.find_element_by_xpath('//li[@class="submenu"]/a[@href="https://www.bookbrowse.com/category/"]').click()
            totals = self.driver.find_element_by_xpath('//div[@class="brownblock tight"]')
            last_page_number = getNumberPages(totals.text)
            pages.append(last_page_number)

            self.driver.find_element_by_xpath('//li/a[@href="https://www.bookbrowse.com/category/index.cfm/tc/2"]').click()
            totals_nonfict = self.driver.find_element_by_xpath('//div[@class="brownblock tight"]')
            last_page_number_nonfict = getNumberPages(totals_nonfict.text)
            pages.append(last_page_number_nonfict)

            self.driver.find_element_by_xpath('//li/a[@href="https://www.bookbrowse.com/category/index.cfm/tc/3"]').click()
            totals_ya = self.driver.find_element_by_xpath('//div[@class="brownblock tight"]')
            last_page_number_ya = getNumberPages(totals_ya.text)
            pages.append(last_page_number_ya)

            urls = []
            for page_number in pages:
                for i in range(1, int(page_number) + 1):
                    url = ''
                    url = response.urljoin('') + 'category/index.cfm/tc/' + str(pages.index(page_number) + 1) + '/g/0/t/0/tp/0/s/0/o/v/v/books/page/' + str(i)
                    urls.append(url)

            for url in urls:
            	self.driver.get(url)
            	books = self.driver.find_elements_by_xpath('//div[@class="books"]/ul/li/div[@class="desc"]')

            	for book in books:
            		title = book.find_element_by_xpath('a[@class="textleft"]').text
            		author = book.find_element_by_xpath('i').text
            		yield{
                        'Title': title,
                        'Author': author,
                        'Source': url,
                        }

            self.driver.close()