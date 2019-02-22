import io_module

# sku naming 에 대한 dictionary를 브랜드 별로 만들어주자
# brand  , product name , volume, type, color
# sku id 목록 저장해놓은거 불러오고.


def sku_naming(jsonstring, brand):

    sku_dict = io_module.get_pickle('sku_dict.pickle', brand)

    for product in jsonstring:
        cvt = (product['brand'], product['name'], product['color'], product['volume'], product['type'])
        # skuid가 있는 경우 == > 원래 있던 skuid를 사용함.
        if sku_dict.get(cvt):
            product['skuid'] = product['skuid'] + sku_dict.get(cvt)[0] + sku_dict.get(cvt)[1]

        # skuid 없는 경우 == > name은 존재하는지 판단
        else:
            brand_id = product['skuid']
            if cvt[1] not in [key[1] for key in sku_dict.keys()]:
                name_id = int(sorted([value[0] for value in sku_dict.values()])[-1]) + 1
                name_id = str(name_id).zfill(6)
                sku_dict[cvt] = (name_id, "001")
                product['skuid'] = brand_id + name_id + "001"
            # name이 존재하는 경우, 기존의 name id 가져오고, cvt id 중 가장 큰 값에 + 1 해서 부여해줌.
            else:
                #
                name_id = ""
                for key in sku_dict.keys():
                    if key[0] == cvt[0] and key[1] == cvt[1]:
                        name_id = sku_dict.get(key)[0]
                        break
                x = [sku_dict.get(cvt_key)[1] for cvt_key in sku_dict.keys()
                     if cvt_key[0] == cvt[0] and cvt_key[1] == cvt[1]]
                cvt_id = int(sorted(x)[-1]) + 1
                cvt_id = str(cvt_id).zfill(3)
                sku_dict[cvt] = (name_id, cvt_id)
                product['skuid'] = brand_id + name_id + cvt_id

    io_module.upload_pickle(sku_dict, 'sku_dict.pickle', brand)

    return jsonstring
