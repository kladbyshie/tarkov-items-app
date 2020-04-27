from selenium import webdriver
import time
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup
import os

#This version is MUCH faster as it uses Selenium only to infinite scroll, and uses BS4 to parse
def marketscrape():
    #these options were added so that Heroku could run selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    url  = 'https://tarkov-market.com/'
    driver.get(url)

    #This section is the infinite scroller; scrolls to the bottom of the page, compares to the "last height", waits, and gets the new "bottom of the page". Keeps going until the bottom of the page is the same as the "last height"
    #SCROLL_PAUSE_TIME is how long the scroller waits to load the info before scrolling further. It is possible to cut down the time to half a second (or even less), but occassionally the while loop will break too early because the page loads too slow. If the scraper consistently doesn't download all the info, need to increase the scroll pause time next time.
    SCROLL_PAUSE_TIME = 4
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    #Yoinks the html code from the full page, uses BS4 to parse the text and select the name and prices. 
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    items=pd.DataFrame()
    for name, price in zip(soup.select('.name'), soup.select('.price-main')):
        new = {'Name': name.get_text(), 'Price (in Roubles)': price.get_text()[:-1]}
        items = items.append(new, ignore_index=True)

    #sources current date and saves the data as a file named the current date (MM-DD-YYYY format)
    today = date.today()
    items.to_csv(f'{today}.csv', encoding='utf-8', index=False)

    driver.close()