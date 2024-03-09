"""
Created on Thu Feb  1 21:15:22 2024

@author: User
"""


import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

HOST = 'https://amwine.ru/'
URL = 'https://amwine.ru/catalog/vino/filter/country-is-yuzhnaya-afrika/'

