from helium import *
import selenium as selenium
from datetime import datetime
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import logging
from mlvc.utility.utils import title_to_underscore

icon_mapping = {
    'M12,2C8.1,2,5,5.1,5,9c0,5.2,7,13,7,13s7-7.8,7-13C19,5.1,15.9,2,12,2z M12,11.5c-1.4,0-2.5-1.1-2.5-2.5s1.1-2.5,2.5-2.5s2.5,1.1,2.5,2.5S13.4,11.5,12,11.5z': 'location',
    'M16.36,10.91a3.28,3.28,0,1,0-3.27-3.27A3.26,3.26,0,0,0,16.36,10.91Zm-8.72,0A3.28,3.28,0,1,0,4.36,7.64,3.26,3.26,0,0,0,7.64,10.91Zm0,2.18C5.09,13.09,0,14.37,0,16.91v2.73H15.27V16.91C15.27,14.37,10.18,13.09,7.64,13.09Zm8.72,0a10.24,10.24,0,0,0-1,.06,4.59,4.59,0,0,1,2.14,3.76v2.73H24V16.91C24,14.37,18.91,13.09,16.36,13.09Z': 'employee',
    'M12,2C6.5,2,2,6.5,2,12s4.5,10,10,10s10-4.5,10-10S17.5,2,12,2z M11,19.9c-3.9-0.5-7-3.9-7-7.9c0-0.6,0.1-1.2,0.2-1.8L9,15v1c0,1.1,0.9,2,2,2V19.9z M17.9,17.4c-0.3-0.8-1-1.4-1.9-1.4h-1v-3c0-0.6-0.4-1-1-1H8v-2h2c0.6,0,1-0.4,1-1V7h2c1.1,0,2-0.9,2-2V4.6c2.9,1.2,5,4.1,5,7.4C20,14.1,19.2,16,17.9,17.4z': 'website',
    'M21.3,0H2.7C1.2,0,0,1.2,0,2.7v18.7C0,22.8,1.2,24,2.7,24h18.7c1.5,0,2.7-1.2,2.7-2.7V2.7C24,1.2,22.8,0,21.3,0z M21.3,21.3H2.7V2.7h18.7V21.3z': 'rank',
    'M9,10.71A3.87,3.87,0,1,0,5.15,6.85,3.85,3.85,0,0,0,9,10.71Zm0,2.58c-3,0-9,1.51-9,4.51V21H18V17.8C18,14.8,12,13.29,9,13.29Z': 'investor',
    'M8.44679391,9.59786248 L8.44679391,10.7127564 C9.51041577,10.9723892 10.0449539,11.7763782 10.0798625,12.6523663 L8.95515061,12.6523663 C8.92569647,12.016375 8.58861016,11.58329 7.68316796,11.58329 C6.82245242,11.58329 6.30864125,11.9705574 6.30864125,12.5247317 C6.30864125,13.0090887 6.67954528,13.3189027 7.83589315,13.6199895 C8.99115012,13.9199854 10.2282242,14.4141604 10.2282242,15.8595953 C10.2282242,16.903581 9.43950764,17.4784823 8.44679391,17.6661161 L8.44679391,18.7613739 L6.91954201,18.7613739 L6.91954201,17.6573889 C5.94210079,17.4479373 5.10756671,16.821764 5.04647664,15.7068701 L6.16464321,15.7068701 C6.2224606,16.3068619 6.63481862,16.7759464 7.68316796,16.7759464 C8.806789,16.7759464 9.05769467,16.2152268 9.05769467,15.8650497 C9.05769467,15.3916017 8.80351632,14.9432441 7.53044277,14.6377938 C6.1090076,14.2974348 5.13702086,13.7116246 5.13702086,12.5345497 C5.13702086,11.5527449 5.93119185,10.9112991 6.91954201,10.6974839 L6.91954201,9.59786248 L8.44679391,9.59786248 Z M1.5272519,20.2886258 L13.7452671,20.2886258 L13.7452671,8.07061058 L1.5272519,8.07061058 L1.5272519,20.2886258 Z M13.7452671,6.54335868 C14.5863465,6.54335868 15.272519,7.23062204 15.272519,8.07061058 L15.272519,20.2886258 C15.272519,21.1286143 14.5863465,21.8158777 13.7452671,21.8158777 L1.5272519,21.8158777 C0.687263355,21.8158777 -5.68434189e-14,21.1286143 -5.68434189e-14,20.2886258 L-5.68434189e-14,8.07061058 C-5.68434189e-14,7.23062204 0.687263355,6.54335868 1.5272519,6.54335868 L13.7452671,6.54335868 Z M24,13.0889422 L24,15.2707306 L17.4546347,15.2707306 L17.4546347,13.0889422 L24,13.0889422 Z M24,7.63447108 L24,9.81625951 L17.4546347,9.81625951 L17.4546347,7.63447108 L24,7.63447108 Z M24,2.18 L24,4.36178843 L12.0001636,4.36178843 L12.0001636,2.18 L24,2.18 Z': 'investment_stage',
    'M12.52,10.53c-3-.78-4-1.6-4-2.86,0-1.46,1.35-2.47,3.6-2.47S15.37,6.33,15.45,8H18.4a5.31,5.31,0,0,0-4.28-5.08V0h-4V2.88c-2.59.56-4.67,2.24-4.67,4.81,0,3.08,2.55,4.62,6.27,5.51,3.33.8,4,2,4,3.21,0,.92-.65,2.39-3.6,2.39-2.75,0-3.83-1.23-4-2.8H5.21c.16,2.92,2.35,4.56,4.91,5.11V24h4V21.13c2.6-.49,4.67-2,4.67-4.73C18.79,12.61,15.55,11.32,12.52,10.53Z': 'last_funding',
    'M14.4,6L14,4H5v17h2v-7h5.6l0.4,2h7V6H14.4z': 'ipo_status',
    'M20,7h-4V5c0-1.1-0.9-2-2-2h-4C8.9,3,8,3.9,8,5v2H4C2.9,7,2,7.9,2,9l0,11c0,1.1,0.9,2,2,2h16c1.1,0,2-0.9,2-2V9C22,7.9,21.1,7,20,7z M14,7h-4V5h4V7z': 'hiring_status'
}

