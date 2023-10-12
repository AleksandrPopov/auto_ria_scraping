import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)


def get_page_html(url: str, sleep: int) -> str:
    driver.get(url)
    time.sleep(sleep)
    button = driver.find_element(By.CLASS_NAME, 'phones_item')
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    button.click()
    time.sleep(sleep)
    return driver.page_source


