# Compare 

## Input
-  cleansing 완료 된 브랜드(사이트)별 json data (old, new) 

## 비교 기준
- 개별 제품 dictionary 일치 여부

## Output
- new 에는 없고 old 에만 있는 목록(단종 목록)
- new 에는 있고 old 에만 없는 목록(신규 목록)
- new 에도 있고 old 에도 있지만 일부 정보가 달라진 목록(갱신 목록)
- 나머지 품목들은 업데이트가 안된 품목.