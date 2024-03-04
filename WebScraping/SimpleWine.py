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
