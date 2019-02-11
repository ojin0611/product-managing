# 전체 구조

# 2가지 process
- cron > 전체 크롤링>비교>클렌징>DB
- 요청 > 특정 브랜드 크롤링>비교>클렌징>DB


## crawling
### 브랜드 크롤링
1. 해당 브랜드가 api/html/manual중 어디에 속하는지 판단 후 크롤링
2. data/brand/crawling/old.json에 new.json 덮어쓰기(처음이라면 복사)
3. data/brand/crawling/new.json 에 저장

결과 : brand, name, color, volume, type, salePrice, originalPrice, url, image


## cleansing
### status 포함된 data 클렌징
1. data/brand/cleansing/old.json에 new.json 덮어쓰기(처음이라면 복사)
2. data/brand/crawling/new.json 클렌징!
3. data/brand/cleansing/new.json에 저장

결과 : cleansing values

## compare
### 새로 크롤링한 데이터와 기존 데이터 비교
1. data/brand/compare/old.json에 new.json 덮어쓰기(처음이라면 복사)
2. data/brand/cleansing/old, new 비교
3. data/brand/compare/new.json에 저장 

결과 : cleansing column + status, 정보갱신, SKUid
createAt(신규), updateAt(변동)


## AWS 연동
- product-managing > EC2로 이동
- data 디렉토리 > S3 디렉토리로 이동
- cleansing 결과 > DynamoDB로 이동


# 크롤링방법
## python - 어떤 모듈?
- urllib > 정빈 정리
- selenium > 영진

## js
- 진구님