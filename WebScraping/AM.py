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

  
