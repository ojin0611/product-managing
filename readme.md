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



## AWS 연동
- product-managing > EC2로 이동
- data 디렉토리 > S3 디렉토리로 이동
- S3 > compare 최종 결과를 DynamoDB로 push 
- athena로 S3 볼 수 있도록 설정


[Python으로 Bash 명령 실행](https://www.journaldev.com/16140/python-system-command-os-subprocess-call)