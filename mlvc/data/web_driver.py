from helium import *
import selenium as selenium
from selenium.webdriver import ChromeOptions, FirefoxOptions
import logging

class WebDriver:
    # initializes and returns web driver 
    @staticmethod
    def start(headless=False, driver_type='Chrome'):
        if driver_type == 'Chrome':
            options = selenium.webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            driver = start_chrome(headless=headless, options=options)

        elif driver_type == 'Firefox':
            options = selenium.webdriver.FirefoxOptions()
            options.add_argument('--start-maximized')
            driver = start_firefox(headless=headless, options=options)

        return driver