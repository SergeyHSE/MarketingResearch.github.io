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

def handle_age_confirmation(driver):
    try:
        # Wait for the age confirmation popup to appear
        age_confirmation_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'confirmation-popup'))
        )

        if age_confirmation_popup.is_displayed():
            # Age confirmation popup is present, click the confirmation button
            confirmation_button = driver.find_element(By.CSS_SELECTOR, '.confirmation-popup__btn a')
            confirmation_button.click()

            # Wait for the page to reload after confirmation
            time.sleep(3)
    except Exception as e:
        print(f"Error handling age confirmation: {e}")

  def get_additional_info_selenium(product_url, driver):
    additional_info = {}

    # Wait for the dynamic content to load (you may need to adjust the wait time)
    time.sleep(2)

    # Get the HTML after JavaScript has modified the content
    driver.get(product_url)
    product_html = driver.page_source

    product_soup = BeautifulSoup(product_html, 'html.parser')
    about_wine_params = product_soup.find_all('div', class_='about-wine__param')

    for param in about_wine_params:
        title = param.find('span', class_='about-wine__param-title').get_text(strip=True)
        value = param.find('span', class_='about-wine__param-value').get_text(strip=True)
        
        additional_info[title] = value

    return additional_info

def get_content(html, driver):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='catalog-list-item__container')
    wines = []

    for item in items:
        title_element = item.select_one('.catalog-list-item__title.js-product-detail-link')
        title = title_element.get_text(strip=True)

        link_product = item.find('div', class_='catalog-list-item__info').find('a').get('href')
        image = item.find('a', class_='catalog-list-item__image js-product-detail-link').find('img').get('data-src')

        rating_div = item.find('div', class_='product-rating-new')
        ratings = rating_div.find('span', class_='product-rating__rating').get_text(strip=True) if rating_div and rating_div.find('span', class_='product-rating__rating') else None
        number_votes_raw = rating_div.find('a', class_='product-rating__text').get_text(strip=True) if rating_div and rating_div.find('a', class_='product-rating__text') else None

        # Extract numeric values from 'Number_votes'
        number_votes = float(''.join(filter(str.isdigit, number_votes_raw))) if number_votes_raw else None

        # Extract numeric values from 'Price'
        price_raw_element = item.find('span', class_='middle_price')
        price_digits = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_raw_element.get_text(strip=True)))) if price_raw_element else None

        # Get additional information from the product page using Selenium
        additional_info = get_additional_info_selenium(HOST + link_product, driver)

        # Include additional information in wine_data
        wine_data = {
            'Title': title,
            'Link_product': link_product,
            'Number_votes': number_votes,
            'Image': image,
            'Ratings': ratings,
            'Price': price_digits,
            'Additional_Info': additional_info
        }

        wines.append(wine_data)

    return wines

def save_to_csv(data, filename='AM'):
    header = list(data[0].keys())

    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def parser():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    wines_data = []

    dynamic_html = get_dynamic_content_selenium(URL + '?page=1', driver)
    wines_data.extend(get_content(dynamic_html, driver))

    for wine_data in wines_data:
        product_link = wine_data['Link_product']
        additional_info = get_additional_info_selenium(HOST + product_link, driver)
        wine_data['Additional_Info'] = additional_info

        time.sleep(1)

    time.sleep(2)

    if wines_data:
        try:
            save_to_csv(wines_data, 'AM1.csv')
            print('Data saved successfully.')
        except Exception as e:
            print(f"Error during data processing: {e}")
    else:
        print('No data to save.')

parser()


