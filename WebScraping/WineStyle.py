"""
Created on Mon Jan 29 17:04:35 2024

@author: User
"""

import requests
from bs4 import BeautifulSoup
import csv
import re
import time

def get_content(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('form', class_='item-block')
    wines = []

    for item in items:

        title = item.find('p', class_='title').find('a').get_text(strip=True)

        price = item.find('div', class_='price').get_text(strip=True)
        price_digits = re.sub(r'\D', '', price)
              
        rating_div = item.find('div', class_='info-block rating-text')
        ratings = rating_div.find('span', class_='text').get_text(strip=True) if rating_div else None
        
        number_votes = rating_div.find('span', class_='link-reviews').get_text(strip=True) if rating_div else None
        
        desc_items = item.find('ul', class_='list-description').find_all('li')
        def extract_text_from_elements(elements):
            return ', '.join(element.get_text(strip=True) for element in elements)
        
        keys_list = [desc_item.find('span', class_='name').get_text(strip=True) for desc_item in desc_items]
        values_list = [extract_text_from_elements(desc_item.find_all('a')) for desc_item in desc_items]
        description_data = dict(zip(keys_list, values_list))   
        
        link_product = item.find('p', class_='title').find('a').get('href')
        
        image = item.find('a', class_='img-block').find('img').get('src')
        
        volume_element = item.find('span', class_='volume-block__title')
        volume_text = volume_element.next_sibling.string.strip()

        # Combine all extracted data into a single dictionary
        wine_data = {
            'Title': title,
            'Link_product': link_product,
            'Ratings': ratings,
            'Number_votes': number_votes,
            'Image': image,
            'Price': price_digits,
            'Объем' : volume_text
 
        }

        # Add the description data to the wine_data dictionary
        wine_data.update(description_data)

        wines.append(wine_data)

    return wines

