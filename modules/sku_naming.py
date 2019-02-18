import json
from datetime import datetime
import sys
import os
import io_module
import pickle
import pprint

# Youngjin Yang [9:12 PM]
# check) 첫 compare 결과 default old.json column에 status 추가할지말지 고민해보기!
#
# Youngjin Yang [9:37 PM]
# +)
# compare.py에 0 0 대신
# 이해할수있는, 유의미한 문장 출력!


# sku naming 에 대한 dictionary를 브랜드 별로 만들어주자
# brand  , product name , volume, type, color
# sku id 목록 저장해놓은거 불러오고.



def sku_naming(jsonstring):

#    with open('sku_brand_dict.pickle', 'rb') as f:
#        sku_brand_dict = pickle.load(f)
#    with open('sku_name_dict.pickle', 'rb') as f:
#        sku_name_dict = pickle.load(f)
#    with open('sku_name_dict.pickle', 'rb') as f:
#        sku_cvt_dict = pickle.load(f)

    sku_brand_dict = {'clio': "clio"}
    sku_name_dict = {('clio', ''): str(000000)}
    sku_cvt_dict = {('clio', '', '', '', ''): str(000)}

    pprint.pprint(sku_brand_dict)
    pprint.pprint(sku_name_dict)


    for product in jsonstring:
        brand = product['brand']
        name = (brand, product['name'])
        cvt = (brand, product['name'], product['color'], product['volume'], product['type'])
        # 등록요청인 경우
        if product['info_status'] == "등록요청":
            brand_id = product['skuid']
            if name not in sku_name_dict.keys():
                name_id = int(sorted(sku_name_dict.values())[-1]) + 1
                name_id = str(name_id).zfill(6)
                sku_name_dict[name] = name_id
                cvt_id = str("001")
                sku_cvt_dict[cvt] = cvt_id
            else:
                name_id = sku_name_dict[name]
                if cvt not in sku_cvt_dict.keys():
                    x = [sku_cvt_dict.get(cvt_key) for cvt_key in sku_cvt_dict.keys() if cvt_key[0] == cvt[0] and cvt_key[1] == cvt[1]]
                    cvt_id = int(sorted(x)[-1]) + 1
                    cvt_id = str(cvt_id).zfill(3)
                    sku_cvt_dict[cvt] = cvt_id

            product['skuid'] = brand_id + name_id + cvt_id
            print("new_skuid_created : " + product['skuid'])

        elif product['info_status'] == "갱신요청":
            if sku_brand_dict.get(name):
                product['skuid'] = product['skuid'] + str(sku_name_dict.get(name)) + str(sku_cvt_dict.get(cvt))
            else:
                product.clear()

    with open('sku_brand_dict.pickle', 'wb') as f:
        pickle.dump(sku_brand_dict, f, pickle.HIGHEST_PROTOCOL)

    with open('sku_name_dict.pickle', 'wb') as f:
        pickle.dump(sku_name_dict, f, pickle.HIGHEST_PROTOCOL)

    with open('sku_cvt_dict.pickle', 'wb') as f:
        pickle.dump(sku_name_dict, f, pickle.HIGHEST_PROTOCOL)

    return jsonstring
