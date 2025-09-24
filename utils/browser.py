import os
from pathlib import Path
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# load variables from .env
load_dotenv()

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = os.environ.get('CHROMEDRIVER_NAME', 'chromedriver')
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / 'win64' / CHROMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    # pass --headless as options to not see the chrome screen
    browser = make_chrome_browser()
    browser.get('http://www.udemy.com/')
    sleep(5)
    browser.quit()
