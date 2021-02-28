# from helium import start_chrome, go_to, click, find_all
# from helium import Text, TextField, ListItem, Button, S, Link
from helium import *
import selenium as selenium
from selenium.webdriver import ChromeOptions
import time

# import pandas as pd
# import numpy as np

icon_mapping = {
    "M12,2C8.1,2,5,5.1,5,9c0,5.2,7,13,7,13s7-7.8,7-13C19,5.1,15.9,2,12,2z M12,11.5c-1.4,0-2.5-1.1-2.5-2.5s1.1-2.5,2.5-2.5s2.5,1.1,2.5,2.5S13.4,11.5,12,11.5z": 'location',
    "M16.36,10.91a3.28,3.28,0,1,0-3.27-3.27A3.26,3.26,0,0,0,16.36,10.91Zm-8.72,0A3.28,3.28,0,1,0,4.36,7.64,3.26,3.26,0,0,0,7.64,10.91Zm0,2.18C5.09,13.09,0,14.37,0,16.91v2.73H15.27V16.91C15.27,14.37,10.18,13.09,7.64,13.09Zm8.72,0a10.24,10.24,0,0,0-1,.06,4.59,4.59,0,0,1,2.14,3.76v2.73H24V16.91C24,14.37,18.91,13.09,16.36,13.09Z": "employee",
    "M12,2C6.5,2,2,6.5,2,12s4.5,10,10,10s10-4.5,10-10S17.5,2,12,2z M11,19.9c-3.9-0.5-7-3.9-7-7.9c0-0.6,0.1-1.2,0.2-1.8L9,15v1c0,1.1,0.9,2,2,2V19.9z M17.9,17.4c-0.3-0.8-1-1.4-1.9-1.4h-1v-3c0-0.6-0.4-1-1-1H8v-2h2c0.6,0,1-0.4,1-1V7h2c1.1,0,2-0.9,2-2V4.6c2.9,1.2,5,4.1,5,7.4C20,14.1,19.2,16,17.9,17.4z": "website",
    "M21.3,0H2.7C1.2,0,0,1.2,0,2.7v18.7C0,22.8,1.2,24,2.7,24h18.7c1.5,0,2.7-1.2,2.7-2.7V2.7C24,1.2,22.8,0,21.3,0z M21.3,21.3H2.7V2.7h18.7V21.3z": "rank",
    "M9,10.71A3.87,3.87,0,1,0,5.15,6.85,3.85,3.85,0,0,0,9,10.71Zm0,2.58c-3,0-9,1.51-9,4.51V21H18V17.8C18,14.8,12,13.29,9,13.29Z": "investor",
    "M8.44679391,9.59786248 L8.44679391,10.7127564 C9.51041577,10.9723892 10.0449539,11.7763782 10.0798625,12.6523663 L8.95515061,12.6523663 C8.92569647,12.016375 8.58861016,11.58329 7.68316796,11.58329 C6.82245242,11.58329 6.30864125,11.9705574 6.30864125,12.5247317 C6.30864125,13.0090887 6.67954528,13.3189027 7.83589315,13.6199895 C8.99115012,13.9199854 10.2282242,14.4141604 10.2282242,15.8595953 C10.2282242,16.903581 9.43950764,17.4784823 8.44679391,17.6661161 L8.44679391,18.7613739 L6.91954201,18.7613739 L6.91954201,17.6573889 C5.94210079,17.4479373 5.10756671,16.821764 5.04647664,15.7068701 L6.16464321,15.7068701 C6.2224606,16.3068619 6.63481862,16.7759464 7.68316796,16.7759464 C8.806789,16.7759464 9.05769467,16.2152268 9.05769467,15.8650497 C9.05769467,15.3916017 8.80351632,14.9432441 7.53044277,14.6377938 C6.1090076,14.2974348 5.13702086,13.7116246 5.13702086,12.5345497 C5.13702086,11.5527449 5.93119185,10.9112991 6.91954201,10.6974839 L6.91954201,9.59786248 L8.44679391,9.59786248 Z M1.5272519,20.2886258 L13.7452671,20.2886258 L13.7452671,8.07061058 L1.5272519,8.07061058 L1.5272519,20.2886258 Z M13.7452671,6.54335868 C14.5863465,6.54335868 15.272519,7.23062204 15.272519,8.07061058 L15.272519,20.2886258 C15.272519,21.1286143 14.5863465,21.8158777 13.7452671,21.8158777 L1.5272519,21.8158777 C0.687263355,21.8158777 -5.68434189e-14,21.1286143 -5.68434189e-14,20.2886258 L-5.68434189e-14,8.07061058 C-5.68434189e-14,7.23062204 0.687263355,6.54335868 1.5272519,6.54335868 L13.7452671,6.54335868 Z M24,13.0889422 L24,15.2707306 L17.4546347,15.2707306 L17.4546347,13.0889422 L24,13.0889422 Z M24,7.63447108 L24,9.81625951 L17.4546347,9.81625951 L17.4546347,7.63447108 L24,7.63447108 Z M24,2.18 L24,4.36178843 L12.0001636,4.36178843 L12.0001636,2.18 L24,2.18 Z": "investment_stage",
    "M12.52,10.53c-3-.78-4-1.6-4-2.86,0-1.46,1.35-2.47,3.6-2.47S15.37,6.33,15.45,8H18.4a5.31,5.31,0,0,0-4.28-5.08V0h-4V2.88c-2.59.56-4.67,2.24-4.67,4.81,0,3.08,2.55,4.62,6.27,5.51,3.33.8,4,2,4,3.21,0,.92-.65,2.39-3.6,2.39-2.75,0-3.83-1.23-4-2.8H5.21c.16,2.92,2.35,4.56,4.91,5.11V24h4V21.13c2.6-.49,4.67-2,4.67-4.73C18.79,12.61,15.55,11.32,12.52,10.53Z": "last_funding",
    "M14.4,6L14,4H5v17h2v-7h5.6l0.4,2h7V6H14.4z": "ipo_status",
}


