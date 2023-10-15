import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class AutoRiaWebDriver:
    """ This is a class for working with a web driver """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """ Create a new instance if it does not exist, otherwise, return the existing one """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, time_to_sleep) -> None:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.time_to_sleep = time_to_sleep
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_html(self, url: str) -> str:
        """ This method pushes the button to display the phone number and returns the HTML code """
        self.driver.get(url)
        time.sleep(self.time_to_sleep)
        button = self.driver.find_element(By.CLASS_NAME, 'phones_item')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        time.sleep(self.time_to_sleep)
        return self.driver.page_source
