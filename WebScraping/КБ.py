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

    def get_content(self):
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        items = soup.find_all('div', class_='catalog_product_item_cont')
        wines = []

        for item in items:
            link_product_element = item.find('div', itemprop='name')
            link_product = link_product_element.find('a').get('href') if link_product_element else None
            full_link_product = self.BASE_URL + link_product if link_product else None

            image = item.find('div', class_='product_item_images').find('img').get('src')

            price_element = item.find('div', class_='product_item__price_c')
            price = price_element.find('div', itemprop='price').get_text(strip=True) if price_element else None

            rating_div = item.find('div', class_='rate_votes')
            number_votes = rating_div.get_text(strip=True) if rating_div else None

            wine_data = {
                'Link_product': full_link_product,
                'Number_votes': number_votes,
                'Image': image,
                'Price': price
            }

            wines.append(wine_data)

        return wines

    def get_product_details(self, link):
        self.driver.get(link)
        time.sleep(3)  # Adding a sleep time before opening the product link
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        product_chars = soup.find_all('div', class_='pr_card_char_item')
        details = {}

        for char in product_chars:
            char_name = char.find('span').get_text(strip=True)
            char_value = char.find('p').get_text(strip=True)
            details[char_name] = char_value

        return details

