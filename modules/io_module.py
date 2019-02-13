import json
from datetime import datetime
import sys
import os


def load_json(time, brand, activity):

    # time : new / old 중 선택
    # brand : 브랜드명
    # activity : crawling / cleansing / compare 중 선택
    file_path = '../data/' + brand + '/' + activity + '/' + time + '.json'
    with open(file_path, encoding="UTF-8") as json_data:
        result_json = json.load(json_data)

    return result_json


def save_json(jsonstring, brand, activity):

    # jsonstring : 저장할 json 파일
    # brand : 브랜드명
    # activity : crawling / cleansing / compare 중 선택.
    now = datetime.now()
    file_time = '%sy-%sm-%sd-%sh' % (now.year, now.month, now.day, now.hour)

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

    output = json.dumps(jsonstring, ensure_ascii=False, indent='\t')



    with open(new_file, 'w', encoding='UTF-8') as file:
        file.write(output)
    with open(history_file, 'w', encoding='UTF-8') as file:
        file.write(output)
