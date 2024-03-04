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
    