class CrunchBaseScrapper:
    driver = None

    def __init__(self, headless=False):
        options = selenium.webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self.driver = start_chrome(headless=headless, options=options)

    def go_company_ranking(self, ranking):
        if not self.driver:
            raise Exception("Driver not initialised")
        go_to(
            f"https://www.crunchbase.com/search/organization.companies/field/organizations/rank_org_company/{ranking}")
        if Text("Organization Name").exists():
            click(Link(below="Organization Name"))
            time.sleep(3)

    def scrape_information(self):
        profile_type = self._get_profile_type()
        if profile_type == "ORGANIZATION":
            # Summary
            for icon in icon_list:
                if icon_location == icon:
                    all_locations.append(general_list[0])
                    general_list.pop(0)  # removes the information
                if icon_employees == icon:
                    all_no_employees.append(general_list[0])
                    general_list.pop(0)  # removes the information
                if icon_last_funding == icon:
                    all_last_funding_types.append(general_list[0])
                    general_list.pop(0)  # removes the information
                if icon_ipo_status == icon:
                    all_ipo_status.append(general_list[0])
                    general_list.pop(0)  # removes the information
                if icon_website == icon:
                    # not saving this
                    general_list.pop(0)  # removes the information
                if icon_cbrank == icon:
                    # dont need to save this
                    general_list.pop(0)  # removes the information
        if profile_type[0] == "INVESTMENT FIRM":
            # Icons
            for icon in icon_list:
                if icon_location == icon:
                    all_locations.append(general_list[0])
                    general_list.pop(0)  # removes the information
                if icon_employees == icon:
                    all_no_employees.append(general_list[0])
                    general_list.pop(0)  # removes the information
                if icon_investor == icon:
                    all_company_types.append(general_list[0])
                    general_list.pop(0)  # removes the information
                if icon_investmentstage == icon:
                    all_investment_stages.append(general_list[0])
                    general_list.pop(0)  # removes the information
                if icon_website == icon:
                    # not keeping website!
                    general_list.pop(0)  # removes the information
                if icon_cbrank == icon:
                    # not keeping this
                    general_list.pop(0)  # removes the information


        location = self._get_location()
        print(location)
        general_info = self._get_general_information()
        print(general_info)
        about = self._get_about()
        print(about)
        highlights = self._get_highlights()
        print(highlights)

    def _check_driver(self):
        if not self.driver:
            raise Exception("Driver not initialised")

    def _get_profile_type(self):
        self._check_driver()
        profile_type = [cell.web_element.text for cell in find_all(S(".profile-type"))]
        return profile_type[0] if profile_type else ""

    def _get_location(self):
        self._check_driver()
        location = [cell.web_element.text for cell in find_all(S("fields-card > ul > li > label-with-icon > span"))]
        return location

    def _get_general_information(self):
        self._check_driver()
        obj = {}
        element = S("fields-card > ul > li > label-with-icon")
        items = find_all(element)
        general_list = [(cell.web_element.find_element_by_tag_name('path').get_attribute("d"), cell.web_element.text)
                        for cell in items]
        for key, value in general_list:
            obj[icon_mapping[key]] = value
        return obj

    def _get_about(self):
        self._check_driver()
        if Button("READ MORE").exists():
            click(Button("READ MORE"))
        about = [cell.web_element.text for cell in find_all(S("description-card > div > span"))]
        short_about = about[0]
        long_about = ", ".join(about[1:])
        return short_about, long_about

    def _get_highlights(self):
        self._check_driver()
        obj = {}
        highlight_element = S("profile-section > section-card > mat-card > div > div > anchored-values > div > a > div")
        highlight_list = [cell.web_element.text.split("\n") for cell in find_all(highlight_element)]
        res = list(map(lambda x: (", ".join(x[:-1]).strip(), x[-1]), highlight_list))
        for key, value in res:
            obj[key] = value
        return obj


