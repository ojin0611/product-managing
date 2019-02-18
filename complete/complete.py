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

    new_compare = local_module.load_json("new", brand, "compare")
    old_complete = local_module.load_json("new", brand, "complete")

    new_skuid_list = [new_info['skuid'] for new_info in new_compare]
    new_complete = new_compare + [old_info for old_info in old_complete if old_info['skuid'] not in new_skuid_list]
    for new
    #   io_module.upload_json(new_complete, brand, "complete")
    local_module.save_json(new_complete, brand, "complete")
    print("---- complete 및 결과물 저장완료 -----------")

if __name__ == "__main__":
    main()
