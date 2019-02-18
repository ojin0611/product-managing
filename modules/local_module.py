import json
from datetime import datetime
import sys
import os


def load_json(time, brand, activity):

    # time : new / old 중 선택
    # brand : 브랜드명
    # activity : "crawling" / "cleansing" / "compare" 중 선택
    file_path = '../data/' + brand + '/' + activity + '/' + time + '.json'
    with open(file_path, encoding="UTF-8") as json_data:
        print('--- load file from',file_path,'---')
        result_json = json.load(json_data)

    return result_json


def save_json(jsonstring, brand, activity):

    # jsonstring : 저장할 json 파일
    # brand : 브랜드명
    # activity : crawling / cleansing / compare 중 선택.
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    file_time = '%s-%s-%s-%s-%s-%s' % (year.zfill(4), month.zfill(2), day.zfill(2),
                                       hour.zfill(2), minute.zfill(2), second.zfill(2))
    output_path = '../data/' + brand + '/' + activity + '/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    new_file = output_path + 'new.json'
    old_file = output_path + 'old.json'
    history_path = output_path + 'history/'
    history_file = history_path + file_time + ".json"

    if not os.path.exists(history_path):
        os.makedirs(history_path)
    # 기존 new file 덮어쓰기
    if os.path.isfile(new_file):
        # old file 존재 시 삭제 후 덮어쓰기
        if os.path.isfile(old_file):
            os.remove(old_file)
        os.rename(new_file, old_file)
    else:
        empty_json = [{"name": "", "url": "", "image": "", "color": "", "category": "",
                       "salePrice": "", "originalPrice": "", "brand": "", "volume": "", "type": "", "skuid": "dummy"}]
        empty_output = json.dumps(empty_json, ensure_ascii=False, indent='\t')
        with open(old_file, 'w', encoding='UTF-8') as file:
            file.write(empty_output)
        print('empty_output file saved')
    output = json.dumps(jsonstring, ensure_ascii=False, indent='\t')

    print('--- save file to',output_path,'---')
    with open(new_file, 'w', encoding='UTF-8') as file:
        file.write(output)
    with open(history_file, 'w', encoding='UTF-8') as file:
        file.write(output)


def putIntoDynamoDB():
    pass