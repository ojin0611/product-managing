# crawling
## 파일 설명
- brand : 해당 브랜드 crawler (홈페이지 링크가 주어지면 상품파일 json을 입력하는 함수) 저장
- crawling_module.py : system, 저장 위치 등에 따라 유동적으로 변경할 수 있도록!
- brandlist.json : 각 브랜드가 어떤 방식으로 크롤링됐는지 기록 (ts, js, python, manual)
- crawling list : https://docs.google.com/spreadsheets/d/1xQvezndG9q9OYohG3FUXVOBo72X-tll46cmgsQIwSR4/edit?usp=sharing

## Output
- column : brand, name, color, volume, type, salePrice, originalPrice, url, image
- SKU 단위로 상품 저장!
- data/brand/crawling/old.json 삭제 후 기존 new.json 이름 변경 (처음이라면 생성)
- data/brand/crawling/new.json 에 저장

## column 정의
1. brand (text)
    - 직접 채움. default = 영어
2. name (text)
    - 브랜드명 섞여있으면 제거
3. category (text) - 사이트 기준
    - ex) 메이크업 > 포인트 메이크업 > 립 
4. color (text)
5. volume (text)
6. type (text) 색상,용량 제외 모든 옵션
7. image (list-url)
    - 메인이미지들 + 옵션별 이미지들
8. originalPrice (int)
    - 가격이 1개라면 우선적으로 채운다. 
9. salePrice (int)
10. url (text)



## Crawler Guide - python
- urllib
- selenium
- bs4

```python
from crawling_module import *
import otherModules # bs4, urlopen, selenium, json, ...
def main():
    def getCategoryList():
        return categoryList
    def getItemList():
        return itemList
    def getItem(itemURL):
        return items

    path = path_chromedriver()

    read(siteHomeURL)
    categoryList = getCategoryList() # category urls (or clickable object)
    result = []
    for category in categoryList:
        read(category)
        clickSeeMoreButton() # or next page.
        itemList = getItemList() # item urls
        for itemURL in itemList:
            result += getItem(itemURL)

    writeJSON(result) # def writeJSON(jsonString) 
```

