import json
from datetime import datetime
import os
import sys

sys.path.append("../modules")
import io_module


def main(brand):
    print('cleansing.py start')
    crawled_data = io_module.load_json("new", brand, "crawling")
    # clean the crawled_data in the block below
    # ----------------------------------------------------
    output = crawled_data
    # ----------------------------------------------------
    io_module.save_json(output, brand, "cleansing")

if __name__ == "__main__":
    if sys.argv[1] is not None:
        brand = sys.argv[1]
        main(brand)

