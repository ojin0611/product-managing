import json
from datetime import datetime
import os
import sys
import re

sys.path.append("../modules")
import io_module
from cleansing_module import *


def main():
    brand = sys.argv[1]
    print('cleansing.py start')
    crawled_data = io_module.get_json("new", brand, "crawling")
    # clean the crawled_data 
    cleansed_data = list(map(cleanseColumns1, crawled_data))
    cleansed_data = list(map(cleanseBrand, cleansed_data))
    cleansed_data = list(filter(None, cleansed_data))   # 취급하지 않는 브랜드의 경우 None값을 return -> filter
    cleansed_data = list(map(cleanseName, cleansed_data))
    cleansed_data = list(map(cleanseVolume, cleansed_data))
    cleansed_data = list(map(cleanseColor, cleansed_data))
    cleansed_data = list(map(cleanseType, cleansed_data))
    cleansed_data = list(map(cleansePrice, cleansed_data))
    cleansed_data = list(map(cleanseColumns2, cleansed_data))
    output = cleansed_data
    # save output as json
    io_module.upload_json(output, brand, "cleansing")

if __name__ == "__main__":
    main()

