import json
from datetime import datetime
import sys
import os
import io_module
import pickle
from io import BytesIO
import boto3
from botocore.errorfactory import ClientError

# sku naming 에 대한 dictionary를 브랜드 별로 만들어주자
# brand  , product name , volume, type, color
# sku id 목록 저장해놓은거 불러오고.


def sku_naming(jsonstring):

    sku_name_dict = io_module.get_pickle('sku_name_dict.pickle')
    sku_cvt_dict = io_module.get_pickle('sku_cvt_dict.pickle')

    for product in jsonstring:
        brand = product['brand']
        name = (brand, product['name'])
        cvt = (brand, product['name'], product['color'], product['volume'], product['type'])
        # skuid가 있는 경우 == > 원래 있던 skuid를 사용함.:
        if sku_cvt_dict.get(cvt):
            product['skuid'] = product['skuid'] + str(sku_name_dict.get(name)) + str(sku_cvt_dict.get(cvt))

        # skuid 없는 경우 == > skuid를 새로 생성해줌
        else:
            brand_id = product['skuid']
            if name not in sku_name_dict.keys():
                name_id = int(sorted(sku_name_dict.values())[-1]) + 1
                name_id = str(name_id).zfill(6)
                sku_name_dict[name] = name_id
                cvt_id = "001"
                sku_cvt_dict[cvt] = cvt_id
                product['skuid'] = brand_id + name_id + cvt_id

            else:
                name_id = sku_name_dict[name]
                if cvt not in sku_cvt_dict.keys():
                    x = [sku_cvt_dict.get(cvt_key) for cvt_key in sku_cvt_dict.keys() if cvt_key[0] == cvt[0] and cvt_key[1] == cvt[1]]
                    cvt_id = int(sorted(x)[-1]) + 1
                    cvt_id = str(cvt_id).zfill(3)
                    sku_cvt_dict[cvt] = cvt_id
                    product['skuid'] = brand_id + name_id + cvt_id

    io_module.upload_pickle(sku_name_dict, 'sku_name_dict.pickle')
    io_module.upload_pickle(sku_cvt_dict, 'sku_cvt_dict.pickle')

    return jsonstring
