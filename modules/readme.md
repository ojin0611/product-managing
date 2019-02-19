# Sku naming
기능 : SKU 단위로 고유 ID를 부여해줌.
- sku id = brand id (알파벳 4글자) + name id (숫자 6자리) + cvt id (숫자 3자리)
- ex) DRJA000000000
* * *

## Input
-  cleansing 완료 된 상품 data (json)
-  기존 sku_dict
    * sku_dict : dictionary, .pickle 형태로 s3에 보관
    * 상품의 brand, name, color, volume, type 을 key 값으로, name id, cvt id를 value 로 저장.
    * 구조 : {('brand', 'name', 'color', 'volume', 'type') : ('name id(6자리)', 'cvt id(3자리)'), ...} 
        * cvt = color, volume, type (sku를 구분하는 최소 단위)
* * *

## Process
####  개별 상품 데이터(cleansing data)의 brand, name, color, volume, type 을 기존 sku_dict와 비교
#### -    상품에 대한 기존 sku id가 cvt id까지 존재할 경우
- 기존 sku id(brand id + name id + cvt id) 부여.
#### -   상품에 대한 name id만 존재할 경우
- name id 는 기존 값을 사용.
- 같은 이름의 상품에 대해, 마지막 cvt id 다음 번호를 부여.
- sku_dict 에 해당 상품과 id 값을 추가.
#### -   상품에 대한 name id, cvt id 모두 존재하지 않을 경우 
- 같은 브랜드의 상품에 대해, 마지막 name id 다음 번호를 부여.
- cvt id 에는 001을 부여.
- sku_dict 에 해당 상품과 id 값을 추가.

* * *
## Output
-  sku id column 에 값이 채워진 상품 데이터.
-  새로운 상품에 대한 key, value 값이 추가된 sku_dict.pickle 을 S3에 업로드