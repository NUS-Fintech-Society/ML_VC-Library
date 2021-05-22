import logging
from mlvc.config import config
from argparse import ArgumentParser
import os
from datetime import datetime


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
        from mlvc.data.crunch_base_v2 import CrunchBaseScrapper_v2

        csv_file = f"./{config.DATA_SAVE_DIR}/{now}_{config.START_RANKING}_{config.END_RANKING}.csv"
        
        if not os.path.isfile(csv_file):
            CrunchBaseScrapper_v2.create_empty_header_file(csv_file)

        CrunchBaseScrapper_v2(headless=False).fetch_data(
            start=config.START_RANKING, 
            end=config.END_RANKING, 
            step=config.STEP_RANKING, 
            backup_filepath=csv_file
            )
            
if __name__ == "__main__":
    main()
