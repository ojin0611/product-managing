import json
import pandas as pd
from pandas.io.json import json_normalize
from pprint import pprint

with open('../data/drjart/cleansing/old.json', encoding="UTF-8") as old_data:
    old_cleansing = json.load(old_data)
    old_df = pd.DataFrame.from_dict(json_normalize(old_cleansing), orient='columns')

with open('../data/drjart/cleansing/new.json', encoding="UTF-8") as new_data:
    new_cleansing = json.load(new_data)
    new_df = pd.DataFrame.from_dict(json_normalize(new_cleansing), orient='columns')

sku_list = ['name', 'color', 'volume', 'type']

old_items = [list(old_dict.values()) for old_dict in old_cleansing]

renew_list = ['url', 'image', 'salePrice', 'originalPrice']

not_changed_data = []
# old data에만 있는 것
old_only = []
# new data에만 있는 것
new_only = []
# --> old_only와 new data 비교 => name, color, volume, type 같으면 renew
# --> 다르면 old_only 에 있는지 new_only 에 있는지 확인 : old_only -> discon, new_only -> newpos
# 갱신되야 하는 것
renew = []
# 판매 상태 : 한정판매/할인중/세트 존재
# 처리 상태(status) :
# 등록요청 (크롤러가 새롭게 가져온 제품에 대해 admin 이 확인하도록 요청)
# 등록검토중(신규 제품에 대해 admin이 확인 중)
# 등록완료(신규 제품에 대해 admin이 카테고리 선택 및 확인완료)
# 에러(코드수정필요) / 크롤러가 데이터 수집 및 처리하는 과정에서 문제가 생긴 상태 (엔지니어 팀에게 수정 요청)
# 수정중(기존 확인) / 고객에게 제품 내용에 대한 수정 요청이 와서 admin이 확인 중인 상태
# -> 제품 url을 통해 확인 해본 결과, 이상 없는 경우 => 등록완료로 다시 전환.
# -> 제품 url을 통해 확인 해본 결과, 크롤러에는 문제가 없으나 정보를 수정할 필요는 있는 경우 => 해당 정보 수정 및 원래 내용을 수정 전 내용에 추가, 등룍완료로 다시 전환.
# -> 제품 url을 통해 확인 해본 결과, 크롤링 자체가 잘못된 경우 -> 에러로 전환 및 엔지니어 팀에게 수정 요청.
# 단종 : 단종된 제품
# 수정 전 내용 : admin이 직접 내용을 바꾸기 전의 크롤러가 확보했던 데이터 

# 단종된 것
discon = []
# 새로 등록 된 것
newpos = []

for new_dict in new_cleansing:
    if new_dict in old_cleansing:
        not_changed_data.append(new_dict)
    else:
        diff_data.append(new_dict)

for old_dict in old_cleansing:
    if old_dict not in new_cleansing:
        diff_data.append(new_dict)


new_posted_list = []

for diff_dic in diff_data:
    if diff_dic['brand'] not in old_brands:
        new_posted_list.append(diff_dic)
    elif diff_dic['category'] not in old_brands:
        new_posted_list.append(diff_dic)
    elif diff_dic['name'] not in old_brands:
        new_posted_list.append(diff_dic)
    elif diff_dic['color'] not in old_brands:
        new_posted_list.append(diff_dic)
    elif diff_dic['volume'] not in old_brands:
        new_posted_list.append(diff_dic)

print(len(old_cleansing))
print(len(new_cleansing))
print(not_changed_data)
print(len(not_changed_data))
print(diff_data)
print(len(diff_data))


#for new_dict in new_cleansing:
#    new_data_set.update(tuple(new_dict.values()))

#print(old_data_set & new_data_set)