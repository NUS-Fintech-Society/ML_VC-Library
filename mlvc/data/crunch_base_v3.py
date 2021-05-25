from helium import *
import selenium as selenium
from datetime import datetime
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

icon_mapping = {
    "M12,2C8.1,2,5,5.1,5,9c0,5.2,7,13,7,13s7-7.8,7-13C19,5.1,15.9,2,12,2z M12,11.5c-1.4,0-2.5-1.1-2.5-2.5s1.1-2.5,2.5-2.5s2.5,1.1,2.5,2.5S13.4,11.5,12,11.5z": 'location',
    "M16.36,10.91a3.28,3.28,0,1,0-3.27-3.27A3.26,3.26,0,0,0,16.36,10.91Zm-8.72,0A3.28,3.28,0,1,0,4.36,7.64,3.26,3.26,0,0,0,7.64,10.91Zm0,2.18C5.09,13.09,0,14.37,0,16.91v2.73H15.27V16.91C15.27,14.37,10.18,13.09,7.64,13.09Zm8.72,0a10.24,10.24,0,0,0-1,.06,4.59,4.59,0,0,1,2.14,3.76v2.73H24V16.91C24,14.37,18.91,13.09,16.36,13.09Z": "employee",
    "M12,2C6.5,2,2,6.5,2,12s4.5,10,10,10s10-4.5,10-10S17.5,2,12,2z M11,19.9c-3.9-0.5-7-3.9-7-7.9c0-0.6,0.1-1.2,0.2-1.8L9,15v1c0,1.1,0.9,2,2,2V19.9z M17.9,17.4c-0.3-0.8-1-1.4-1.9-1.4h-1v-3c0-0.6-0.4-1-1-1H8v-2h2c0.6,0,1-0.4,1-1V7h2c1.1,0,2-0.9,2-2V4.6c2.9,1.2,5,4.1,5,7.4C20,14.1,19.2,16,17.9,17.4z": "website",
    "M21.3,0H2.7C1.2,0,0,1.2,0,2.7v18.7C0,22.8,1.2,24,2.7,24h18.7c1.5,0,2.7-1.2,2.7-2.7V2.7C24,1.2,22.8,0,21.3,0z M21.3,21.3H2.7V2.7h18.7V21.3z": "rank",
    "M9,10.71A3.87,3.87,0,1,0,5.15,6.85,3.85,3.85,0,0,0,9,10.71Zm0,2.58c-3,0-9,1.51-9,4.51V21H18V17.8C18,14.8,12,13.29,9,13.29Z": "investor",
    "M8.44679391,9.59786248 L8.44679391,10.7127564 C9.51041577,10.9723892 10.0449539,11.7763782 10.0798625,12.6523663 L8.95515061,12.6523663 C8.92569647,12.016375 8.58861016,11.58329 7.68316796,11.58329 C6.82245242,11.58329 6.30864125,11.9705574 6.30864125,12.5247317 C6.30864125,13.0090887 6.67954528,13.3189027 7.83589315,13.6199895 C8.99115012,13.9199854 10.2282242,14.4141604 10.2282242,15.8595953 C10.2282242,16.903581 9.43950764,17.4784823 8.44679391,17.6661161 L8.44679391,18.7613739 L6.91954201,18.7613739 L6.91954201,17.6573889 C5.94210079,17.4479373 5.10756671,16.821764 5.04647664,15.7068701 L6.16464321,15.7068701 C6.2224606,16.3068619 6.63481862,16.7759464 7.68316796,16.7759464 C8.806789,16.7759464 9.05769467,16.2152268 9.05769467,15.8650497 C9.05769467,15.3916017 8.80351632,14.9432441 7.53044277,14.6377938 C6.1090076,14.2974348 5.13702086,13.7116246 5.13702086,12.5345497 C5.13702086,11.5527449 5.93119185,10.9112991 6.91954201,10.6974839 L6.91954201,9.59786248 L8.44679391,9.59786248 Z M1.5272519,20.2886258 L13.7452671,20.2886258 L13.7452671,8.07061058 L1.5272519,8.07061058 L1.5272519,20.2886258 Z M13.7452671,6.54335868 C14.5863465,6.54335868 15.272519,7.23062204 15.272519,8.07061058 L15.272519,20.2886258 C15.272519,21.1286143 14.5863465,21.8158777 13.7452671,21.8158777 L1.5272519,21.8158777 C0.687263355,21.8158777 -5.68434189e-14,21.1286143 -5.68434189e-14,20.2886258 L-5.68434189e-14,8.07061058 C-5.68434189e-14,7.23062204 0.687263355,6.54335868 1.5272519,6.54335868 L13.7452671,6.54335868 Z M24,13.0889422 L24,15.2707306 L17.4546347,15.2707306 L17.4546347,13.0889422 L24,13.0889422 Z M24,7.63447108 L24,9.81625951 L17.4546347,9.81625951 L17.4546347,7.63447108 L24,7.63447108 Z M24,2.18 L24,4.36178843 L12.0001636,4.36178843 L12.0001636,2.18 L24,2.18 Z": "investment_stage",
    "M12.52,10.53c-3-.78-4-1.6-4-2.86,0-1.46,1.35-2.47,3.6-2.47S15.37,6.33,15.45,8H18.4a5.31,5.31,0,0,0-4.28-5.08V0h-4V2.88c-2.59.56-4.67,2.24-4.67,4.81,0,3.08,2.55,4.62,6.27,5.51,3.33.8,4,2,4,3.21,0,.92-.65,2.39-3.6,2.39-2.75,0-3.83-1.23-4-2.8H5.21c.16,2.92,2.35,4.56,4.91,5.11V24h4V21.13c2.6-.49,4.67-2,4.67-4.73C18.79,12.61,15.55,11.32,12.52,10.53Z": "last_funding",
    "M14.4,6L14,4H5v17h2v-7h5.6l0.4,2h7V6H14.4z": "ipo_status",
    "M20,7h-4V5c0-1.1-0.9-2-2-2h-4C8.9,3,8,3.9,8,5v2H4C2.9,7,2,7.9,2,9l0,11c0,1.1,0.9,2,2,2h16c1.1,0,2-0.9,2-2V9C22,7.9,21.1,7,20,7z M14,7h-4V5h4V7z": "hiring_status"
}


