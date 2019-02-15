# 1. 너가 해야할일 :
# compare 결과로 만들어진 요청서에, 신규 제품을 sku id 부여해서 (brand->productname->)  complete 결과로 만들어진 json에 추가.
#
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
sku_id_dict = load_json(sku_id_json)

# 여기에 brand 없으면? 브랜드 sku id 추가 , 뒤에껀 000000 000 부터 시작
#
sku_id_dict['brand'] =