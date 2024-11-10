from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time

driver_path = './chromedriver-win64/chromedriver.exe'
service = Service(driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

try:
    url = 'https://www.avito.ru/moskva/noutbuki/igrovoy_noutbuk_thunderobot_i5_i7_rtx_4050_4060_3897056856'
    driver.get(url)

    # Время для входа в личный кабинет
    time.sleep(60)

    while True:
        button = False
        price = int(driver.find_element(By.CSS_SELECTOR, 'span[data-marker="item-view/item-price"]').text.replace("₽", "").replace(" ", ""))
        try:
            button = driver.find_element(By.CSS_SELECTOR, 'button[data-marker="delivery-item-button-main"]')
        except: None

        if (button and price < 60000):
            button.click()
        time.sleep(5)
finally:
    driver.quit()