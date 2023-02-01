from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions

import os
import pandas as pd
import time
from itertools import repeat
import csv
import json
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

options = Options()
options.add_argument("headless")
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
options.add_argument('--disable-blink-features=AutomationControlled')

delay = 20

url = "https://www.costco.co.kr/c/SpecialPriceOffers?itm_source=homepage&itm_medium=blueNav&itm_campaign=SpecialPriceOffers&itm_term=SpecialPriceOffers&itm_content=InternalCATSpecialPriceOffers"
url2= "https://www.costco.co.kr/c/SpecialPriceOffers?itm_source=homepage&itm_medium=blueNav&itm_campaign=SpecialPriceOffers&itm_term=SpecialPriceOffers&itm_content=InternalCATSpecialPriceOffers&page=1"
url3 = url + "&page=2"

print("작업을 시작했습니다.")
i = 1
urls = [url, url2, url3]
for i, url in enumerate(urls):
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.get(url)
    print("접송을 시작했습니다.")
    time.sleep(5)
    browser.maximize_window()
    time.sleep(5)
    print("화면을 최대화 했습니다.")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = browser.page_source

    # items = browser.find_elements(By.TAG_NAME, 'li')

    # res = requests.get(url3, headers=headers)
    # res.raise_for_status()
    soup = BeautifulSoup(html, "lxml")

    items = soup.find_all('li', {'class':'product-list-item product-list-item--grid vline ng-star-inserted'})
    # for item in items:
    #     print(item.get_text())

    sort_item_list = []

    for item in items:
        price = item.find("span", attrs={"class":"product-price-amount"}).get_text()
        disc_price = item.find("div", attrs={"class":"discount-row-message ng-star-inserted"}).get_text()
        name = item.find("a", attrs={"class":"lister-name js-lister-name"}).get_text()
        period = item.find("span", attrs={"class": "discount-date"}).get_text()
        img_url = item.find('img').attrs['src']
        full_img_url = 'https://www.costco.co.kr'+img_url
        print(i)
        print(name)
        print(price)
        print(disc_price)
        print(period)
        print('https://www.costco.co.kr'+img_url)
        i += 1
        print('-------------------end-------------------')
        item_dict = {}
        item_dict["market"] = "costco"
        item_dict["itemName"] = name
        item_dict["image"] = img_url
        item_dict["period"] = period
        item_dict["price"] = price
        item_dict["disc_price"] = disc_price
        try:
            with open(f'C:/Users/s1/Documents/Dev/crawl/cvs_data/img/{name}_img.jpg', 'wb') as handle:
                response = requests.get(full_img_url, stream=True)
                if not response.ok:
                    print(response)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
        except FileNotFoundError:
            print("error")
            pass

        sort_item_list.append(item_dict)

    df = pd.DataFrame(sort_item_list)
    f_name = 'costco_items.csv'
    if os.path.exists(f_name):
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else:
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    browser.implicitly_wait(5)
    browser.quit()

print("상품 정리 완료")
#
