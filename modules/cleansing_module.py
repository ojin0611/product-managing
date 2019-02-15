# 브랜드명 클렌징 + 취급안하는 브랜드 제거 + sku_id의 브랜드명 약어 부여
def cleanseBrand(jsonString):
    
    brand = jsonString.get('brand')
    brandList = list(ref.get('영문명').values()) # 취급 브랜드의 영문명 리스트
    abbList = list(ref.get('약어').values()) # 브랜드 약어 리스트
    
    p = re.compile(r'\s+') #띄어쓰기 없음
    brand = re.sub(p, '',brand) 
    brand = brand.upper() #영문 대문자 표기
    
    if brand not in brandList:
        return None
    
    # skuID 브랜드 약어 부분 부여
    else:
        idx = brandList.index(brand)
        skuid = abbList[idx]
        result = dict(jsonString, **{'brand': brand, 'skuid': skuid})
    
        return result



def cleanseName(jsonString):
    
    name = jsonString.get('name')
    
    # 1. 불필요한 수식어와 특수기호 제거 -> 별표사이사이에 있는 문구 삭제? ex)★~가 추천한 상품★
    p = re.compile(r'리미티드|한정|한정판|행사|1+1|1 + 1|[리미티드]|★|☆|추천|!|@|^|new', re.I) # * () [] / , . ' _ 제외 특수기호 ? \W
    name = p.sub(' ', name)
    
    # 2. [SPF00+ PA+] 형식으로 통일
    #p = re.compile(r'(.^spf)(\d)([+]*).*(pa)([+]$.)', re.I)
    #name = p.sub(r'[SPF\2\3 PA\5]', name)
    p = re.compile(r'spf|pa', re.I)
    #if p.search(name):
    #    name = p.sub(r'', name)
    
    # 3. 세트 여부 구별 -> 세트로 구분되지 않은 상품 존재할 수 있음
    
    p = re.compile('set|세트', re.I)  # 컬렉션 / 박스 / 0종 / 키트 / 듀오 / 트리오 -> 세트 상품이 아닐 가능성 있음. 대부분이 세트로 걸러지긴 함-> 세트 표기가 더 나은지
    if p.search(name):
        sale_status = '세트'
    else:
        sale_status = '*'
    
    # 4. 한글명과 영문명 분리
    p = re.compile(r'(.*[가-힣])\s([a-zA-Z].*)')
    if p.search(name):
        name = p.sub(r'\1', name)
        en_name = p.sub(r'\2', name)
    else:
        en_name = '*'
        
    # 5. 한 칸 이상의 공백 제거
    p = re.compile(r'\s+')
    name = p.sub(' ', name)

    result =  dict(jsonString, **{'name': name, 'sale_status': sale_status, 'en_name': en_name})
    
    return result


def cleanseVolume(jsonString):
    
    volume = jsonString.get('volume')
    
    # 1. 영문 소문자 표기
    volume = str(volume).lower()
    
    # 2. 용량과 단위 사이 띄어쓰기 없음
    p = re.compile(r'(\d)\s+([가-힣a-zA-Z])')
    volume = p.sub(r'\1\2', volume)

   #3. 용량 여러개 경우 / 로 구분
    p = re.compile(r'([가-힣a-zA-Z])\s*(\d.)')
    volume = p.sub(r'\1/\2', volume)
    
    #4. 용량*개수 경우 뒷 단위 제거 / 용량x개수로 표기된 경우도 존재!
    p1 = re.compile(r'([*].\d+).*[가-힣a-zA-Z]')
    volume = p1.sub(r'\1', volume)
    p2 = re.compile(r'([x].\d+).*[가-힣a-zA-Z]', re.I)
    volume = p2.sub(r'\1', volume)
    
    #5. bottle/spray/pat 등 용량 앞에 수식어 붙는 경우 + 단위가 pieces 같은 영어일 경우
    p = re.compile('pieces|piece', re.I)
    volume = p.sub('개', volume)

    #6 제품과 용량 모두 2가지 이상인 경우 [용량, 용량] or [용량(종류), 용량(종류)]   

    #7 제품 종류 2가지 이상이지만 용량 동일 경우 [용량*갯수(종류1/종류2/...)]

    #8 단위 여러개인 경우 ml과 g 우선 (oz 후순위)
    
    result =  dict(jsonString, **{'volume': volume})
    
    return result


def cleanseColor(jsonString):
    
    color = jsonString.get('color')
    
    #1-1 특수문자/수식어 하나하나 따로 제거할 경우..
    p = re.compile(r'new|추천|\W', re.I) # 제거하고 싶은 단어 추가
    color = p.sub(' ', color) # space 한 칸 줘야 한글끼리, 영어끼리 띄어쓰기가 유지됨. 하지만 필요 이상의 공백이 생길 수 있으므로 한칸 이상 공백 제거하는 식 필요
    
    #2 문자와 숫자는 띄어쓰기로 구분  -> 'A01 레드' 경우 ? 
    p1 = re.compile(r'([가-힣a-zA-Z]+)(\S\d+)') # 문자+숫자 사이 띄어쓰기
    color = p1.sub(r'\1 \2', color)
    p2 = re.compile(r'(\d+)(\S[가-힣a-zA-Z]+)') # 숫자+문자 사이 띄어쓰기
    color = p2.sub(r'\1 \2', color)

    #3 한글 영문 동시 기재시 한글을 앞으로
    p = re.compile('([a-zA-Z]+.*?)([가-힣]+)')
    color = p.sub(r'\2 \1', color)
    
    # 괄호 안 부가설명 있을 경우
    
    # 한 칸 이상의 공백은 제거
    p = re.compile(r'\s+')
    color = p.sub(' ', color)
    
    result =  dict(jsonString, **{'color': color})
    
    return result


# 원화/달러/유료 표기
# price는 무조건 numeric이라 가정

def cleansePrice(jsonString):
    brand = jsonString.get('brand')
    saleprice = jsonString.get('salePrice')
    originalprice = jsonString.get('originalPrice')
    
    # thousand separator
    if brand == 'tomford' or brand == 'TOMFORD':
        # 달러 기호 포함
        p = re.compile(r'\D')
        saleprice = p.sub('', saleprice)
        originalprice = p.sub('', originalprice)
        saleprice = '$' + '{:,}'.format(int(saleprice))
        originalprice = '$' + '{:,}'.format(int(originalprice))
    else:
        saleprice = '{:,}'.format(int(saleprice))
        originalprice = '{:,}'.format(int(originalprice))
        
    result =  dict(jsonString, **{'salePrice': saleprice, 'originalPrice': originalprice})
    
    return result