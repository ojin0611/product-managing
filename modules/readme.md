# Sku naming
기능 : SKU 단위로 고유 ID를 부여해줌.

* * *

## Input
-  cleansing 완료 된 상품 data (json)
-  기존 sku_dict
    * sku_dict : dictionary, .pickle 형태로 s3에 보관
    * 상품의 brand, name, color, volume, type 을 key 값으로, name id, cvt id를 value 로 저장.
    * 구조 : {('brand', 'name', 'color', 'volume', 'type') : ('name id', 'cvt id'), ...} 
        * cvt = color, volume, type (sku를 구분하는 최소 단위)
* * *

## Process
###  개별 상품 데이터(cleansing data)의 brand, name, color, volume, type 를, 
 기존 sku_dict와 비교
-
#### 상품에 대한 기존 sku id가 cvt 단위까지 존재할 경우
- 기존 sku id 그대로 부여.
#### 상품에 대한 기존 sku id가 brand, name에 대해서만 존재할 경우
- name color volume type 일치하지 않을 경우 -> 단종상품
- name color volume type 일치 할 경우 -> pass

* * *

## Output
- 신규, 변경, 단종 상품에 대한 변경 요청 data
    - 신규 상품 => 등록요청
    - 변경 상품 => 갱신요청
    - 단종 상품 => 갱신요청에 포함, 단종 여부 별도 표시

## output 예시
등록상황(info_status) | 판매상태(sale_status) | 단종여부(discon) | 요청시간(request_time) | 확인시간(confirm_time)
| ------------- | ------------- | ------------- | ------------- |------------- |
등록요청 | 한정판매      | *    | 2018-2-12 / 13:50 | * 
갱신요청 | 품절    | 단종  | 2018-2-12 / 13:50 | * 
에 러    | 세트상품    | *     | 2018-2-12 / 13:50 | *
등록완료 | 할인    | *     | 2018-2-12 / 13:50 | *
##### * 참고 : brand, name, category, color, volume, type, url, image, salePrice, originalPrice 는 cleansing 결과와 동일(생략) 

* * *
- 등록상황(info_status) : 등록 요청 / 갱신 요청 / 에러 / 등록완료
  * 등록요청 : 신규상품(새롭게 확보한 상품 데이터)에 대해 admin에게 등록요청을 한 상태
  * 갱신요청 : 변경상품 확보한 상품 데이터)에 대해 admin에게 정보갱신에 대한 확인을 요청한 상태
  * 등록완료 : admin이 상품 정보 확인 후 등록 요청 / 갱신요청을 등록완료로 변경한 상태
  * 에러 : crawling / cleansing 단계에서 문제가 발생한 경우 (해당 브랜드 제품에 대해 에러 표시)
- 판매 상태(sale_status) : 한정판매/품절/할인/세트상품
  * 한정/품절/할인/세트상품 정보가 없는 경우 default 값 : *
- 단종(discon)
  * 기존에 데이터를 확보해왔었으나, 제품 게시물이 삭제되거나 등의 이유로 정보 갱신이 불가능한 상태
  * 단종이 아닌 경우 default 값 : *
- 요청시간(request_time)
  * 신규상품의 경우, 등록요청이 된 시간
  * 변경상품의 경우, 갱신요청이 된 시간
- 확인시간(comfirm_time)
  * admin이 등록요청 혹은 갱신요청 상태의 상품을 등록완료로 변경한 시간.
  * default 값 : *
- 수정 전 내용 (미정)