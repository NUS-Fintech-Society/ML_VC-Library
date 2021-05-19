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
        from mlvc.data.crunch_base_v3 import CrunchBaseScrapper
        df = pd.read_csv("test.csv")
        df = CrunchBaseScrapper(headless=False).fetch_data(start=0, end=len(df), data=df)
        now = datetime.now().strftime("%Y%m%d")
        #print(df)
        df.to_csv(f"./{config.DATA_SAVE_DIR}/{now}_{config.START_RANKING}_{config.END_RANKING}.csv", index=False)


if __name__ == "__main__":
    main()
