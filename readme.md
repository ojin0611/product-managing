# 디렉토리 세팅중


## crawling.py
### 브랜드 크롤링
1. 해당 브랜드가 api/html/manual중 어디에 속하는지 판단 후 크롤링
2. crawling/brand/npm start(python crawling.py)
3. data/brand/crawling/old.json에 new.json 덮어쓰기(처음이라면 복사)
4. data/brand/crawling/new.json 에 저장

결과 : brand, name, color, volume, type, salePrice, originalPrice, url, image
createAt

### 2가지 크롤링 방식
- cron > 전체 크롤링
- 요청시 > 원하는 브랜드 크롤링


## compare
### 새로 크롤링한 데이터와 기존 데이터 비교
1. data/brand/compare/old.json에 new.json 덮어쓰기(처음이라면 복사)
2. data/brand/crawling/old, new 비교
3. data/brand/compare/new.json에 저장 

결과 : crawling column + status, updateAt

## cleansing
### status 포함된 data 클렌징
1. data/brand/cleansing/old.json에 new.json 덮어쓰기(처음이라면 복사)
2. data/brand/compare/new.json 클렌징!
3. data/brand/cleansing/new.json에 저장

결과 : compare column + SKUid

