#%%
import json
import re

global ref

#%%
def cleanseColumnNames(jsonString):
    
    # color로투터 type, volume 분리하는 것이 더 편하기 때문에 'option'은 'color'로 변경
    colName = {
        'beforeOnlineSalePrice':'originalPrice', 
        'originalPrice':'originalPrice',
        'salePrice':'salePrice',
        'brand':'brand',
        'brandName':'brand', 
        'category':'category', 
        'color':'color',
        'colorname':'color',
        'finalOnlinePrice':'salePrice',
        'image':'image',
        'mainName':'name',
        'name':'name',
        'type':'type',
        'url':'url',
        'volume':'volume',
        'price' : 'originalPrice',
        'option' : 'color',
        'originalName': 'delete',
        'notes': 'delete',
        'prodId': 'delete',
        'rootCategory': 'delete',
        'subCategory': 'delete',
        'subName': 'type',
        'companyOfManufacturer': 'delete',
        'countryOfManufacturer': 'delete',
        'expirationDate': 'delete',
        'id': 'delete',
        'ingredient': 'delete',
        'specifications': 'delete',
        'functionalCosmetics': 'delete',
        'limited': 'delete'
    }
    
    jsonString = dict((colName[key], value) for (key, value) in jsonString.items())

    return jsonString

#%%
# 크롤링되지 않은 칼럼이 존재할 수 있음 + API로 가져온 브랜드의 데이터 칼럼 통일
def cleanseColumns1(jsonString):
    
    columnList = jsonString.keys()
    if 'category' not in columnList:
        jsonString = dict(jsonString, **{'category':'#'})
    if 'color' not in columnList:
        jsonString = dict(jsonString, **{'color':'#'})
    if 'type' not in columnList:
        jsonString = dict(jsonString, **{'type':'#'})
    if 'volume' not in columnList:
        jsonString = dict(jsonString, **{'volume':'#'})
    if 'salePrice' not in columnList:
        jsonString = dict(jsonString, **{'salePrice':'#'})
    if 'originalPrice' not in columnList:
        jsonString = dict(jsonString, **{'originalPrice':'#'})
    # dummy 'delete'칼럼 추가 : 'delete' key가 하나도 없을 경우 후에 전체 데이터가 필터링됨
    if 'delete' not in columnList:
        jsonString = dict(jsonString, **{'delete':'#'})

    return jsonString

#%%
# 한글명 -> 영어로
# 브랜드명 클렌징 + 취급안하는 브랜드 제거 + skuid의 브랜드명 약어 부여
def cleanseBrand(jsonString):
    
    with open('./brandReference.json', encoding="UTF-8") as json_data: 
        ref = json.load(json_data)
  
    brand = jsonString.get('brand')
    brandList = list(ref.get('영문명').values()) # 취급 브랜드의 영문명 리스트
    korBrandList = list(ref.get('한글명').values())
    abbList = list(ref.get('약어').values()) # 브랜드 약어 리스트
    
    p = re.compile(r'\s+') #띄어쓰기 없음
    brand = re.sub(p, '',brand) 
    brand = brand.upper()

    # 브랜드명이 한글명일 경우 (API) 영문명으로 바꿔줌
    if brand in korBrandList:
        idx = korBrandList.index(brand)
        newBrand = brandList[idx]
        brand = newBrand

    # 취급하지 않는 브랜드의 상품 제거
    if brand not in brandList:
        return None
    # skuid 브랜드 약어 부분 부여
    else:
        brand = brand.upper() #영문 대문자 표기
        idx = brandList.index(brand)
        skuid = abbList[idx]
        result = dict(jsonString, **{'brand': brand, 'skuid': skuid})
    
        return result

#%%
def cleanseImage(jsonString):
    images = jsonString.get('image')
    if type(images) != type(['a']):
        imageList=[]
        images = images.split(',')
        for image in images:
            imageList.append(image)
        image = imageList
    else:
        image = images
    result = dict(jsonString, **{'image' : image})
    return result

