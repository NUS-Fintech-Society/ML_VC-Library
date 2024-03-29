import logging
from mlvc.config import config
from argparse import ArgumentParser
import os
from datetime import datetime
import pandas as pd

logging.basicConfig(level=logging.INFO)

def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '--mode',
        dest='mode',
        help='start mode, train, download_data' ' backtest',
        metavar='MODE',
        default='download_data',
    )
    parser.add_argument(
        '--type',
        dest='type',
        help='list information',
        metavar='TYPE',
        default='information',
    )
    return parser


def main():
    parser = build_parser()
    options = parser.parse_args()
    if not os.path.exists('./' + config.DATA_SAVE_DIR):
        os.makedirs('./' + config.DATA_SAVE_DIR)
        
    if options.mode == 'download_data':
        download_data(options)
    elif options.mode == 'train':
        train_model(options)

def download_data(options):
    from mlvc.data.web_driver import WebDriver
    from mlvc.data.crunch_base_scrapper import CrunchBaseScrapper

    csv_file = f'./{config.DATA_SAVE_DIR}/{options.mode}_{options.type}.csv'        

    if not os.path.isfile(csv_file):
        CrunchBaseScrapper.create_empty_header_file(csv_file, file_type=options.type)

    scraper = CrunchBaseScrapper()

    if options.type == 'list':            
        scraper.fetch_company_list(
            csv_file,
            backup=config.BACKUP,
            start=config.START_RANKING,
            end=config.END_RANKING,
            )

    elif options.type == 'information':
        companies = pd.read_csv(f'./{config.DATA_SAVE_DIR}/{config.COMPANY_LIST_FILE}.csv')
        scraper.fetch_company_data(
            companies, 
            csv_file,
            backup=config.BACKUP
            )

def train_model(options):
    from mlvc.train.crunchbase import Crunchbase

if __name__ == '__main__':
    main()
