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
    now = datetime.now()
    request_time = '%s-%s-%s / %s:%s' % (now.year, now.month, now.day, now.hour, now.minute)

#    new_cleansing = io_module.get_json("new", brand, "cleansing")
#    old_cleansing = io_module.get_json("old", brand, "cleansing")
    new_cleansing = local_module.load_json("new", brand, "cleansing")
    old_cleansing = local_module.load_json("old", brand, "cleansing")

    # --> old와 new data 비교 => name, color, volume, type 같으면 renew
    # --> 다르면 old 에 있는지 new에 있는지 확인 : old_only -> discon, new_only -> newpos
    # 갱신되야 하는 것
    renew = []
    # 단종된 것
    discon = []
    # 새로 등록 된 것
    new_pos = []

    for new_dict in new_cleansing:
        if new_dict not in old_cleansing:
            for old_dict in old_cleansing:
                if new_dict['brand'] == old_dict['brand'] and new_dict['name'] == old_dict['name'] and new_dict['color'] == old_dict['color'] and new_dict['volume'] == old_dict['volume'] and new_dict['type'] == old_dict['type']:
                    new_dict['info_status'] = "갱신요청" # sku 단위는 변화없으나, 부수 항목(price, image, url, sale_status 만 변한 상태
                    new_dict['discon'] = "#" # 단종이 아님
                    new_dict['request_time'] = request_time
                    new_dict['sale_status'] = "#"
                    new_dict['confirm_time'] = "*"
                    renew.append(new_dict)
                    break
                else:
                    new_dict['info_status'] = "등록요청"
                    new_dict['discon'] = "#" # 단종이 아님
                    new_dict['request_time'] = request_time
                    new_dict['sale_status'] = "#"
                    new_dict['confirm_time'] = "*"
                    new_pos.append(new_dict)
                    break

    for old_dict in old_cleansing:
        if old_dict not in new_cleansing:
            for new_dict in new_cleansing:
                if new_dict['brand'] == old_dict['brand'] and new_dict['name'] == old_dict['name'] and new_dict['color'] == old_dict['color'] and new_dict['volume'] == old_dict['volume'] and new_dict['type'] == old_dict['type']:
                    before_renew.append(new_dict) # just for check
                    pass
                else:
                    old_dict['info_status'] = "갱신요청"
                    old_dict['discon'] = "단종" # 공식 사이트에서 더 이상 그 제품을 찾을 수 없는 경우를 의미.
                    old_dict['request_time'] = request_time
                    old_dict['sale_status'] = "#"
                    old_dict['confirm_time'] = "*"
                    discon.append(old_dict)
                    break

    result_json = renew + new_pos + discon
    # just for check
    # print(result_json)
    sku_tagged_json = sku_naming.sku_naming(result_json)
#    io_module.upload_json(sku_tagged_json, brand, "compare")
    local_module.save_json(sku_tagged_json, brand, "compare")
    print("---- compare 및 결과물 저장완료 -----------")
    #   io_module.upload_json(sku_tagged_json, brand, "complete")
    local_module.save_json(sku_tagged_json, brand, "complete")


if __name__ == "__main__":
    main()