#%%
# 각 내용 순서도 중요!
def cleanseName(jsonString):
    
    name = jsonString.get('name')
    volume = jsonString.get('volume')
    types = jsonString.get('type')

    # SPF00+ PA+ 형식으로 통일
    #p = re.compile(r'(.^spf)(\d)([+]*).*(pa)([+]$.)', re.I)
    #name = p.sub(r'[SPF\2\3 PA\5]', name)
    p = re.compile(r'spf', re.I)
    if p.search(name):
        p2 = re.compile(r'pa', re.I)
        if p2.search(name):
            p = re.compile(r'spf\s?(\d+)\s?([+]*)(.*)pa\s?([+]*)', re.I)
            name = p.sub(r'SPF\1\2 PA\4', name)
        else:
            p = re.compile(r'spf\s?(\d+)\s?([+]*)', re.I)
            name = p.sub(r'SPF\1\2', name)
            
    # 세트 여부 구별 -> 세트로 구분되지 않은 상품 존재할 수 있음
    p = re.compile('set|세트', re.I)  # 컬렉션 / 박스 / 0종 / 키트 / 듀오 / 트리오 -> 세트 상품이 아닐 가능성 있음. 대부분이 세트로 걸러지긴 함-> 세트 표기가 더 나은지
    if p.search(name):
        sale_status = '세트상품'
    else:
        sale_status = '#'
    # 세트 이름에서 지워야하나?
    # name = p.sub(' ', name)
        

    # 할인 여부 구별 -> 할인으로 구분되지 않은 상품 존재할 수 있음
    p = re.compile(r'sale|할인|세일|\d+\s?[%]\s?off', re.I)
    if p.search(name) and sale_status != '#':
        sale_status += '/할인'
    elif p.search(name) and sale_status == '#':
        sale_status = '할인'
    elif sale_status != '#':
        pass
    else:
        sale_status = '#'
    name = p.sub(' ', name)

    # 한정판매여부 구별
    p = re.compile('리미티드|한정판매|한정품|한정판|한정|limited', re.I)
    if p.search(name) and sale_status != '#':
        sale_status += '/한정판매'
    elif p.search(name) and sale_status == '#':
        sale_status = '한정판매'
    elif sale_status != '#':
        pass
    else:
        sale_status = '#'
    name = p.sub(' ', name)

    # 품절여부 구별
    p = re.compile(r'품\s?절|sold\s?out|sold', re.I)
    if p.search(name) and sale_status != '#':
        sale_status += '/품절'
    elif p.search(name) and sale_status == '#':
        sale_status = '품절'
    elif sale_status != '#':
        pass
    else:
        sale_status = '#'
    name = p.sub(' ', name)

    # 괄호 안 추출
    '''
    p = re.compile(r'[(]([^)]*)[)]|[[]([^]]*)[]]|[<]([^>]*)[>]|[{]([^>]*)[}]')
    '''

    # 불필요한 수식어와 특수기호 제거 -> 별표사이사이에 있는 문구 삭제? ex)★~가 추천한 상품★   [리미티드] 추가하면 안됨.->리/미/티/드 다 제거
    p = re.compile(r'<br>|#디렉터파이_추천!|★겟잇뷰티 1위!★|최대3개구매가능|온라인\s?단독|온라인|online|사은품\s?:\s?샤워볼|기획\s?세트|기획\s?특가|기획|특가|컬러\s?추가|마지막\s?수량', re.I)
    name = p.sub(' ', name)
    p = re.compile(r'리미티드|한정판|한정|행사|event|이벤트|최대\s?\d*[%]|본품\s?\d?\s?[+]\s?리필\s?\d?|\d\s?[+]\s?\d|[★]|[☆]|추천|증정품|리필\s?증정|[@]|^|[^(re)]new[^(al)]|new!|_|-|~|!', re.I)
    #  [리미티드] [new] renewal 주의
    # 증정 -> ?
    name = p.sub(' ', name)
    
    # 제품이름에 volume이 괄호 안에 포함된 경우
    p = re.compile(r'(.*)[(]([^)]*(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs).*)[)](.*)')
    if p.search(name) and volume == '#':
        volume = p.sub(r'\2', name)
        name = p.sub(r'\1 \3', name)
    '''
    p = re.compile(r'\d+(\s)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I)
    if p.search(name) and volume == '#':
        volumes = p.findall(name)
        volume = ' '.join(volumes)
    name = p.sub(' ', name)
    '''
    # 제품이름에 volume이 2개 이상 포함된 경우
    p = re.compile(r'\d+(\s)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I)
    if p.search(name) and volume == '#':
        m = p.search(name)
        volume = m.group()
    name = p.sub(' ', name)
    # \d+(\s)?ml(\s)?[*](\s)?\d+매
    # \d+(\s)?ml[^+]
    # \d+(\s)?mg|\d+(\s)?g|\d+(\s)?oz|\d+(\s)?매|\d+(\s)?매입|\d+(\s)?ea|\d+(\s)?each
    
    
    # 제품이름에 type (대용량/리필/지성용/건성용/복합성) 포함 경우
    p = re.compile(r'대용량|소용량|리필 포함|리필용|본품[+]리필구성|본품[+]리필|리필|[(]소[)]|[(]중[)]|[(]대[)]|지성용|건선용|복합성')
    if p.search(name) and types == '#':
        m = p.search(name)
        types = m.group()
    name = p.sub(' ', name)
    
    # 제품이름에 _+옵션 경우
    '''
    p = re.compile(r'_(.+)\s?')
    if p.search(name) and types == '#':
        m = p.search(name)
        types = m.group()
    name = p.sub(' ', name)
    '''
        
    # 한글명과 영문명 분리
    p = re.compile(r'(.*[가-힣].*?)\s?([^\d가-힣][a-zA-Z]+)*')
    p2 = re.compile(r'(.*[가-힣].*?)\s?([^가-힣][a-zA-Z]+)*[가-힣]')
    p3 = re.compile('spf|pa|ad|uv|xp|set', re.I) # SPF00+ PA+ 부분 등을 영문명으로 인식하지 않도록

    if p.search(name) and p2.search(name) != True:
        en = p.sub(r'\2', name) 
        if p3.search(en):
            eng_name = '#'
        else:
            eng_name = en 
            name = p.sub(r' \1 ', name)  # 이 부분을 eng_name 지정하는 윗줄보다 먼저 쓰면 안됨 
    else:
        eng_name = '#'
    
    # RMK 스펀지(UV) RMK SPONGE(UV) -> name = RMK 스펀지, eng_name = (UV) RMK SPONGE(UV) 이런 경우 해결
    if eng_name != '#':
        enlist = eng_name.split()
        if len(enlist) > len(set(enlist)) and name.split()[-1]==enlist[0]:
            i = len(enlist) - len(set(enlist))
            name = name + ' ' + enlist[i-1]
            eng_name = ' '.join(enlist[i:])
    
    # 괄호들 제거
    #p = re.compile(r'[(]([^)]*)[)]|[[]([^]]*)[]]|[<]([^>]*)[>]|[{]([^>]*)[}]') # (), [], <>, {}
    p = re.compile(r'[[]|[]]|[(]|[)]|[<]|[>]|[{]|[}]')
    if p.search(name):
        name = p.sub(' ', name)
        eng_name = p.sub(' ', eng_name)

    # 한 칸 이상의 공백 제거
    p = re.compile(r'\s+')
    name = p.sub(' ', name)
    name = name.strip() # 앞뒤 공백 제거
    eng_name = p.sub(' ', eng_name)
    eng_name = eng_name.strip()

    p = re.compile(r'\d')
    if eng_name is None or eng_name == '' or len(eng_name) < 4 or p.match(eng_name):
        eng_name = '#'

    # sale_status칼럼: 세일상품, 할인, 한정, 품절-> 4가지
    result =  dict(jsonString, **{'name': name, 'volume': volume, 'type': types, 'sale_status': sale_status, 'eng_name': eng_name})
    
    return result

#%%
def cleanseVolume(jsonString):
    
    volume = jsonString.get('volume')
    
    # 영문 소문자 표기
    volume = str(volume).lower()
    
    # 용량x개수 표기 경우 용량*개수로 변경
    p = re.compile('x', re.I)
    volume = p.sub(r'*', volume)

    # 2가지 이상의 제품이 ,로 분류된 경우
    p = re.compile(r'[,]')
    if p.search(volume):
        volumes = volume.split('+')
        newvolumes = []
        for separatedvolume in volumes:
            p = re.compile(r'([가-힣]+[^()].*?)\s?(\d+)\s?((ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs))')
            if p.search(separatedvolume):
                separatedvolume = p.sub(r'\2\3(\1)', separatedvolume)
            newvolumes.append(separatedvolume)
        volume = ', '.join(newvolumes)

    # 2가지 이상의 제품이 +로 분류된 경우
    p = re.compile(r'[+]')
    if p.search(volume):
        volumes = volume.split('+')
        newvolumes = []
        for separatedvolume in volumes:
            #p = re.compile(r'([가-힣]+)\s?(\d+)\s?((ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs))')
            p = re.compile(r'([가-힣]+.*?)\s?(\d+)\s?((ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs))')
            if p.search(separatedvolume):
                separatedvolume = p.sub(r'\2\3(\1)', separatedvolume)
            newvolumes.append(separatedvolume)
        volume = ', '.join(newvolumes)
    

    # bottle/spray/pat 등 용량 앞에 수식어 붙는 경우 수식어 유지 + 단위가 pieces 같은 영어일 경우
    p = re.compile('pieces|piece|pcs', re.I)
    volume = p.sub('개', volume)

    # 용량과 단위 사이 띄어쓰기 없음
    p = re.compile(r'(\d)\s+([가-힣a-zA-Z])')
    volume = p.sub(r'\1\2', volume)

    # 용량 여러개 경우 / 로 구분
    #p = re.compile(r'([가-힣a-zA-Z])\s*(\d.)')
    #volume = p.sub(r'\1/\2', volume)

    p = re.compile(r'(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)\s*(\d.)')
    volume = p.sub(r'\1/\2', volume)

    # 용량*개수 경우 뒷 단위 제거
    p1 = re.compile(r'\s?[*]\s?(\d+).*[가-힣a-zA-Z]')
    volume = p1.sub(r'*\1', volume)
    #p2 = re.compile(r'([x].\d+).*[가-힣a-zA-Z]', re.I)
    #volume = p2.sub(r'\1', volume)
    
    

    #6 제품과 용량 모두 2가지 이상인 경우 [용량, 용량] or [용량(종류), 용량(종류)]   

    #7 제품 종류 2가지 이상이지만 용량 동일 경우 [용량*갯수(종류1/종류2/...)]

    #8 단위 여러개인 경우 ml과 g 우선 (oz 후순위)
    p = re.compile('(\d+\s?oz)(.*?)(\d+\s?(ml|g))', re.I)
    if p.search(volume):
        volume = p.sub(r'\3\2\1', volume)
    
    volume = volume.strip()
    
    result =  dict(jsonString, **{'volume': volume})
    
    return result

#%%
def cleanseColor(jsonString):
    
    color = jsonString.get('color')
    sale_status = jsonString.get('sale_status')
    saleprice = jsonString.get('salePrice')
    originalprice = jsonString.get('originalPrice')
    volume = jsonString.get('volume')
    
    color = str(color)
    saleprice = str(saleprice)
    originalprice = str(originalprice)

    # 특수문자/수식어 제거
    p = re.compile(r'[^(re)]new[^(al)]|추천|-|_|/|:|일반\s?판매|재고\s?[:]\s?\d*개|옵션가격|가격', re.I) # 제거하고 싶은 단어 추가  renewal 주의
    color = p.sub(' ', color) # space 한 칸 줘야 한글끼리, 영어끼리 띄어쓰기가 유지됨. 하지만 필요 이상의 공백이 생길 수 있으므로 한칸 이상 공백 제거하는 식 필요
    
    
    # 문자와 숫자는 띄어쓰기로 구분  -> 'A01 레드' 경우 ? 
    '''
    p1 = re.compile(r'([가-힣a-zA-Z]+)(\S\d+)') # 문자+숫자 사이 띄어쓰기
    color = p1.sub(r'\1 \2', color)
    '''
    #p2 = re.compile(r'(\d+)(\S[가-힣]+)') # 숫자+한글 사이 띄어쓰기
    #color = p2.sub(r'\1 \2', color)
    
    
    # 한글 영문 동시 기재시 한글을 앞으로
    p = re.compile(r'([a-zA-Z]+.*?)([가-힣]+.*)', re.I)
    if p.match(color):
        engColor = p.sub(r'\1', color)
        if len(engColor) > 3 :
            newOrder = p.sub(r'\2 \1', color)
            color = newOrder

    
    # 세트 여부 구별 -> 세트로 구분되지 않은 상품 존재할 수 있음
    p = re.compile('set|세트', re.I)  # 컬렉션 / 박스 / 0종 / 키트 / 듀오 / 트리오 -> 세트 상품이 아닐 가능성 있음. 대부분이 세트로 걸러지긴 함-> 세트 표기가 더 나은지
    if p.search(color):
        sale_status = '세트상품'
    else:
        sale_status = '#'

    # 품절 경우
    p = re.compile(r'품\s?절|sold\s?out|sold', re.I)
    if p.search(color) and sale_status != '#':
        sale_status += '/품절'
    elif p.search(color) and sale_status == '#':
        sale_status = '품절'
    elif sale_status != '#':
        pass
    else:
        sale_status = '#'
    color = p.sub(' ', color)

    # 할인 여부 구별
    p = re.compile(r'sale|할인|세일|\d+\s?[%]\s?off', re.I)
    if p.search(color) and sale_status != '#':
        sale_status += '/할인'
    elif p.search(color) and sale_status == '#':
        sale_status = '할인'
    elif sale_status != '#':
        pass
    else:
        sale_status = '#'
    color = p.sub(' ', color)

    # 가격변동 (+기호 있는 경우)
    p = re.compile(r'\D')
    saleprice = p.sub('', saleprice)
    originalprice = p.sub('', originalprice)
    p = re.compile(r'([+]\s?\d+)[,]?(\d+)\D?원?')
    p2 = re.compile(r'(\d+)[,]?(\d+)\D?원?')
    p3 = re.compile('할인')
    if p.search(color):
        colorCopy = color
        m = p.search(color)
        color = p.sub(' ', color)
        priceChange = m.group()
        #p = re.compile(r'\D')
        #priceChange = p.sub('', priceChange)
        #priceChange = p.sub(r' \1\2 ', priceChange)
        # 할인 중인 제품일 경우 saleprice 변경, +000 (최소 백원단위 증가 가정)
        if p3.search(sale_status) is True and saleprice != '#' and len(priceChange.strip()) > 3 :
            p = re.compile(r'\D')
            priceChange = p.sub('', priceChange)
            saleprice = saleprice + '+' + priceChange
            saleprice = eval(saleprice)
        # 할인 중인 제품이 아닐 경우 originalprice 변경, +000 (최소 백원단위 증가 가정)
        if p3.search(sale_status) is None and originalprice != '#' and len(priceChange.strip()) > 3 :
            p = re.compile(r'\D')
            priceChange = p.sub('', priceChange)
            originalprice = originalprice + '+' + priceChange
            originalprice = eval(originalprice)
        # 그 외는 가격변동 아님
        else:
            color = colorCopy
        
    # 가격변동 (+기호 없는 경우)
    elif p2.search(color):
        colorCopy = color
        m = p.search(color)
        color = p.sub(' ', color)
        if p3.search(sale_status) and saleprice == '#' :
            newPrice = m.group()
            newPrice = p.sub(r' \1\2 ', newPrice)
            p = re.compile(r'\s+')
            newPrice = p.sub('', newPrice)
            if len(newPrice) > 2:
                saleprice = newPrice
            else:
                color = colorCopy
        elif p3.search(sale_status) is None and originalprice == '#' :
            newPrice = m.group()
            newPrice = p.sub(r' \1\2 ', newPrice)
            p = re.compile(r'\s+')
            newPrice = p.sub('', newPrice)
            if len(newPrice) > 2:
                originalprice = newPrice
            else:
                color = colorCopy
    # 컬러에 volume이 괄호 안에 포함된 경우
    p = re.compile(r'(.*)[(]([^)]*(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs).*)[)](.*)')
    if p.search(color) and volume == '#':
        volume = p.sub(r'\2', color)
        color = p.sub(r'\1 \3', color)
    '''
    p = re.compile(r'\d+(\s)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I)
    if p.search(name) and volume == '#':
        volumes = p.findall(name)
        volume = ' '.join(volumes)
    name = p.sub(' ', name)
    '''
    # 컬러에 volume이 2개 이상 포함된 경우
    p = re.compile(r'\d+(\s)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I)
    if p.search(color) and volume == '#':
        m = p.search(color)
        volume = m.group()
    color = p.sub(' ', color)  


    # API에서 'option' -> 'color'로 바꾼경우 color에 type, volume 포함될 수 있다 (에스쁘아option = color, 아리따움option = type+volume, 훌리카 = color,type,'일반판매')

    p = re.compile(r'리미티드|한정판|한정|행사|event|이벤트|1\s?[+]\s?1|2\s?[+]\s?1|[★]|[☆]|추천|증정품|증정|[@]|^|[^(re)]new[^(al)]|new!|_|-|~|!', re.I)
    # * () [] / , .  _ 제외 특수기호 ? \W [리미티드] [new] renewal 주의
    color = p.sub(' ', color)

    # 괄호들 제거
    #p = re.compile(r'[(]([^)]*)[)]|[[]([^]]*)[]]|[<]([^>]*)[>]|[{]([^>]*)[}]') # (), [], <>, {}
    p = re.compile(r'[[]|[]]|[(]|[)]|[<]|[>]|[{]|[}]')
    if p.search(color):
        color = p.sub(' ', color)


    # 한 칸 이상의 공백은 제거
    p = re.compile(r'\s+')
    color = p.sub(' ', color)
    color = color.strip()
    
    result =  dict(jsonString, **{'color': color, 'volume': volume, 'originalPrice' : originalprice, 'salePrice': saleprice, 'sale_status' : sale_status})
    
    return result

#%%
def cleanseType(jsonString):
    
    types = jsonString.get('type')
    sale_status = jsonString.get('sale_status')
    saleprice = jsonString.get('salePrice')
    originalprice = jsonString.get('originalPrice')
    volume = jsonString.get('volume')

    types = str(types)
    saleprice = str(saleprice)
    originalprice = str(originalprice)
    
    # 특수문자/수식어 제거
    p = re.compile(r'[^(re)]new[^(al)]|추천|-|_|/|:|일반\s?판매|재고\s?[:]\s?\d*개|옵션가격|가격', re.I) # 제거하고 싶은 단어 추가  renewal 주의
    types = p.sub(' ', types) # space 한 칸 줘야 한글끼리, 영어끼리 띄어쓰기가 유지됨. 하지만 필요 이상의 공백이 생길 수 있으므로 한칸 이상 공백 제거하는 식 필요
    
    # 문자와 숫자는 띄어쓰기로 구분
    p1 = re.compile(r'([가-힣a-zA-Z]+)(\S\d+)') # 문자+숫자 사이 띄어쓰기
    types = p1.sub(r'\1 \2', types)
    p2 = re.compile(r'(\d+)(\S[가-힣a-zA-Z]+)') # 숫자+문자 사이 띄어쓰기
    types = p2.sub(r'\1 \2', types)

    # 품절 경우
    p = re.compile(r'품\s?절|sold\s?out|sold', re.I)
    if p.search(types) and sale_status != '#':
        sale_status += '/품절'
    elif p.search(types) and sale_status == '#':
        sale_status = '품절'
    elif sale_status != '#':
        pass
    else:
        sale_status = '#'
    types = p.sub(' ', types)

    p = re.compile(r'([+]\s?\d+)[,]?(\d+)\D?원?\s?')
    p2 = re.compile(r'(\d+)[,]?(\d+)\D?원?\s?')
    p3 = re.compile('할인')
    if p.search(types):
        typesCopy = types
        m = p.search(types)
        types = p.sub(' ', types)
        priceChange = m.group()
        priceChange = p.sub(r' \1\2 ', priceChange)
        # 할인 중인 제품일 경우 saleprice 변경, +000 (최소 백원단위 증가 가정)
        if p3.search(sale_status) and saleprice != '#' and len(priceChange.strip()) > 3 :
            saleprice = str(saleprice)
            saleprice += str(priceChange)
            p = re.compile(r'\s+')
            saleprice = p.sub('', saleprice)
            saleprice = eval(saleprice)
        # 할인 중인 제품이 아닐 경우 originalprice 변경, +000 (최소 백원단위 증가 가정)
        elif p3.search(sale_status) == False and originalprice != '#' and len(priceChange.strip()) > 3 :
            originalprice = str(originalprice)
            originalprice += str(originalChange)
            p = re.compile(r'\s+')
            originalprice = p.sub('', originalprice)
            originalprice = eval(originalprice)
        # 그 외는 가격변동 아님
        else:
            types = typesCopy
    # 가격변동 (+기호 없는 경우)
    elif p2.search(types):
        typesCopy = types
        m = p.search(types)
        types = p.sub(' ', types)
        if p3.search(sale_status) and saleprice == '#' :
            newPrice = m.group()
            newPrice = p.sub(r' \1\2 ', newPrice)
            p = re.compile(r'\s+')
            newPrice = p.sub('', newPrice)
            if len(newPrice) > 2:
                saleprice = newPrice
            else:
                types = typesCopy
        elif p3.search(sale_status) == False and originalprice == '#' :
            newPrice = m.group()
            newPrice = p.sub(r' \1\2 ', newPrice)
            p = re.compile(r'\s+')
            newPrice = p.sub('', newPrice)
            if len(newPrice) > 2:
                originalprice = newPrice
            else:
                types = typesCopy
    # 타입에 volume이 괄호 안에 포함된 경우
    p = re.compile(r'(.*)[(]([^)]*(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs).*)[)](.*)')
    if p.search(types) and volume == '#':
        volume = p.sub(r'\2', types)
        types = p.sub(r'\1 \3', types)
    '''
    p = re.compile(r'\d+(\s)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I)
    if p.search(name) and volume == '#':
        volumes = p.findall(name)
        volume = ' '.join(volumes)
    name = p.sub(' ', name)
    '''
    # 타입에 volume이 2개 이상 포함된 경우
    p = re.compile(r'\d+(\s)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I)
    if p.search(types) and volume == '#':
        m = p.search(types)
        volume = m.group()
    types = p.sub(' ', types)  


    # API에서 'option' -> 'color'로 바꾼경우 color에 type, volume 포함될 수 있다 (에스쁘아option = color, 아리따움option = type+volume, 훌리카 = color,type,'일반판매')

    # 괄호들 제거
    #p = re.compile(r'[(]([^)]*)[)]|[[]([^]]*)[]]|[<]([^>]*)[>]|[{]([^>]*)[}]') # (), [], <>, {}
    p = re.compile(r'[[]|[]]|[(]|[)]|[<]|[>]|[{]|[}]')
    if p.search(types):
        types = p.sub(' ', types)

    # 괄호 안 부가설명 있을 경우

    # API에서 'option' -> 'type'으로 바꾼경우 타입에 용량 포함될 수 있다
    
    # 한 칸 이상의 공백은 제거
    p = re.compile(r'\s+')
    types = p.sub(' ', types)
    types = types.strip()
    
    result =  dict(jsonString, **{'type': types, 'volume': volume, 'originalPrice' : originalprice, 'salePrice': saleprice, 'sale_status' : sale_status})
    
    return result

# 원화/달러/유료 표기
# price는 무조건 numeric이라 가정

#%%
def cleansePrice(jsonString):
    brand = jsonString.get('brand')
    saleprice = jsonString.get('salePrice')
    originalprice = jsonString.get('originalPrice')
    
    # thousand separator
    if brand == 'tomford' or brand == 'TOMFORD':
        # 'tomford' 브랜드의 경우 달러 기호 포함
        p = re.compile(r'\D')
        saleprice = p.sub('', saleprice)
        originalprice = p.sub('', originalprice)
        saleprice = '$' + '{:,}'.format(int(saleprice))
        originalprice = '$' + '{:,}'.format(int(originalprice))
    elif saleprice != '#' and originalprice != '#':
        saleprice = str(saleprice)
        originalprice = str(originalprice)
        p = re.compile(r'\D')
        saleprice = p.sub('', saleprice)
        originalprice = p.sub('', originalprice)
        saleprice = '{:,}'.format(int(saleprice))
        originalprice = '{:,}'.format(int(originalprice))
        '''
        if type(originalprice) == type(1) and type(saleprice) == type(1) :
            saleprice = '{:,}'.format(int(saleprice))
            originalprice = '{:,}'.format(int(originalprice))
        elif type(originalprice) == type(1):
            p = re.compile(r'\D')
            saleprice = p.sub('', saleprice)
            saleprice = '{:,}'.format(int(saleprice))
            originalprice = '{:,}'.format(int(originalprice))
        elif type(saleprice) == type(1):
            p = re.compile(r'\D')
            originalprice = p.sub('', originalprice)
            saleprice = '{:,}'.format(int(saleprice))
            originalprice = '{:,}'.format(int(originalprice))
        else:
            p = re.compile(r'\D')
            saleprice = p.sub('', saleprice)
            originalprice = p.sub('', originalprice)
            saleprice = '{:,}'.format(int(saleprice))
            originalprice = '{:,}'.format(int(originalprice))
        '''
    result =  dict(jsonString, **{'salePrice': saleprice, 'originalPrice': originalprice})
    
    return result

def cleanseColumns2(jsonString):
    columnList = jsonString.keys()
    if 'sale_status' not in columnList:
        jsonString = dict(jsonString, **{'sale_status':'#'})
   
    return jsonString

# 최종 데이터 칼럼 13개: 'brand', 'name', 'category', 'image', 'url', 'color', 'type', 'volume', 'salePrice', 'orignialPrice', 'skuid', 'sale_status', 'eng_name'

#%%
'''
sample = {
		"name": "라스트 오토 젤 아이라이너 ",
		"url": "http://www.bbia.co.kr//shop/shopdetail.html?branduid=86260&xcode=007&mcode=001&scode=003&type=X&sort=manual&cur_code=007001&GfDT=bmx1W18%3D",
		"image": [
			"http://www.bbia.co.kr//shopimages/bbia/0070010000243.jpg?1528934756"
		],
		"color": "베이직 6종 (+45,000원)",
		"category": "",
		"salePrice": "9,000원",
		"originalPrice": "9,000원",
		"brand": "삐아"
	}
s = cleanseColumnNames(sample)
s = cleanseColumns1(s)
s = cleanseBrand(s)
# s = cleansePrice(s)
s = cleanseName(s)
s = cleanseVolume(s)
s = cleanseColor(s)
s = cleanseType(s)
s = cleansePrice(s)
s = cleanseColumns2(s)
s
'''