class CrunchBaseScrapper_v3:
    driver = None
    profile_type = 	'profile_type'
    url = 'url'
    about = 'about'	
    name = 'name'	
    location = 'location'
    employee_no	= 'employee_no'
    investor_type = 'investor_type'	
    website = 'website'	
    no_funds = 'no_funds'	
    no_acquisition = 'no_acquisition'	
    no_investments = 'no_investments'	
    no_diversity_investments = 'no_diversity_investments'	
    no_exits = 'no_exits'	
    industries = 'industries'
    founded_date = 'founded_date'	
    founders = 'founders'	
    operating_status = 'operating_status'	
    last_funding_types = 'last_funding_types'
    hqs ='hqs'
    stock_symbols ='stock_symbols'	
    related_hubs = 'related_hubs'	
    company_types = 'company_types'	
    no_funding_rounds = 'no_funding_rounds'	
    funds_raised = 'funds_raised'	
    ipo_dates = 'ipo_dates'
    no_lead_investments	= 'no_lead_investments'
    total_products_active = 'total_products_active'	
    active_tech_count = 'active_tech_count'	
    monthly_visits = 'monthly_visits'	
    monthly_visit_growth = 'monthly_visit_growth'	
    no_articles	= 'no_articles	'
    no_events = 'no_events'
    rank = 'rank'	
    ipo_status	='ipo_status'
    total_funding_amt	='total_funding_amt'
    no_investors = 'no_investors'
    hub_tags = 'hub_tags'	
    no_lead_investors = 'no_lead_investors'
    product_downloads = 'product_downloads'
    investment_stages = 'investment_stages'
    

    def __init__(self, headless=False):
        self.options = selenium.webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.headless = headless
    
    @staticmethod
    def create_empty_header_file(filepath):
        df = pd.DataFrame({ CrunchBaseScrapper_v3.profile_type: [], CrunchBaseScrapper_v3.url: [], CrunchBaseScrapper_v3.about: [], CrunchBaseScrapper_v3.name: [], CrunchBaseScrapper_v3.location: [], 
                           CrunchBaseScrapper_v3.employee_no: [], CrunchBaseScrapper_v3.investor_type: [], CrunchBaseScrapper_v3.website: [],
                           CrunchBaseScrapper_v3.no_funds: [], CrunchBaseScrapper_v3.no_acquisition: [], CrunchBaseScrapper_v3.no_investments: [],
                           CrunchBaseScrapper_v3.no_diversity_investments: [], CrunchBaseScrapper_v3.no_exits: [], CrunchBaseScrapper_v3.industries: [],
                           CrunchBaseScrapper_v3.founded_date: [], CrunchBaseScrapper_v3.founders: [], CrunchBaseScrapper_v3.operating_status: [],
                           CrunchBaseScrapper_v3.last_funding_types: [], CrunchBaseScrapper_v3.hqs: [], CrunchBaseScrapper_v3.stock_symbols: [], 
                           CrunchBaseScrapper_v3.related_hubs: [], CrunchBaseScrapper_v3.company_types: [], CrunchBaseScrapper_v3.no_funding_rounds: [],
                           CrunchBaseScrapper_v3.funds_raised: [], CrunchBaseScrapper_v3.ipo_dates: [], CrunchBaseScrapper_v3.no_lead_investments: [], 
                           CrunchBaseScrapper_v3.total_products_active: [], CrunchBaseScrapper_v3.active_tech_count: [], CrunchBaseScrapper_v3.monthly_visits: [],
                           CrunchBaseScrapper_v3.monthly_visit_growth: [], CrunchBaseScrapper_v3.no_articles: [], CrunchBaseScrapper_v3.no_events: [],
                           CrunchBaseScrapper_v3.rank: [], CrunchBaseScrapper_v3.ipo_status: [], CrunchBaseScrapper_v3.total_funding_amt: [], CrunchBaseScrapper_v3.no_investors: [],
                           CrunchBaseScrapper_v3.hub_tags: [], CrunchBaseScrapper_v3.no_lead_investors: [], CrunchBaseScrapper_v3.product_downloads: [],
                           CrunchBaseScrapper_v3.investment_stages: [],})
        
        df.to_csv(filepath, index=False)

    def fetch_data(self, start, end, data, backup_filepath=None):
        df = pd.DataFrame()
        df1 = data
        #for i in range(len(df1)): 
        for i in range(10):
            if not self.driver:
                self.driver = start_chrome(headless=self.headless, options=self.options)

            obj = self.scrape_information(df1['company_url'].iloc[i])
            obj['rank'] = i
            df = pd.DataFrame([obj]) if df.empty else df.append([obj])
            #kill_browser()
            
            if backup_filepath:
                df = pd.DataFrame([obj]) if df.empty else df.append([obj])
                df.to_csv(backup_filepath, mode='a', header=False, index=False)
        
        return df

    def _go_company_URL(self, url):
        if not self.driver:
            raise Exception("Driver not initialised")
        go_to(f"{url}")
        time.sleep(3)
        if Text("Please verify you are a human").exists():
            element = self.driver.find_element_by_id('px-captcha').find_element_by_tag_name("iframe")
            ActionChains(self.driver).click_and_hold(element).perform()
            time.sleep(5)
            ActionChains(self.driver).release(element).perform()
            time.sleep(3)

        print("Org exists, clicking now")
        time.sleep(3)
        
    def scrape_information(self, url):
        self._go_company_URL(url)

        output = {}

        profile_name = self.driver.current_url.split('/')[-1:]
        profile_type = self._get_profile_type()
        general_info = self._get_general_information()
        about = self._get_about()
        highlights = self._get_highlights()
        details = self._get_details()
        news = self._get_recentNews()

        output['profile_type'] = profile_type
        output['url'] = url
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # check if its investment firm
        if profile_type == "INVESTMENT FIRM":
            # Summary Page
            # general info
            if about is not None:
                output['about'] = about[0]

            if profile_name is not None:
                output['name'] = profile_name[0]
            if 'location' in general_info:
                output['location'] = general_info['location']
            if 'employee' in general_info:
                output['employee_no'] = general_info['employee']
            if 'investor' in general_info:
                output['investor_type'] = general_info['investor']
            if 'investment_stage' in general_info:
                output['investment_stages'] = general_info['investment_stage']
            if 'website' in general_info:
                output['website'] = general_info['website']

            # Highlights
            if 'Number of Funds' in highlights:
                output['no_funds'] = highlights['Number of Funds']
            if 'Number of Acquisitions' in highlights:
                output['no_acquisition'] = highlights['Number of Acquisitions']
            if 'Number of Investments' in highlights:
                output['no_investments'] = highlights['Number of Investments']
            if 'Number of Diversity Investments' in highlights:
                output['no_diversity_investments'] = highlights['Number of Diversity Investments']
            if 'Number of Exits' in highlights:
                output['no_exits'] = highlights['Number of Exits']
            if 'Total Funding Amount' in highlights:
                output['total_funding_amt'] = highlights['Total Funding Amount']

            # Details
            if 'Industries' in details:
                output['industries'] = details['Industries']
            if 'Founded Date' in details:
                output['founded_date'] = details['Founded Date']
            if 'Founders' in details:
                output['founders'] = details['Founders']
            if 'Operating Status' in details:
                output['operating_status'] = details['Operating Status']
            if 'Last Funding Type' in details:
                output['last_funding_types'] = details['Last Funding Type']
            if 'Headquarters Regions' in details:
                output['hqs'] = details['Headquarters Regions']
            if 'Stock Symbol' in details:
                output['stock_symbols'] = details['Stock Symbol']
            if 'Related Hubs' in details:
                output['related_hubs'] = details['Related Hubs']
            if 'Hub Tags' in details:
                output['hub_tags'] = details['Hub Tags']
            if 'Company Type' in details:
                output['company_types'] = details['Company Type']

            # Financials Page
            go_to(
                f"https://www.crunchbase.com/organization/{profile_name[0].lower()}/investor_financials")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # highlights
            highlights2 = self._get_highlights3()
            highlights3 = self._get_highlights2()
            if 'Number of Funding Rounds' in highlights2:
                output['no_funding_rounds'] = highlights2['Number of Funding Rounds']
            if 'Number of Lead Investors' in highlights2:
                output['no_lead_investors'] = highlights2['Number of Lead Investors']
            if 'Number of Investors' in highlights2:
                output['no_investors'] = highlights2['Number of Investors']
            if 'Total Fund Raised' in highlights2:
                output['funds_raised'] = highlights2['Total Fund Raised']
            if 'IPO Date' in highlights3:
                output['ipo_dates'] = highlights3['IPO Date']

            # Investments Page
            go_to(
                f"https://www.crunchbase.com/organization/{profile_name[0].lower()}/recent_investments")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            highlights3 = self._get_highlights()
            if 'Number of Lead Investments' in highlights3:
                output['no_lead_investments'] = highlights3['Number of Lead Investments']

            # People Page
            go_to(
                f"https://www.crunchbase.com/organization/{profile_name[0].lower()}/people")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            highlights4 = self._get_highlights()
            if 'Number of Board Members / Advisors' in highlights4:
                output['no_board_members'] = highlights4['Number of Board Members / Advisors']
            if 'Number of Current Team' in highlights4:
                output['no_current_team'] = highlights4['Number of Current Team']

            # Technology Page
            go_to(
                f"https://www.crunchbase.com/organization/{profile_name[0].lower()}/technology")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            highlights5 = self._get_highlights()
            if 'Total Products Active' in highlights5:
                output['total_products_active'] = highlights5['Total Products Active']
            if 'Active Tech Count' in highlights5:
                output['active_tech_count'] = highlights5['Active Tech Count']
            if 'Monthly Visits' in highlights5:
                output['monthly_visits'] = highlights5['Monthly Visits']
            if 'Monthly Visits Growth' in highlights5:
                output['monthly_visit_growth'] = highlights5['Monthly Visits Growth']
            if 'Downloads Last 30 Days' in highlights5:
                output['product_downloads'] = highlights5['Downloads Last 30 Days']

            # Signals & News Page
            go_to(
                f"https://www.crunchbase.com/organization/{profile_name[0].lower()}/signals_and_news")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            news = self._get_recentNews()
            if 'Number of Articles' in news:
                output['no_articles'] = news['Number of Articles']
            if 'Number of Events' in news:
                output['no_events'] = news['Number of Events']

        if profile_type == "ORGANIZATION":
            # Summary Page
            # general info
            if about is not None:
                output['about'] = about[0]

            if profile_name is not None:
                output['name'] = profile_name[0]
            if 'location' in general_info:
                output['location'] = general_info['location']
            if 'employee' in general_info:
                output['employee_no'] = general_info['employee']
            if 'ipo_status' in general_info:
                output['ipo_status'] = general_info['ipo_status']
            if 'website' in general_info:
                output['website'] = general_info['website']

            # Highlights
            if 'Number of Acquisitions' in highlights:
                output['no_acquisition'] = highlights['Number of Acquisitions']
            if 'Number of Investments' in highlights:
                output['no_investments'] = highlights['Number of Investments']
            if 'Total Funding Amount' in highlights:
                output['total_funding_amt'] = highlights['Total Funding Amount']
            if 'Number of Current Team Members' in highlights:
                output['no_current_team'] = highlights['Number of Current Team Members']
            if 'Number of Investors' in highlights:
                output['no_investors'] = highlights['Number of Investors']

            # Details
            if 'Industries' in details:
                output['industries'] = details['Industries']
            if 'Headquarters Regions' in details:
                output['hqs'] = details['Headquarters Regions']
            if 'Founded Date' in details:
                output['founded_date'] = details['Founded Date']
            if 'Founders' in details:
                output['founders'] = details['Founders']
            if 'Operating Status' in details:
                output['operating_status'] = details['Operating Status']
            if 'Last Funding Type' in details:
                output['last_funding_types'] = details['Last Funding Type']
            if 'Related Hubs' in details:
                output['related_hubs'] = details['Related Hubs']
            if 'Hub Tags' in details:
                output['hub_tags'] = details['Hub Tags']
            if 'Company Type' in details:
                output['company_types'] = details['Company Type']

            # Financials Page
            go_to(
                f"https://www.crunchbase.com/organization/{profile_name[0].lower()}/company_financials")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            highlights2 = self._get_highlights()
            highlights3 = self._get_highlights2()

            if 'Number of Funding Rounds' in highlights2:
                output['no_funding_rounds'] = highlights2['Number of Funding Rounds']
            if 'Number of Lead Investors' in highlights2:
                output['no_lead_investors'] = highlights2['Number of Lead Investors']
            if 'Number of Lead Investments' in highlights2:
                output['no_lead_investments'] = highlights2['Number of Lead Investments']
            if 'Number of Exits' in highlights2:
                output['no_exits'] = highlights2['Number of Exits']
            if 'IPO Date' in highlights3:
                output['ipo_dates'] = highlights3['IPO Date']

            # People Page
            go_to(
                f"https://www.crunchbase.com/organization/{profile_name[0].lower()}/people")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            highlights4 = self._get_highlights()

            if 'Number of Board Members / Advisors' in highlights4:
                output['no_board_members'] = highlights4['Number of Board Members / Advisors']
            if 'Number of Current Team' in highlights4:
                output['no_current_team'] = highlights4['Number of Current Team']

            # Technology Page
            go_to(
                f"https://www.crunchbase.com/organization/{profile_name[0].lower()}/technology")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # highlights
            highlights5 = self._get_highlights()
            if 'Total Products Active' in highlights5:
                output['total_products_active'] = highlights5['Total Products Active']
            if 'Active Tech Count' in highlights5:
                output['active_tech_count'] = highlights5['Active Tech Count']
            if 'Monthly Visits' in highlights5:
                output['monthly_visits'] = highlights5['Monthly Visits']
            if 'Monthly Visits Growth' in highlights5:
                output['monthly_visit_growth'] = highlights5['Monthly Visits Growth']
            if 'Downloads Last 30 Days' in highlights5:
                output['product_downloads'] = highlights5['Downloads Last 30 Days']

            # Signals & News Page
            go_to(
                f"https://www.crunchbase.com/organization/{profile_name[0].lower()}/signals_and_news")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            news = self._get_recentNews()
            if 'Number of Articles' in news:
                output['no_articles'] = news['Number of Articles']
            if 'Number of Events' in news:
                output['no_events'] = news['Number of Events']

        return output

    def _check_driver(self):
        if not self.driver:
            raise Exception("Driver not initialised")

    def _get_profile_type(self):
        self._check_driver()
        profile_type = [cell.web_element.text for cell in find_all(S(".profile-type"))]
        return profile_type[0] if profile_type else ""

    def _get_profile_name(self):
        self._check_driver()
        profile_name = [cell.web_element.text for cell in find_all(S(".profile-name"))]
        return profile_name if profile_name else ""

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
        short_about = about
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

    def _get_highlights2(self):
        self._check_driver()
        obj = {}
        highlight_element = S("profile-section > section-card > mat-card > div > div > fields-card > ul > li")
        highlight_list = [cell.web_element.text.split("\n") for cell in find_all(highlight_element)]
        res = list(map(lambda x: (", ".join(x[:-1]).strip(), x[-1]), highlight_list))
        for key, value in res:
            obj[key] = value
        return obj

    def _get_highlights3(self):
        self._check_driver()
        obj = {}
        highlight_element = S("profile-section > section-card > mat-card > div > div > big-values-card > div")
        highlight_list = [cell.web_element.text.split("\n") for cell in find_all(highlight_element)]
        res = list(map(lambda x: (", ".join(x[:-1]).strip(), x[-1]), highlight_list))
        for key, value in res:
            obj[key] = value
        return obj

    def _get_details(self):
        self._check_driver()
        obj = {}
        detail_element = S("row-card > profile-section > section-card > mat-card > div > div > fields-card > ul > li")
        detail_list = [cell.web_element.text.split("\n") for cell in find_all(detail_element)]
        res = list(map(lambda x: (", ".join(x[:1]).strip(), x[1:]), detail_list))
        for key, value in res:
            obj[key] = value
        return obj

    def _get_recentNews(self):
        self._check_driver()
        obj = {}
        recent_news_element = S("profile-section > section-card > mat-card > div > div > big-values-card")
        recent_news_list = [cell.web_element.text.split("\n") for cell in find_all(recent_news_element)]
        res = list(map(lambda x: (", ".join(x[:1]).strip(), x[1:]), recent_news_list))
        for key, value in res:
            obj[key] = value
        return obj
    