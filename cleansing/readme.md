# Cleansing Process
## 상세 설명
1. 코스미 상품 정보 등록 양식 + 크롤링된 json 파일 통해 기타 사항 확인 => Excel로 정리
2. Excel에 정리된 각 항목에 대한 function 작성 (string변환 + 정규식)
3. function들을 module로 만듦 
  (-> 전처리된 데이터가 원하는 형식에 들어 맞는지 검토하는 정규식도 작성해 확인)
4. 새로 크롤링된 Raw data가 들어오면 module을 import해 클렌징한 후 최종 데이터를 json으로 S3에 저장 

## 파일 경로
- data/brand/cleansing/old.json에 new.json 덮어쓰기(처음이라면 복사)
- data/brand/crawling/new.json 클렌징!
- data/brand/cleansing/new.json에 저장

결과 : cleansing values