all_rnklst = []
all_names = []
all_acquired_by = []
all_abouts = []
all_locations = []
all_no_employees = []
all_industries = []
all_ipo_status = []
all_founded_date = []
all_hqs = []
all_founders = []
all_operating_status = []
all_hub_tags = []
all_last_funding_types = []
all_company_types = []
all_investment_stages = []
all_no_investors = []
all_no_funding_rounds = []
all_total_funding_amt = []
all_no_funds = []
all_no_investments = []
all_no_diversity_investments = []
all_no_exits = []
all_stock_symbols = []
all_no_lead_investors = []
all_no_acquisitions = []
all_no_current_team = []
all_no_board_members = []
all_total_products_active = []
all_product_downloads = []
all_active_tech_count = []
all_monthly_visits = []
all_monthly_visit_growth = []
all_no_articles = []
all_no_events = []

big_array = [all_rnklst, all_names, all_acquired_by, all_abouts, all_locations,
             all_no_employees, all_industries, all_ipo_status, all_founded_date,
             all_hqs, all_founders, all_operating_status, all_hub_tags,
             all_last_funding_types, all_company_types, all_investment_stages,
             all_no_investors, all_no_funding_rounds, all_total_funding_amt,
             all_no_funds, all_no_investments, all_no_diversity_investments, all_no_exits,
             all_stock_symbols, all_no_lead_investors, all_no_acquisitions,
             all_no_current_team, all_no_board_members, all_total_products_active,
             all_product_downloads, all_active_tech_count, all_monthly_visits,
             all_monthly_visit_growth, all_no_articles, all_no_events]

# Script Starts Here
cbs = CrunchBaseScrapper()
cbs.go_company_ranking(1)
cbs.scrape_information()



# combine list into dataframe and print
df = pd.DataFrame({
    'CrunchBase Ranking': all_rnklst,
    'Company Name/Organisation Name': all_names,
    'Acquired by': all_acquired_by,
    'Location': all_locations,
    'Number of Employees': all_no_employees,
    'Industry': all_industries,
    'IPO Status': all_ipo_status,
    'Founded Date': all_founded_date,
    'Headquarters': all_hqs,
    'Founders': all_founders,
    'Operating Status': all_operating_status,
    'Hub Tags': all_hub_tags,
    'Last Funding Type': all_last_funding_types,
    'Company Type': all_company_types,
    'Investment Stage': all_rnklst,
    'Number of Investors': all_no_investors,
    'Number Funding Rounds': all_no_funding_rounds,
    'Total Funding Amount': all_total_funding_amt,
    'Number of exits': all_no_exits,
    'Number of Lead Investors': all_no_lead_investors,
    'Number of Acquisitions': all_no_acquisitions,
    'Number of Current Team Members (core team)': all_no_current_team,
    'Number of Board Members/Advisors': all_no_board_members,
    'Total Products Active': all_total_products_active,
    'Product Downloads in the Last 30 Days': all_product_downloads,
    'Active Tech Count': all_active_tech_count,
    'Monthly Visits': all_monthly_visits,
    'Monthly Visits Growth': all_monthly_visit_growth,
    'Number of Articles': all_no_articles,
    'Number of Events': all_no_events,
    'Number of Funds': all_no_funds,
    'Number of Investments': all_no_investments,
    'Number of Diversity Investments': all_no_diversity_investments,
    'Number of Exits': all_no_exits,
    'Related Hubs': all_hub_tags,
    'Investor Type': all_rnklst,
    'Stock Symbol': all_stock_symbols,
    'IPO Date': all_rnklst,
    'Number of Sub': all_rnklst,
    'Organisations': all_rnklst,
    'Funding Rounds': all_rnklst,
    'Funds Raised (for VC)': all_rnklst,
    'Number of Lead Investments': all_rnklst
})
