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

def save_to_csv(data, filename='WineStyle'):
    if not data:
        print("No data to save.")
        return

    # Extract the header from the first dictionary in the list
    header = list(data[0].keys())

    # Write the data to the CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()

        for row in data:
            # Filter out keys that are not present in the header
            filtered_row = {key: row[key] for key in header if key in row}
            writer.writerow(filtered_row)

def parser():
    base_url = 'https://winestyle.ru/wine/south-africa/'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Upgrade-Insecure-Requests': '1',
    }

    session = requests.Session()
    session.headers.update(headers)

    wines_data = []
    count = 0
    for page in range(1, 23):  
        url = f'{base_url}?page={page}'
        response = session.get(url)

        if response.status_code == 200:
            wines_data.extend(get_content(response))
            count += 1
            if count % 2 == 0:
                time.sleep(30)
            else:
                time.sleep(60)

        else:
            print(f'Error on page {page}. Status code: {response.status_code}')

    save_to_csv(wines_data, 'WineStyle.csv')
        
parser()
