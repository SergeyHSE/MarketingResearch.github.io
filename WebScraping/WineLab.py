"""
Created on Fri Feb  2 20:04:54 2024

@author: User
"""

import json
import csv

# Specify the paths to your JavaScript files
path_page1 = r"C:\Users\User\Documents\pyton-projects\spider\Машинное обучение\WebScraping\file.js"
path_page2 = r"C:\Users\User\Documents\pyton-projects\spider\Машинное обучение\WebScraping\Page2WineLab.js"

# Read the content of the JavaScript files and load them as JSON arrays
parsed_data_page1 = []
parsed_data_page2 = []

# Read and parse data from page 1
with open(path_page1, 'r', encoding='utf-8') as file_page1:
    try:
        parsed_data_page1 = json.loads(file_page1.read())
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from page 1: {e}")

# Read and parse data from page 2
with open(path_page2, 'r', encoding='utf-8') as file_page2:
    try:
        parsed_data_page2 = json.loads(file_page2.read())
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from page 2: {e}")

  
# Combine data from both pages
combined_data = parsed_data_page1 + parsed_data_page2

# Specify the path to save the combined CSV file
csv_path_combined = r"C:\Users\User\WineLab_data.csv"

# Open the CSV file in write mode and write the header
with open(csv_path_combined, 'w', newline='', encoding='utf-8') as csvfile_combined:
    fieldnames = ['code', 'name', 'price', 'rating', 'num_reviews', 'image_url', 'full_product_url', 'alcohol_content']
    writer_combined = csv.writer(csvfile_combined)
    writer_combined.writerow(fieldnames)

