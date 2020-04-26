from selenium import webdriver
import time
from datetime import date
import pandas as pd

#This version is must slower, as it uses Selenium to both infinite scroll and parse
driver = webdriver.Chrome()
url  = 'https://tarkov-market.com/'
driver.get(url)

#This section is the infinite scroller; scrolls to the bottom of the page, compares to the "last height", waits, and gets the new "bottom of the page". Keeps going until the bottom of the page is the same as the "last height"
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

#This uses Selenium CSS selectors to find the name and price, creates an empty dataframe, and appends name-price pairs to the dataframe. This is slower than BS4.
name = driver.find_elements_by_css_selector('.name')
price = driver.find_elements_by_css_selector('.price-main')
data = {'name': [],
       'price': []}
items = pd.DataFrame(data)
for item, price in zip(name, price):
    new = {'name':item.text,'price':price.text[:-1]}
    items = items.append(new, ignore_index=True)

#sources current date and saves the data as a file named the current date (MM-DD-YYYY format)
today = date.today()
items.to_csv(f'{today}.csv', encoding='utf-8', index=False)

driver.close()