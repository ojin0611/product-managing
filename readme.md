# 전체 구조

## 2가지 process
- cron > 전체 크롤링>비교>클렌징>DB
- 요청 > 특정 브랜드 크롤링>비교>클렌징>DB


## crawling
[자세히 보기](./crawling)

## cleansing
[자세히 보기](./cleansing)


## compare
[자세히 보기](./compare)
데이터 저장 경로
1. data/brand/compare/old.json에 new.json 덮어쓰기(처음이라면 복사)
2. data/brand/cleansing/old, new 비교
3. data/brand/compare/new.json에 저장 



## AWS 연동
- product-managing > EC2로 이동
- data 디렉토리 > S3 디렉토리로 이동
- cleansing 결과 > DynamoDB로 이동


