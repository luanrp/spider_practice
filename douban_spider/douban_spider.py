#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('lang=zh_CN.UTF-8')
chrome_options.add_argument(
    'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

url = 'https://book.douban.com/people/16656074'

capabilities = webdriver.DesiredCapabilities().INTERNETEXPLORER
capabilities['acceptSslCerts'] = True

browser = webdriver.Chrome(chrome_options=chrome_options)

csv_file = open("book_list.csv", "w", newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow([u'书名', u'评级', u'时间', u'封面'])

browser.get(url)

next_page = browser.find_elements_by_css_selector("#db-book-mine div span.pl a")[1]

while next_page:
    next_page.click()
    sel = Selector(text=browser.page_source)
    books = sel.xpath('//li[@class="subject-item"]')

    for book in books:
        title = book.xpath('.//h2/a/@title').extract_first()
        try:
            rating = book.xpath('.//span/@class').extract_first()
        except:
            rating = ''
        cover_img = book.xpath(".//img/@src").extract_first()
        read_date = book.xpath('.//span[@class="date"]/text()').extract_first().split(" 读过")[0].strip()

        writer.writerow([title, rating, read_date, cover_img])
        print("%s %s %s %s" % (title, rating, read_date, cover_img))
    next_pages = browser.find_element_by_xpath('//span[@class="next"]').find_elements_by_tag_name("a")
    if len(next_pages) > 0:
        next_page = next_pages[0]
    else:
        next_page = None

csv_file.close()
