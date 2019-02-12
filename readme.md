# 전체 구조

# 2가지 process
- cron > 전체 크롤링>비교>클렌징>DB
- 요청 > 특정 브랜드 크롤링>비교>클렌징>DB


## crawling
[자세히 보기](./crawling)

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
## python 
- urllib, bs4, selenium 활용
- urllib으로 page 정보 request, bs4 이용해서 필요한 데이터 가져옴.
- selenium 사용해야 하는 경우 :
- 1.페이지에 담긴 내용이 바뀌어도 url 주소가 바뀌지 않는 경우
- 2.urllib으로는 제어할 수 없는 JavaScript 요소가 있는 페이지를 다루어야 할 때
- 3.urllib을 통한 접속이 막혀 있는 사이트를 스크래핑 할 때
- => selenium으로 직접 firefox나 chromedriver 을 작동시켜서 데이터를 수집할 수 있으나, 시간이나 안정성 면에서 최대한 사용을 줄이는 것이 좋음.


## js
- 진구님
