import json
from datetime import datetime
import sys
import os
sys.path.append("../modules")
import io_module
import sku_naming
import local_module
import pprint

def main():
    brand = sys.argv[1]

    new_compare = io_module.get_json("new", brand, "compare")

    try:
        old_complete = io_module.get_json("new", brand, "complete")
    except:
        old_complete = [{"name": "#", "url": "#", "image": "#", "color": "#", "category": "#", "salePrice": "#",
                       "originalPrice": "#", "brand": "#", "volume": "#", "type": "#", "skuid": "#"}]

    new_skuid_list = [new_info['skuid'] for new_info in new_compare]
    new_complete = new_compare + [old_info for old_info in old_complete if old_info['skuid'] not in new_skuid_list]
    io_module.upload_json(new_complete, brand, "complete")
    print("---- complete 및 결과물 저장완료 -----------")

if __name__ == "__main__":
    main()
