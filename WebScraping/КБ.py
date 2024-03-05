"""
Created on Fri Jan 26 19:35:18 2024

@author: User
"""

import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WineScraper:
    BASE_URL = "https://krasnoeibeloe.ru"

    def __init__(self):
        self.driver = webdriver.Chrome()

    def close_driver(self):
        self.driver.quit()

    def handle_age_popup(self):
        try:
            age_popup_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn_red age_popup_btn age_popup_btn--agree']"))
            )
            age_popup_button.click()
        except Exception as e:
            print(f"Error clicking 'Да': {e}")
