import json
from datetime import datetime
import os
import sys

sys.path.append("../modules")
import io_module


def main():
    brand = sys.argv[1]
    print('cleansing.py start')
    crawled_data = io_module.get_json("new", brand, "crawling")
    # clean the crawled_data in the block below
    # ----------------------------------------------------
    output = crawled_data
    # ----------------------------------------------------
    io_module.upload_json(output, brand, "cleansing")

if __name__ == "__main__":
    main()

