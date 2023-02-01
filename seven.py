from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

options = Options()
options.add_argument("headless")
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)

delay = 3

url = "https://www.7-eleven.co.kr/product/presentList.asp"
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

browser.get(url)

# elm_1 = browser.find_element(By.XPATH, '//*[@id="actFrm"]/div[3]/div[1]/ul/li[1]/a')
# elm_1.click()
# print("1+1 상품을 클릭했습니다.")

# elm_2 = browser.find_element(By.XPATH,'//*[@id="actFrm"]/div[3]/div[1]/ul/li[2]/a')
# elm_2.click()
# print("2+1 상품을 클릭했습니다.")

elm_3 = browser.find_element(By.XPATH,'//*[@id="actFrm"]/div[3]/div[1]/ul/li[4]/a')
elm_3.click()
print("할인행사 상품을 클릭했습니다.")

browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

more_btn = browser.find_element(By.LINK_TEXT, 'MORE')
for i in repeat(None, 30):
    try:
        browser.execute_script("arguments[0].click();", more_btn)
        print("더보기 버튼을 클릭했습니다.")
        time.sleep(5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        more_btn = browser.find_element(By.LINK_TEXT, 'MORE')
    except NoSuchElementException:
        print("더보기 버튼이 없습니다.")
        break
    except StaleElementReferenceException:
        print("더보기 버튼이 업습니다.")
        break

sort_item_list = []

li_list = browser.find_elements(By.CLASS_NAME, 'pic_product')
for li in li_list:
   img_url = li.find_element(By.TAG_NAME, 'img').get_attribute('src')
   item_name = li.find_element(By.CLASS_NAME, 'name').text
   item_price = li.find_element(By.CLASS_NAME, 'price').text.strip()
   # event_type = find_element(By.CLASS_NAME, 'ico_tag_06').text
   print(f"이미지 주소: {img_url}")
   print(f"상품명:{item_name}")
   print(f"가격:{item_price}")
   # print(f"행사명:{event_type}")
   print("----------------------")
   item_dict={}
   item_dict["market"]= "seven"
   item_dict["itemName"] = item_name
   item_dict["image"] = img_url
   item_dict["price"] = item_price.strip()
   item_dict["eventName"] = "discount"
   sort_item_list.append(item_dict)

df = pd.DataFrame(sort_item_list)

f_name = 'seven_event_item_3.csv'
if os.path.exists(f_name):
    df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
else:
    df.to_csv(f_name, encoding='utf-8-sig', index=False)
print("상품 정리 완료")

# csvfile = open('event_item.csv', 'r', encoding='utf-8-sig')
# jsonfile = open('event_item.json', 'w', encoding='utf-8-sig')
#
# reader = csv.DictReader( csvfile, fieldnames)
# for row in reader:
#     json.dump(row, jsonfile)
#     jsonfile.write('\n')
# print("json 파일을 만들었습니다.")
browser.quit()