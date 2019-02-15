# Cleansing Process
## 상세 설명
1. 코스미 상품 정보 등록 양식 + 크롤링된 json 파일 통해 기타 사항 확인 => Excel로 정리
2. Excel에 정리된 각 항목에 대한 function 작성 (string변환 + 정규식)
  공유 링크:  https://docs.google.com/spreadsheets/d/1969ZWZeSzIHcqA8Ix1wkBbEPrUR_gltpNMOrOqYeakA/edit?usp=sharing

3. cleansing_module.py에 함수들 저장
4. 실행시 cleansing_module을 import해 해당 브랜드 클렌징하는 cleansing.py 작성

## 파일 경로
- data/brand/cleansing/old.json에 new.json 덮어쓰기(처음이라면 복사)
- data/brand/crawling/new.json 클렌징!
- data/brand/cleansing/new.json에 저장

결과 : cleansing values

