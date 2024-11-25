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
    time.sleep(2)

    # Время для входа в личный кабинет
    WebDriverWait(driver, 120).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, '[data-marker="header/login-button"]'))
    )

    button = None
    # Кнопка Купить с доставкой
    while not button:
        try:
            button = driver.find_element(By.CSS_SELECTOR, 'button[data-marker="delivery-item-button-main"]')
            price_element = driver.find_element(By.CSS_SELECTOR, "span[itemprop='price']")
            price_content = price_element .get_attribute("content")
            price = int(price_content)
        except Exception: 
            button = None
            driver.refresh()
            time.sleep(random.uniform(0.5, 2))
            driver.execute_script("window.stop();")

    if price < 55000:
        button.click()
        time.sleep(1)
        driver.execute_script("window.stop();")

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


        #Кнока Оплатить СУММА
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-marker="payButton"]'))
        )
        while True:
            try:
                button.click()
                if is_button_clicked_with_refresh(button):
                    break
            except Exception: None
                
        code = get_code()
        driver.execute_script("window.stop();")
        #Вставка кода
        
        # # СБЕР
        # password_input = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "passwordEdit"))
        # )
        # while True:
        #     try:
        #         password_input.send_keys(code)
        #         break
        #     except Exception:
        #         password_input = driver.find_element(By.ID, "passwordEdit")

        # ВТБ
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "psw_id"))
        )
        password_input.send_keys(code)
        password_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnSubmit"))
        )
        password_button.click() 
finally:
    time.sleep(120)
    driver.quit()