"""
Created on Sat Jan 27 22:10:15 2024

@author: User
"""

import requests
from bs4 import BeautifulSoup
import csv
import re
import time

HOST = 'https://simplewine.ru/'
URL = 'https://simplewine.ru/catalog/vino/filter/country-yuzhnaya_afrika/'
HEADERS = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

class SimpleWineParser:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.host = 'https://simplewine.ru/'

    def get_html(self, url, params=''):
        r = requests.get(url, headers=self.headers, params=params)
        return r

    def get_content(self, html):
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all('article', class_='snippet swiper-slide')
        wines = []
    
        for item in items:
            description_items = item.find_all('div', class_='snippet-description__item')

            keys_list = [description_item.get_text(strip=True).split(':')[0] for description_item in description_items]
            values_list = [description_item.find('a').get_text(strip=True) if description_item.find('a') else description_item.find('span').get_text(strip=True) for description_item in description_items]

            description_data = dict(zip(keys_list, values_list))

            title = item.find('div', class_='snippet-middle').find('a', class_='snippet-name js-dy-slot-click').get_text(strip=True)
            link_product = item.find('div', class_='snippet-middle').find('a').get('href')

            ratings_span = item.find('span', class_='snippet-star__value')
            ratings = ratings_span.get_text(strip=True) if ratings_span else None

            votes_span = item.find('span', class_='snippet-star__reviews')
            number_votes = ''.join(filter(str.isdigit, votes_span.get_text(strip=True))) if votes_span else None

            price_div = item.find('div', class_='snippet-price__total')
            common_price = item.find('span', class_='snippet-price__total snippet-price__total-black')
