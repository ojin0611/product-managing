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

sku_list = ['name', 'color', 'volume']

old_items = [list(old_dict.values()) for old_dict in old_cleansing]

renew_list = ['url', 'image', 'salePrice', 'originalPrice']

not_changed_data = []
diff_data = []
for new_dict in new_cleansing:
    if new_dict in old_cleansing:
        not_changed_data.append(new_dict)
    else:
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