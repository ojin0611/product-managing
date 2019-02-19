import json
from datetime import datetime
import sys
import os
sys.path.append("../modules")
import io_module


def main():
    brand = sys.argv[1]
    now = datetime.now()
    request_time = '%s-%s-%s / %s:%s' % (now.year, now.month, now.day, now.hour, now.minute)

    # 새로 클린징완료 된 파일과 직전에 클린징 되었던 파일을 가져옴.
    new_cleansing = io_module.get_json("new", brand, "cleansing")
    old_cleansing = io_module.get_json("old", brand, "cleansing")

    result_json = []

    for new_dict in new_cleansing:
        if new_dict not in old_cleansing:
            for old_dict in old_cleansing:
                if new_dict['skuid'] == old_dict['skuid']:
                    new_dict['info_status'] = "갱신요청" # sku 단위는 변화없으나, 부수 항목(price, image, url, sale_status 만 변한 상태
                    new_dict['discon'] = "#" # 단종이 아님
                    new_dict['request_time'] = request_time
                    new_dict['sale_status'] = "#"
                    new_dict['confirm_time'] = "*"
                    result_json.append(new_dict)
                    break
                else:
                    new_dict['info_status'] = "등록요청"
                    new_dict['discon'] = "#" # 단종이 아님
                    new_dict['request_time'] = request_time
                    new_dict['sale_status'] = "#"
                    new_dict['confirm_time'] = "*"
                    result_json.append(new_dict)
                    break

    for old_dict in old_cleansing:
        if old_dict not in new_cleansing:
            for new_dict in new_cleansing:
                if new_dict['skuid'] == old_dict['skuid']:
                    pass
                else:
                    old_dict['info_status'] = "갱신요청"
                    old_dict['discon'] = "단종" # 공식 사이트에서 더 이상 그 제품을 찾을 수 없는 경우를 의미.
                    old_dict['request_time'] = request_time
                    old_dict['sale_status'] = "#"
                    old_dict['confirm_time'] = "*"
                    result_json.append(old_dict)
                    break

    io_module.upload_json(result_json, brand, "compare")
    print("---- compare 및 결과물 저장완료 -----------")


if __name__ == "__main__":
    main()
