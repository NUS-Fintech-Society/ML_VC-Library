from helium import *
import selenium as selenium
from datetime import datetime
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import logging

class CrunchBaseScrapper_v2:
    driver = None
    name_header = 'company_name'
    url_header = 'company_url'

    def __init__(self, headless=False):
        self.options = selenium.webdriver.FirefoxOptions()
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
            element = self.driver.find_element_by_id('px-captcha')
            ActionChains(self.driver).click_and_hold(element).perform()
            time.sleep(5)
            ActionChains(self.driver).release(element).perform()
            time.sleep(3)

    def fetch_data(self, start=100001, end=300000, step=15, backup_filepath=None):
        all_names = []
        all_links = []
        for i in range(start, end, step):
            print(f"{start} to {end}. Currently at : {i}")
            if not self.driver:
                self.driver = start_firefox(headless=self.headless, options=self.options)
            elif (((step - start) / 15) % 400 == 0):
                self.driver.close()
                time.sleep(3)
                self.driver = start_firefox(headless=self.headless, options=self.options)
            
            self._go_company_ranking(i)
            time.sleep(2)
            
            name_list = [cell.web_element.text for cell in find_all(
                S("div > grid-row > grid-cell > div > field-formatter > identifier-formatter > a",
                  below="Organization Name"))]
            
            link_list = [cell.web_element.get_attribute("href") for cell in find_all(
                S("div > grid-row > grid-cell > div > field-formatter > identifier-formatter > a",
                  below="Organization Name"))]

            if backup_filepath:
                df = pd.DataFrame({ self.name_header: name_list, self.url_header: link_list })
                df.to_csv(backup_filepath, mode='a', header=False, index=False)
            
            all_names.append(name_list)
            all_links.append(link_list)

        return pd.DataFrame({ self.name_header: all_names, self.url_header: all_links })

    def _check_driver(self):
        if not self.driver:
            raise Exception("Driver not initialised")
