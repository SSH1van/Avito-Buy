from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random
import time
from wait import get_code


def is_button_clicked_with_refresh(temp_button):
    try:
        WebDriverWait(driver, 1).until(EC.invisibility_of_element(temp_button))
        return True
    except:
        return False

def is_button_clicked_without_refresh(temp_button):
    try:
        div_element = temp_button.find_element(By.TAG_NAME, "div")       
        div_class = div_element.get_attribute("class")    
        if "active" in div_class:
            return True 
        else:
            return False 
    except Exception:
        return False


driver_path = './chromedriver-win64/chromedriver.exe'
service = Service(driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--disable-webrtc")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(service=service, options=options)

try:
    url = 'https://www.avito.ru/moskva/noutbuki/igrovoy_noutbuk_thunderobot_i5_i7_rtx_4050_4060_3897056856'
    driver.get(url)

    # Время для входа в личный кабинет
    time.sleep(60)
    price = int(driver.find_element(By.CSS_SELECTOR, 'span[data-marker="item-view/item-price"]').text.replace("₽", "").replace(" ", ""))
    
    button = None
    # Кнопка Купить с доставкой
    while not button:
        try:
            button = driver.find_element(By.CSS_SELECTOR, 'button[data-marker="delivery-item-button-main"]')
        except Exception: 
            button = None
            driver.refresh()
            time.sleep(random.uniform(0.5, 5))

    if price < 60000:
        button.click()

        # Кнопка Оплатить
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-marker="sd/order-widget-payment-button"]'))
        )
        while True:
            try:
                button.click()
                if is_button_clicked_with_refresh(button):
                    break
            except Exception: None

        # Выбор способа оплаты
        li = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-index="1"]'))
        )
        while True:
            try:
                li.click()
                if is_button_clicked_without_refresh(li):
                    break
            except Exception: None


        # Кнока Оплатить СУММА
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-marker="payButton"]'))
        )
        while True:
            try:
                button.click()
                if is_button_clicked_with_refresh(button):
                    break
            except Exception: None
                

        # Вставка кода в passwordEdit
        code = get_code()
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "passwordEdit"))
        )
        while True:
            try:
                password_input.send_keys(code)
                break
            except Exception:
                password_input = driver.find_element(By.ID, "passwordEdit")
finally:
    driver.quit()