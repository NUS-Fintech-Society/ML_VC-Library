from helium import *
import selenium as selenium
from datetime import datetime
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

class CrunchBaseScrapper_v2:
    driver = None
    name_header = 'company_name'
    url_header = 'company_url'

    def __init__(self, headless=False):
        self.options = selenium.webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.headless = headless

    @staticmethod
    def create_empty_header_file(filepath):
        df = pd.DataFrame({ CrunchBaseScrapper_v2.name_header: [], CrunchBaseScrapper_v2.url_header: [] })
        df.to_csv(filepath, index=False)

    def _go_company_ranking(self, ranking):
        if not self.driver:
            raise Exception("Driver not initialised")
        go_to(f"https://www.crunchbase.com/search/organization.companies/field/organizations/rank_org_company/{ranking}")
        time.sleep(3)
        if Text("Please verify you are a human").exists():
            element = self.driver.find_element_by_id('px-captcha').find_element_by_tag_name("iframe")
            ActionChains(self.driver).click_and_hold(element).perform()
            time.sleep(5)
            ActionChains(self.driver).release(element).perform()
            time.sleep(3)

    

    def _check_driver(self):
        if not self.driver:
            raise Exception("Driver not initialised")
