import json
from datetime import datetime
import sys
import os



def compare(brand):
    now = datetime.now()
    request_time = '%sy_%sm_%sd_%sh_%sm' % ( now.year, now.month, now.day, now.hour, now.minute )

    old_path = '../data/' + brand + '/cleansing/old.json'
    with open(old_path, encoding="UTF-8") as old_data:
        old_cleansing = json.load(old_data)

    new_path = '../data/' + brand + '/cleansing/new.json'
    with open('../data/drjart/cleansing/new.json', encoding="UTF-8") as new_data:
        new_cleansing = json.load(new_data)

    #sku_attributes = ['brand', 'name', 'color', 'volume', 'type']

    #renew_attributes = ['url', 'image', 'salePrice', 'originalPrice']

    # old data에만 있는 것
    old_only = []
    # new data에만 있는 것
    new_only = []
    # --> old_only와 new data 비교 => name, color, volume, type 같으면 renew
    # --> 다르면 old_only 에 있는지 new_only 에 있는지 확인 : old_only -> discon, new_only -> newpos
    # 갱신되야 하는 것
    renew = []
    before_renew = []
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

# just for check, if below two line not equal zero, check the code above
    print(len(old_cleansing) - len(new_cleansing) + len(new_pos) - len(discon) + len(renew))
    print(len(renew) - len(before_renew))

    result_json = renew + new_pos + discon
# just for check
# print(result_json) 

    output_path = '../data/' + brand + '/compare/'
    history_path = output_path + 'history/'
    # 경로 없으면 디렉토리 생성
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not os.path.exists(history_path):
        os.makedirs(history_path)
        
    new_file = output_path + 'new.json'
    old_file = output_path + 'old.json'
    history_file = history_path + request_time + ".json"

    # 기존 new file 덮어쓰기
    if os.path.isfile(new_file):
        # old file 존재 시 삭제 후 덮어쓰기
        if os.path.isfile(old_file):
            os.remove(old_file)
        os.rename(new_file, old_file)
        
    output = json.dumps(result_json,ensure_ascii=False, indent='\t')

    with open(new_file,'w',encoding='UTF-8') as file:
        file.write(output)

    with open(history_file, 'w', encoding='UTF-8') as file:
        file.write(output)

if __name__ == "__main__":
    if sys.argv[1] is not None:
        brand = sys.argv[1]
        compare(brand)