ignored_column = [' ', 'also_known_as', 'legal_name', 'rank', 'contact_email', 'phone_number', 'transaction_name']

class CrunchBaseScrapper:
    company_name:str = 'company_name'
    company_url = 'company_url'
    name = 'name'
    profile_type = 'profile_type'
    about = 'about'
    location = 'location'
    employee = 'employee'
    investor = 'investor'
    hiring_status = 'hiring_status'
    investor_type = 'investor_type'
    website = 'website'
    industries = 'industries'
    founded_date = 'founded_date'
    closed_date = 'closed_date'
    founders = 'founders'
    operating_status = 'operating_status'
    last_funding_type = 'last_funding_type'
    stock_symbols = 'stock_symbol'
    hqs = 'headquarters_regions'
    related_hubs = 'related_hubs'
    company_type = 'company_type'
    ipo_status = 'ipo_status'
    hub_tags = 'hub_tags'
    product_downloads = 'product_downloads'
    investment_stage = 'investment_stage'
    no_funding_rounds = 'number_of_funding_rounds'
    no_lead_investors = 'number_of_lead_investors'
    no_investors = 'number_of_investors'
    funds_raised = 'funds_raised'
    no_funds = 'number_of_funds'
    total_funding_amt ='total_funding_amount'
    ipo_dates = 'ipo_date'
    total_fund_raised = 'total_fund_raised'
    no_investments = 'number_of_investments'
    no_lead_investments = 'number_of_lead_investments'
    no_diversity_investments = 'number_of_diversity_investments'
    no_acquisition = 'number_of_acquisitions'
    no_exits = 'number_of_exits'
    no_board_members = 'number_of_board_member_and_advisor_profiles'
    no_current_team = 'number_of_employee_profiles'
    total_products_active = 'total_products_active'
    monthly_visits = 'monthly_visits'
    monthly_visit_growth = 'monthly_visits_growth'
    active_tech_count = 'active_tech_count'
    no_articles = 'number_of_articles'
    no_events = 'number_of_events'
    valuation_at_ipo = 'valuation_at_ipo'
    money_raised_at_ipo = 'money_raised_at_ipo'
    last_funding = 'last_funding'
    ipo_share_price = 'ipo_share_price'
    downloads_last_30_days = 'downloads_last_30_days'
    acquired_by = 'acquired_by'
    announced_date = 'announced_date'
    price = 'price'

    company_information_columns = [
        name,
        profile_type,
        about,
        location,
        employee,
        hiring_status,
        investor,
        investor_type,
        website,
        industries,
        founded_date,
        closed_date,
        founders,
        operating_status,
        last_funding_type,
        stock_symbols,
        hqs,
        related_hubs,
        company_type,
        ipo_status,
        hub_tags,
        product_downloads,
        investment_stage,
        no_funding_rounds,
        no_lead_investors,
        no_investors,
        funds_raised,
        no_funds,
        total_funding_amt,
        ipo_dates,
        total_fund_raised,
        no_investments,
        no_lead_investments,
        no_diversity_investments,
        no_acquisition,
        no_exits,
        no_board_members,
        no_current_team,
        total_products_active,
        monthly_visits,
        monthly_visit_growth,
        active_tech_count,
        no_articles,
        no_events,
        valuation_at_ipo,
        money_raised_at_ipo,
        last_funding,
        ipo_share_price,
        downloads_last_30_days,
        acquired_by,
        announced_date,
        price
        ]

    @staticmethod
    def create_empty_header_file(filepath, file_type='information'):
        if file_type == 'information':
            df = CrunchBaseScrapper.get_empty_company_information()

        elif file_type == 'list':
            df = CrunchBaseScrapper.get_empty_company_list()
        
        else:
            df = pd.DataFrame()

        df.to_csv(filepath, index=False)

    @staticmethod
    def get_empty_company_list():
        return pd.DataFrame({ 
            CrunchBaseScrapper.company_name: [], 
            CrunchBaseScrapper.company_url: [] 
        })

    @staticmethod
    def get_empty_company_information():
        return pd.DataFrame({ 
            CrunchBaseScrapper.name: [],
            CrunchBaseScrapper.profile_type: [],
            CrunchBaseScrapper.about: [],
            CrunchBaseScrapper.location: [],
            CrunchBaseScrapper.employee: [],
            CrunchBaseScrapper.hiring_status: [],
            CrunchBaseScrapper.investor: [],
            CrunchBaseScrapper.investor_type: [],
            CrunchBaseScrapper.website: [],
            CrunchBaseScrapper.industries: [],
            CrunchBaseScrapper.founded_date: [],
            CrunchBaseScrapper.closed_date: [],
            CrunchBaseScrapper.founders: [],
            CrunchBaseScrapper.operating_status: [],
            CrunchBaseScrapper.last_funding_type: [],
            CrunchBaseScrapper.stock_symbols: [],
            CrunchBaseScrapper.hqs: [],
            CrunchBaseScrapper.related_hubs: [],
            CrunchBaseScrapper.company_type: [],
            CrunchBaseScrapper.ipo_status: [],
            CrunchBaseScrapper.hub_tags: [],
            CrunchBaseScrapper.product_downloads: [],
            CrunchBaseScrapper.investment_stage: [],
            CrunchBaseScrapper.no_funding_rounds: [],
            CrunchBaseScrapper.no_lead_investors: [],
            CrunchBaseScrapper.no_investors: [],
            CrunchBaseScrapper.funds_raised: [],
            CrunchBaseScrapper.no_funds: [],
            CrunchBaseScrapper.total_funding_amt: [],
            CrunchBaseScrapper.ipo_dates: [],
            CrunchBaseScrapper.total_fund_raised: [],
            CrunchBaseScrapper.no_investments: [],
            CrunchBaseScrapper.no_lead_investments: [],
            CrunchBaseScrapper.no_diversity_investments: [],
            CrunchBaseScrapper.no_acquisition: [],
            CrunchBaseScrapper.no_exits: [],
            CrunchBaseScrapper.no_board_members: [],
            CrunchBaseScrapper.no_current_team: [],
            CrunchBaseScrapper.total_products_active: [],
            CrunchBaseScrapper.monthly_visits: [],
            CrunchBaseScrapper.monthly_visit_growth: [],
            CrunchBaseScrapper.active_tech_count: [],
            CrunchBaseScrapper.no_articles: [],
            CrunchBaseScrapper.no_events: [],
            CrunchBaseScrapper.valuation_at_ipo: [],
            CrunchBaseScrapper.money_raised_at_ipo: [],
            CrunchBaseScrapper.last_funding: [],
            CrunchBaseScrapper.ipo_share_price: [],
            CrunchBaseScrapper.downloads_last_30_days: [],
            CrunchBaseScrapper.acquired_by: [],
            CrunchBaseScrapper.announced_date: [],
            CrunchBaseScrapper.price: []
        })

    
    def fetch_data(self, driver, output_filepath, backup=True, start=100001, end=300000):
        name_list = []
        link_list = []
        for i in range(start, end, 15):
            logging.info(f'Processing companies ranked {i} to {i+15}')
            is_navigation_successful = self._go_company_ranking(driver, i)
            if not is_navigation_successful:
                continue

            names = [cell.web_element.text for cell in find_all(
                S('div > grid-row > grid-cell > div > field-formatter > identifier-formatter > a',
                  below='Organization Name'))]
            
            links = [cell.web_element.get_attribute('href') for cell in find_all(
                S('div > grid-row > grid-cell > div > field-formatter > identifier-formatter > a',
                  below='Organization Name'))]

            if backup:
                df = pd.DataFrame({ self.name_header: names, self.url_header: links })
                df.to_csv(output_filepath, mode='a', header=False, index=False)
            else:
                name_list.append(names)
                link_list.append(links)

        if not backup:
            output = pd.DataFrame({ self.name_header: name_list, self.url_header: link_list })
            output.to_csv(output_filepath, index=False)

    def fetch_company_data(self, driver, companies, output_filepath, backup=True):
        output = CrunchBaseScrapper.get_empty_company_information()
        for c in companies.values:
            company = c[1]
            logging.info(f'Currently scraping {company}')
            is_navigation_successful = self._go_company_information(driver, company)

            if not is_navigation_successful:
                logging.info(f'Unable to navigate to {company}, proceeding to next..')
                continue

            data = self._scrape_company_information(driver, company)
            output.append(data, ignore_index=True)
            if backup:
                CrunchBaseScrapper.get_empty_company_information().append(
                    data, 
                    ignore_index=True
                    ).to_csv(
                        output_filepath, 
                        mode='a', 
                        header=False, 
                        index=False
                    )
        return output

    def _go_company_ranking(self, driver, ranking):
        url = f'https://www.crunchbase.com/search/organization.companies/field/organizations/rank_org_company/{ranking}'
        return self._go_to_url(
            driver,
            url
            )

    def _go_company_information(self, driver, endpoint):
        url = f'https://www.crunchbase.com/organization/{endpoint}'
        return self._go_to_url(
            driver,
            url
        )
    
    def _go_to_url(self, driver, url, time_wait=2, connection_attempt=3):
        attempt = 0
        while attempt < 3:
            try:
                driver.get(url)
                time.sleep(time_wait)
                return False if Text('Please verify you are a human').exists() else True     
            except Exception as e:
                attempt += 1
        return False
    
    def _get_value_from_key(self, dictionary, key):
        return dictionary[key] if key in dictionary else ''

    def _scrape_company_information(self, driver, company, sleep_duration=2):
        profile_type = self._get_profile_type()
        general_info = self._get_general_information()
        about = self._get_about()
        summary_highlights = self._get_highlights()

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        details = self._get_details()

        output = {}
        output['name'] = company
        output['profile_type'] = profile_type
        output['about'] = about[0] if about is not None else ''
        output = {**output, **general_info}
        output = {**output, **details}

        if Link('Financials').exists():
            click(Link('Financials'))
            time.sleep(sleep_duration)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            big_values = self._get_big_value_cards()
            field_values = self._get_field_cards() 
            output = {**output, **field_values, **big_values}

        if Link('Investments').exists():
            click(Link('Investments'))
            time.sleep(sleep_duration)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            big_values = self._get_big_value_cards()
            field_values = self._get_field_cards() 
            output = {**output, **field_values, **big_values}

        if Link('People').exists():
            click(Link('People'))
            time.sleep(sleep_duration)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            people_highlights = self._get_highlights()
            output = {**output, **people_highlights}

        if Link('Technology').exists():
            click(Link('Technology'))
            time.sleep(sleep_duration)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            technology_highlights = self._get_highlights()
            output = {**output, **technology_highlights}

        if Link('Signals & News').exists():
            click(Link('Signals & News'))
            time.sleep(sleep_duration)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            news = self._get_recent_news()
            output = {**output, **news}

        return output

    def _get_profile_type(self):
        profile_type = [cell.web_element.text for cell in find_all(S('.profile-type'))]
        return profile_type[0] if profile_type else ''

    def _get_profile_name(self):
        profile_name = [cell.web_element.text for cell in find_all(S('.profile-name'))]
        return profile_name if profile_name else ''

    def _get_location(self):
        location = [cell.web_element.text for cell in find_all(S('fields-card > ul > li > label-with-icon > span'))]
        return location

    def _get_general_information(self):
        obj = {}
        element = S('fields-card > ul > li > label-with-icon')
        items = find_all(element)
        general_list = [(cell.web_element.find_element_by_tag_name('path').get_attribute('d'), cell.web_element.text)
                        for cell in items]
        for key, value in general_list:
            obj = self._add_to_company_information(obj, icon_mapping[key] , value)
        return obj

    def _get_about(self):
        if Button('READ MORE').exists():
            click(Button('READ MORE'))
        about = [cell.web_element.text for cell in find_all(S('description-card > div > span'))]
        short_about = about
        long_about = ', '.join(about[1:])
        return short_about, long_about


    def _get_details(self):
        obj = {}
        detail_element = S("row-card > profile-section > section-card > mat-card > div > div > fields-card > ul > li")
        detail_list = [cell.web_element.text.split('\n') for cell in find_all(detail_element)]
        res = list(map(lambda x: (', '.join(x[:1]).strip(), x[1:]), detail_list))
        for key, value in res:
            obj = self._add_to_company_information(obj, title_to_underscore(key), value)
        return obj

    def _get_values_from_card(self, path):
        obj = {}
        element = S(path)
        lists = [cell.web_element.text.split('\n') for cell in find_all(element)]
        res = list(map(lambda x: (', '.join(x[:-1]).strip(), x[-1]), lists))
        for key, value in res:
            obj = self._add_to_company_information(obj, title_to_underscore(key), value)
        return obj

    def _get_highlights(self):
        return self._get_values_from_card('profile-section > section-card > mat-card > div > div > anchored-values > div > a > div')

    def _get_field_cards(self):
        return self._get_values_from_card('profile-section > section-card > mat-card > div > div > fields-card > ul > li')

    def _get_big_value_cards(self):
        return self._get_values_from_card('profile-section > section-card > mat-card > div > div > big-values-card > div')

    def _get_recent_news(self):
        return self._get_values_from_card('profile-section > section-card > mat-card > div > div > big-values-card')
    
    def _add_to_company_information(self, obj, key, value):
        if key in self.company_information_columns:
            obj[key] = value
        elif key not in self.company_information_columns and key not in ignored_column:
            logging.info(f'The key {key} with value {value} exists but is not stored in excel')
        return obj