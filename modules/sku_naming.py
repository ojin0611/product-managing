import io_module


'''
sku_naming 

1. sku_dict 를 s3에서 불러옴

2. 기존의 sku_dict를 참고하여, 새로운 상품들에 대해 번호를 부여함
    
    2.1. 브랜드명, 상품명, CVT(color, volume, type) 순서로 기존의 sku_dict 에 sku_id가 있는지 체크
    2.2. 없을 경우, 기존의 id 중 마지막 값에 + 1 해서 새로운 값을 부여.
    2.3. 신규상품의 경우, CVT id는 001부터 시작.
    
3. 새로운 상품에 대한 key, value 가 추가된 sku_dict 를 s3에 저장함 

'''


def sku_naming(jsonstring, brand):

    sku_json = io_module.get_pickle('sku_dict.json', brand)
    sku_dict = {}

    for content in sku_json:
        sku_dict = content
        break

    for product in jsonstring:
        bncvt = (product['brand'], product['name'], product['color'], product['volume'], product['type'])
        # sku id 가 있는 경우 == > 원래 있던 skuid를 사용함.
        if sku_dict.get(bncvt):
            product['skuid'] = product['skuid'] + sku_dict.get(bncvt)[0] + sku_dict.get(bncvt)[1]

        # sku id 없는 경우 == > name은 존재하는지 판단
        else:
            brand_id = product['skuid']
            if bncvt[1] not in [key[1] for key in sku_dict.keys()]:
                name_id = int(sorted([value[0] for value in sku_dict.values()])[-1]) + 1
                name_id = str(name_id).zfill(6)
                sku_dict[bncvt] = (name_id, "001")
                product['skuid'] = brand_id + name_id + "001"
            # name이 존재하는 경우, 기존의 name id 가져오고, cvt id 중 가장 큰 값에 + 1 해서 부여해줌.
            else:
                name_id = ""
                for key in sku_dict.keys():
                    if key[0] == bncvt[0] and key[1] == bncvt[1]:
                        name_id = sku_dict.get(key)[0]
                        break
                x = [sku_dict.get(cvt_key)[1] for cvt_key in sku_dict.keys()
                     if cvt_key[0] == bncvt[0] and cvt_key[1] == bncvt[1]]
                cvt_id = int(sorted(x)[-1]) + 1
                cvt_id = str(cvt_id).zfill(3)
                sku_dict[bncvt] = (name_id, cvt_id)
                product['skuid'] = brand_id + name_id + cvt_id

    io_module.upload_pickle(sku_dict, 'sku_dict.json', brand)

    return [jsonstring]
