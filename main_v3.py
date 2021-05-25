import logging
from mlvc.config import config
from argparse import ArgumentParser
import os
from datetime import datetime
import pandas as pd


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--mode",
        dest="mode",
        help="start mode, train, download_data" " backtest",
        metavar="MODE",
        default="download_data",
    )
    return parser


def main():
    logging.info("Logger successfully initialized, running main.py")
    parser = build_parser()
    options = parser.parse_args()
    if not os.path.exists("./" + config.DATA_SAVE_DIR):
        os.makedirs("./" + config.DATA_SAVE_DIR)
        
    if options.mode == "download_data":
        now = datetime.now().strftime("%Y%m%d")
        from mlvc.data.crunch_base_v3 import CrunchBaseScrapper_v3
        csv_file = f"./{config.DATA_SAVE_DIR}/{now}_{config.START_RANKING}_{config.END_RANKING}.csv" # to change the file
        
        if not os.path.isfile(csv_file):
            CrunchBaseScrapper_v3.create_empty_header_file(csv_file)
        
        df = pd.read_csv(f"./{config.DATA_SAVE_DIR}/data_100000-200000.csv")
        df= df.drop_duplicates()
        df1 = CrunchBaseScrapper_v3(headless=False).fetch_data(start=config.start, end=len(df), data=df, backup_filepath=csv_file)
        df1= df1.drop_duplicates(['url'])
        end = len(df1)
        df1.to_csv(f"./{config.DATA_SAVE_DIR}/{now}_{config.start}_{end}_full.csv", index=False)

        

if __name__ == "__main__":
    main()
