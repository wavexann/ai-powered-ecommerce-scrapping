from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import logging

chrome_options = Options()
#chrome.options.add_argument('--headless')

service = Service(executable_path=r"C:\Users\anjali\Downloads\chromedriver_win32\chromedriver.exe")
driver = webdriver.Chrome(service=service , options = chrome_options)

wait = WebDriverWait(driver, 10)

product = []

current_page = 1
max_pages = 5

Base_url = 'https://www.ebay.com/e/row/luxurysneakersrow?rt=nc&_pgn='

while current_page <= max_pages:
	print(f'scraping pages {current_page}.... ')
	driver.get(Base_url + str(current_page))

	try:
		element = wait.until(
			EC.visibility_of_element_located((By.CSS_SELECTOR ,'.s-item__info'))
			)
		items = driver.find_elements(By.CSS_SELECTOR, '.s-item__info')

		for item in items:
			name = item.find_element(By.CSS_SELECTOR, 'h3.s-item__title').text.strip()
			price = item.find_element(By.CSS_SELECTOR, 'span.s-item__price').text.strip()
			rating_elements = item.find_elements(By.CSS_SELECTOR, 'div.star-rating.b-rating__rating-star[role="img"]')
			rating = (
				rating_elements[0].get_attribute('aria-label') if rating_elements else 'N/A'
				)
			product.append({
				"name": name,
				"Price": price,
				"Rating": rating
				})
	except Exception as e:
		print(f'Failed to scrape page {current_page}: {e}')

	current_page += 1
	time.sleep(4)



df = pd.DataFrame(product)
df.to_csv('scraper.csv', index = False)

print("scraping complete.")
driver.quit()
		
		
		
	

		





