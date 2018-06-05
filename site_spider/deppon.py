# !/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapy import Selector
from selenium import webdriver
import csv

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=chrome_options)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('lang=zh_CN.UTF-8')
chrome_options.add_argument(
    'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

csv_file = open("deppon_list.csv", "w", newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow([u'城市', u'网点', u'编号', u'地址', u'电话', u'业务'])

url = 'https://www.deppon.com/deptlist/#'

capabilities = webdriver.DesiredCapabilities().INTERNETEXPLORER
capabilities['acceptSslCerts'] = True

browser = webdriver.Chrome(chrome_options=chrome_options)

browser.get(url)
selector = Selector(text=browser.page_source)

city_list = selector.xpath('//dd[@class="ddTop"]/div/a')
for city in city_list:
    city_url_2 = urljoin(url, city.xpath("./@href").extract_first())
    city_name = city.xpath("./text()").extract_first()
    while city_url_2:
        html = urlopen(city_url_2)
        bs_obj = BeautifulSoup(html.read(), "html.parser")

        site_list = bs_obj.find_all('tr')
        # 表格里的每一行
        for site in site_list[1:]:
            # 每一列    
            site_tds = site.find_all('td')
            site_name = site_tds[0].text
            site_no = site.find("input")['value']
            site_readable_name = site_tds[0].text
            site_address = site_tds[2].text
            site_phone = site_tds[3].text
            site_business = site_tds[4].text.replace("\t", "").replace("\r\n", "").split("、")
            writer.writerow([city_name, site_name, site_no, site_address, site_phone, site_business])
            print("%s %s %s %s %s %s" % (city_name, site_name, site_no, site_address, site_phone, site_business))
        short_url = bs_obj.find("a", text="下一页")
        if short_url:
            city_url_2 = urljoin(url, short_url['href'])
        else:
            city_url_2 = None

csv_file.close()
