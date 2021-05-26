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
        "--mode",
        dest="mode",
        help="start mode, train, download_data" " backtest",
        metavar="MODE",
        default="download_data",
    )
    parser.add_argument(
        "--type",
        dest="type",
        help="list information",
        metavar="TYPE",
        default="information",
    )
    return parser


def main():
    parser = build_parser()
    options = parser.parse_args()
    if not os.path.exists("./" + config.DATA_SAVE_DIR):
        os.makedirs("./" + config.DATA_SAVE_DIR)
        
    if options.mode == "download_data":
        now = datetime.now().strftime("%Y%m%d")
        from mlvc.data.crunch_base import CrunchBaseScrapper

        csv_file = f"./{config.DATA_SAVE_DIR}/{options.mode}_{options.type}.csv"
        if not os.path.isfile(csv_file):
            CrunchBaseScrapper.create_empty_header_file(csv_file, file_type=options.type)

        if options.type == "list":            
            CrunchBaseScrapper().fetch_company_list(
                start=config.START_RANKING, 
                end=config.END_RANKING, 
                step=config.STEP_RANKING, 
                backup_filepath=csv_file)

        elif options.type == "information":
            
            companies = pd.read_csv(f"./{config.DATA_SAVE_DIR}/company_url.csv")
            output = CrunchBaseScrapper().fetch_company_data(companies, backup_filepath=csv_file)
            output.to_csv(f"./{config.DATA_SAVE_DIR}/{now}_full.csv", index=False)

if __name__ == "__main__":
    main()
