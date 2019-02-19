# Cleansing Process
## 상세 설명
1. 코스미 상품 정보 등록 양식 + 크롤링된 json 파일 통해 기타 사항 확인 => Excel로 정리 

   공유 링크: https://docs.google.com/spreadsheets/d/1969ZWZeSzIHcqA8Ix1wkBbEPrUR_gltpNMOrOqYeakA/edit?usp=sharing
2. Excel에 정리된 각 항목에 대해 클렌징해야 할 칼럼별 ('brand', 'name', 'volume', 'color', 'type', 'salePrice', 'originalPrice') 
      함수를 cleansing_module.py에 저장
3. 실행시 cleansing_module을 import해 해당 브랜드 클렌징하는 cleansing.py

## 파일 경로
- data/brand/cleansing/old.json에 new.json 덮어쓰기(처음이라면 복사)
- data/brand/crawling/new.json 클렌징!
- data/brand/cleansing/new.json에 저장
- data/cleansing/brandReference.json 취급하는 브랜드 목록

최종 데이터 칼럼 13개: 'brand', 'name', 'category', 'image', 'url', 'color', 'type', 'volume', 'salePrice', 'orignialPrice', 'skuid', 'sale_status', 'eng_name'

## cleansing.py
- input : 최소 'brand', 'name' 칼럼이 포함된 raw json data
- output : 'brand', 'name', 'category', 'image', 'url', 'color', 'type', 'volume', 'salePrice', 'orignialPrice', 'skuid', 'sale_status', 'eng_name' 클렌징된 결과

## cleansing_module.py
- 각 파트의 순서가 중요!
1. cleanseColumn1 : 클렌징해야 할 칼럼이 없을 경우 칼럼을 생성하고 default '#'값을 넣어준다.
2. cleanseBrand : brandReference.json에 없는 취급하지 않는 브랜드 인 상품을 제거하고 skuid의 브랜드 약어 부분을 부여해 준다.
-> 'brand', 'skuid' 를 update
3. cleanseName :
- 자외선 차단지수 형식 통일 [SPF00+ PA+]
- 세트여부 구별 : 대소문자 구분없이 '세트', 'set' 포함시 sale_status = '세트상품' 추가
- 할인여부 구별 : 대소문자 구분없이 '할인', '세일', 'sale' 포함시 sale_status = '할인' 추가 (세트상품일 경우 '세트상품/할인' 형태)
- 불필요한 수식어와 특수기호 제거 : 발견할 때마다 추가해 준다.
- 제품명에 volume이 포함된 경우
 - 괄호 안에 volume이 있는 경우 : 괄호 안에 용량 단위가 있고, volume값 존재하지 않는다면 괄호 안 내용을 volume으로 이동
 - volume이 괄호 없이 있을 경우 : 괄호 밖에 용량 단위가 있고, volume값 존재하지 않는다면 용량단위 앞뒤의 숫자를 volume으로 이동
- 제품명에 type이 포함된 경우 : '대용량', '리필'
- 한글명과 영문명 분리 : 한글이 끝나는 지점에서 분리한 후 분리된 영문명에 포함된 단어와 영문명의 길이를 고려해 잘 분리되었는지 확인
- 남아있는 괄호들 제거
- 공백은 한 칸씩만 남기기
-> 'name', 'volume' ,'type', 'sale_status'(세일상품, 할인, 세일상품/할인, #), 'eng_name' 를 update
4. cleanseVolume
- 영문 소문자 표기
- 용량*개수 또는 용량x개수 형식 통일 : 용량*개수(단위생략)
- 2가지 이상 제품의 용량이 표기된 경우 형식 통일 : + 또는 , 으로 split
- 영어 단위를 한글 단위로 통일
- 용량이 여러 개일 경우 / 로 구분해 주고 ml와 g을 먼저 표기해 준다.
- 용량+단위 단위 사이 공백 제거
-> 'volume' 을 update
5. cleanseColor
- 수식어와 특수문자 제거 : 발견할 때마다 추가해 준다.
- 문자와 숫자는 띄어쓰기로 구분
- 한글 영문 동시 기재시 한글명을 앞에 표기한다.
- 괄호 안 부가설명 있는 경우 제거 혹은 분리해 준다 : '품절'은 제거, 가격변동은 'salePrice', 'originalPrice'에 update
- 남아있는 괄호들 제거
- 공백은 한 칸씩만 남기기
-> 'color', 'salePrice', 'originalPrice' update
6. cleanseType -> cleanseColor과 동일, 'type'을 update
7. cleansePrice
- 브랜드명이 tomford 인 경우 $기호 추가
- 그 외 : 천단위 콤마표기 추가
-> 'salePrice', 'originalPrice' 를 update
8. cleanseColumn2
- 'sale_status' 없다면 추가
