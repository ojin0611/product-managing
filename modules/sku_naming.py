import io_module


'''
sku_naming 

1. sku_dict 를 s3에서 불러옴

2. 기존의 sku_dict를 참고하여, 새로운 상품들에 대해 번호를 부여함
    
    2.1. 브랜드명, 상품명, CVT(color, volume, type) 순서로 기존의 sku_dict 에 sku_id가 있는지 체크
    2.2. 없을 경우, 기존의 id 중 마지막 값에 + 1 해서 새로운 값을 부여.
    2.3. 신규상품의 경우, CVT id는 001부터 시작.
    
3. 새로운 상품에 대한 key, value 가 추가된 sku_dict 를 s3에 저장함 
[{"brand": "#", "name": "#", "color": "#","volume": "#", "type": "#",
                   "name_id": "#", "cvt_id": "#"}]
'''


def sku_naming(jsonstring, brand_path):

    sku_dict = io_module.get_sku_json('sku_dict.json', brand_path)

    for product in jsonstring:
        brand = product['brand']
        name = product['name']
        color = product['color']
        volume = product['volume']
        tipe = product['type']
        ncvt = (name, color, volume, tipe)
        sku_name_list = [sku['name'] for sku in sku_dict]
        # sku id 가 있는 경우 == > 원래 있던 skuid를 사용함.
        sku_list = [(sku['name'], sku['color'], sku['volume'], sku['type']) for sku in sku_dict]

        if ncvt in sku_list:
            for sku in sku_dict:
                if sku['name'] == name and sku['color'] == color and sku['volume'] == volume and sku['type'] == tipe:
                    product['skuid'] = product['skuid'] + sku['name_id'] + sku['cvt_id']
                    break
        # sku id 없는 경우 == > name은 존재하는지 판단
        elif name in sku_name_list and ncvt not in sku_list:
            name_id = ""
            for sku in sku_dict:
                if sku['name'] == name:
                    name_id = sku['name_id']
                    break
            cvt_id = int(sorted([sku['cvt_id'] for sku in sku_dict if name == sku['name']])[-1]) + 1
            cvt_id = str(cvt_id).zfill(3)
            new_sku = {"brand": brand, "name": name, "color": color, "volume": volume, "type": tipe,
                       "name_id": name_id, "cvt_id": cvt_id}
            sku_dict.append(new_sku)
            product['skuid'] = product['skuid'] + name_id + cvt_id

        # name이 존재하는 경우, 기존의 name id 가져오고, cvt id 중 가장 큰 값에 + 1 해서 부여해줌.
        elif name not in sku_name_list:
            name_id = int(sorted(sku['name_id'] for sku in sku_dict)[-1]) + 1
            name_id = str(name_id).zfill(6)
            cvt_id = "001"
            new_sku = {"brand": brand, "name": name, "color": color, "volume": volume, "type": tipe,
                       "name_id": name_id, "cvt_id": cvt_id}
            sku_dict.append(new_sku)
            product['skuid'] = product['skuid'] + name_id + cvt_id

    io_module.upload_sku_json(sku_dict, 'sku_dict.json', brand_path)

    return jsonstring
