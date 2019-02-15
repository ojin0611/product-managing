import pandas as pd
import json

# 상품데이터 Master로 부터 브랜드 json파일로 따로 저장
brandRef= pd.read_excel('C:/Users/TRILLIONAIRE/Downloads/상품데이터 Master.xlsx', sheet_name = '브랜드') 
brandRef[['한글명','영문명','약어']].to_json('brandReference.json')