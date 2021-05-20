from helium import *
import selenium as selenium
from datetime import datetime
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

class CrunchBaseScrapper_v2:
    driver = None

    def __init__(self, headless=False):
        self.options = selenium.webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.headless = headless

    def _go_company_ranking(self, ranking):
        if not self.driver:
            raise Exception("Driver not initialised")
        go_to(f"https://www.crunchbase.com/search/organization.companies/field/organizations/rank_org_company/{ranking}")
        time.sleep(2)
        if Text("Please verify you are a human").exists():
            element = self.driver.find_element_by_id('px-captcha').find_element_by_tag_name("iframe")
            ActionChains(self.driver).click_and_hold(element).perform()
            time.sleep(5)
            ActionChains(self.driver).release(element).perform()
            time.sleep(3)

    def fetch_data(self, start=100001, end=300000, step=15):
        all_names = []
        all_links = []
        for i in range(start, end, step):
            if not self.driver:
                self.driver = start_chrome(headless=self.headless, options=self.options)
            self._go_company_ranking(i)
            name_list = [cell.web_element.text for cell in find_all(
                S("div > grid-row > grid-cell > div > field-formatter > identifier-formatter > a",
                  below="Organization Name"))]
            link_list = [cell.web_element.get_attribute("href") for cell in find_all(
                S("div > grid-row > grid-cell > div > field-formatter > identifier-formatter > a",
                  below="Organization Name"))]
            for name in name_list:
                all_names.append(name)
            for link in link_list:
                all_links.append(link)
            #kill_browser()
        df = pd.DataFrame({'Company Name': all_names,
                           'URL': all_links})
        return df

    def _check_driver(self):
        if not self.driver:
            raise Exception("Driver not initialised")
