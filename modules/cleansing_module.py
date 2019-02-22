import json
import re

# 함수들 input(jsonString)의 형태 : {'key1':'value1', 'key2':'value2', ...}


'''정규식 리스트
space = re.compile(r'\s+') : 한 칸 이상의 공백
digit = re.compile(r'\d') : 숫자
mod = re.compile(r"""<br>|[#]디렉터파이_추천!|★겟잇뷰티 1위!★|최대\d개구매가능|온라인\s?단독|온라인|online|사은품\s?:\s?샤워볼|기획\s?세트|기획\s?특가|기획|특가|컬러\s?추가|마지막\s?수량|
                    행사|event|이벤트|최대\s?\d*[%]|본품\s?\d?\s?[+]\s?리필\s?\d?|\d\s?[+]\s?\d|[★]|[☆]|추천|증정품|리필\s?증정|[@]|^|[^(re)]new[^(al)]|new!|_|-|~|!
                    """, re.I|re.X)
includingVolume1 = re.compile(r'(.*)[(]([^)]*(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs).*)[)](.*)') : volume이 포함된 경우
includingVolume2 = re.compile(r'\d+(\s)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I) : volume이 2개 이상 포함된 경우 (volume이 하나만 포함된 경우와 표기 형식이 다르기 때문에 따로 정규식 작성한 것)
includingType = re.compile(r'대용량|소용량|리필 포함|리필용|본품[+]리필구성|본품[+]리필|리필|[(]소[)]|[(]중[)]|[(]대[)]|지성용|건선용|복합성') : type이 포함된 경우    
brackets = re.compile(r'[[]|[]]|[(]|[)]|[<]|[>]|[{]|[}]') : 괄호
volumeForm_comma = re.compile(r'([가-힣]+[^()].*?)\s?(\d+)\s?((ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs))') : comma로 분리된 volume
volumeForm_plus = re.compile(r'([가-힣]+.*?)\s?(\d+)\s?((ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs))') : plus기호로 분리된 volume
multiVolumes = re.compile(r'(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)\s*(\d.)') : 여러 개의 용량
    '''

# API로 가져온 데이터의 칼럼을 크롤링한 데이터 기준 칼럼과 통일시킴
def cleanseColumnNames(jsonString):
    
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
        'option' : 'color',     # color로투터 type, volume 분리하는 것이 더 편하기 때문에 'option'은 'color'로 변경
        'originalName': 'delete',  # 불필요한 칼럼의 경우 이름을 'delete'로 변경 (cleansing.py에서 'delete'칼럼들 삭제)
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

# 필요 칼럼이 없을 경우 default값 가진 칼럼 추가해 줌
def cleanseColumns(jsonString):
    
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
    # sale_status 추가해 줌
    jsonString = dict(jsonString, **{'sale_status':'#'})
    # dummy 'delete'칼럼 추가 : 'delete' key가 하나도 없을 경우 cleansing.py에서 전체 데이터가 필터링되기 때문
    if 'delete' not in columnList:
        jsonString = dict(jsonString, **{'delete':'#'})

    return jsonString

# 브랜드명 클렌징 + 취급하지 않는 브랜드의 데이터 제거 + skuid의 브랜드명 약어 부여
def cleanseBrand(jsonString):
    
    # 상품 Master.xlsx - 브랜드 sheet을 저장한 json파일 {'영문명':'영문명목록', '한글명':'한글명목록', '약어':'약어목록'}을 'reference'로 불러옴 -> 상품 Master 문서가 변경될 경우 json파일도 변경해 줘야 함!
    with open('./brandReference.json', encoding="UTF-8") as json_data: 
        reference = json.load(json_data)
  
    brand = jsonString.get('brand')

    # reference로부터 리스트 형태로 가져옴
    brandList = list(reference.get('영문명').values()) # 취급 브랜드의 영문명 리스트
    korBrandList = list(reference.get('한글명').values()) # 취급 브랜드의 한글명 리스트
    abbList = list(reference.get('약어').values()) # 브랜드 약어 리스트
    
    p = re.compile(r'\s+') #띄어쓰기 패턴
    brand = re.sub(p, '',brand) #띄어쓰기 패턴 제거
    brand = brand.upper() #브랜드명 대문자로 표기

    # 브랜드명이 한글명일 경우 영문명으로 바꿔줌
    if brand in korBrandList:
        idx = korBrandList.index(brand)
        newBrand = brandList[idx]
        brand = newBrand

    # 취급하지 않는 브랜드의 상품에 대해 None 리턴
    if brand not in brandList:
        return None
    # skuid 브랜드 약어 부분 부여
    else:
        brand = brand.upper()
        idx = brandList.index(brand)
        skuid = abbList[idx]
        result = dict(jsonString, **{'brand': brand, 'skuid': skuid})
    
        return result

# 'image'가 리스트 형태가 아닐 경우 리스트로 변경
def cleanseImage(jsonString):
    image = jsonString.get('image')
    if isinstance(image, str()):
        image = image.split(',')
    result = dict(jsonString, **{'image' : image})
    print(image)
    return result

def createSaleStatus(jsonString):
'''
    sale_status = jsonString.get('sale_status')
    name = jsonString.get('name')
    volume = jsonString.get('volume')
    color = jsonString.get('color')
    types = jsonString.get('types')

    valueList = [name, volume, color, types]

    saleStatusDict = {'setPattern' : '세트상품', 'soldoutPattern' : '품절', 'discountPattern': '할인', 'limitedPattern' : '한정'}

    setPattern = re.compile('set|세트', re.I)
    soldoutPattern = re.compile(r'품\s?절|sold\s?out|sold', re.I)
    discountPattern = re.compile(r'sale|할인|세일|\d+\s?[%]\s?off', re.I)
    limitedPattern = re.compile(r'리미티드|한정판매|한정품|한정판|한정|limited', re.I)

    p = saleStatusDict.key()
    if p.search(value) and sale_status == '#':
        sale_status = saleStatusDict.get(p)
    else:
         p.search(value) and sale_status != '#':
        sale_status += ('/' + saleStatusDict.get(p))
    
    saleStatusList = sale_status.split('/')
    saleStatusList = list(set(saleStatusList))
    sale_status = '/'.join(saleStatusList)


    # 할인 여부 구별
    p = re.compile(r'sale|할인|세일|\d+\s?[%]\s?off', re.I)
    discountPattern = re.compile('할인')
    if p.search(types) and discountPattern.search(sale_status) is None and sale_status != '#':
        sale_status += '/할인'
    elif p.search(types) and sale_status == '#':
        sale_status = '할인'
    types = p.sub(' ', types)


    # 세트 여부 구별
    p = re.compile('set|세트', re.I) # 세트 패턴
    if p.search(name):
        sale_status = '세트상품'
    else:
        sale_status = '#'
 
    # 할인 여부 구별 
    p = re.compile(r'sale|할인|세일|\d+\s?[%]\s?off', re.I) # 할인 패턴
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
    p = re.compile(r'리미티드|한정판매|한정품|한정판|한정|limited', re.I) # 한정판매 패턴
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
    p = re.compile(r'품\s?절|sold\s?out|sold', re.I) # 품절 패턴
    if p.search(name) and sale_status != '#':
        sale_status += '/품절'
    elif p.search(name) and sale_status == '#':
        sale_status = '품절'
    elif sale_status != '#':
        pass
    else:
        sale_status = '#'
    name = p.sub(' ', name)

    # 세트 여부 구별
    p = re.compile('set|세트', re.I)
    setPattern = re.compile('세트상품')  
    if p.search(color) and setPattern.search(sale_status) is None and sale_status != '#':
        sale_status += '/세트상품'
    elif p.search(color) and sale_status == '#' :
        sale_status = '세트상품'

    # 품절 경우
    p = re.compile(r'품\s?절|sold\s?out|sold', re.I)
    soldoutPattern = re.compile('품절')
    if p.search(color) and soldoutPattern.search(sale_status) is None and sale_status != '#':
        sale_status += '/품절'
    elif p.search(color) and sale_status == '#':
        sale_status = '품절'
    color = p.sub(' ', color)

    # 할인 여부 구별
    p = re.compile(r'sale|할인|세일|\d+\s?[%]\s?off', re.I)
    discountPattern = re.compile('할인')
    if p.search(color) and discountPattern.search(sale_status) is None and sale_status != '#':
        sale_status += '/할인'
    elif p.search(color) and sale_status == '#':
        sale_status = '할인'
    color = p.sub(' ', color)

    # 세트 여부
    p = re.compile('set|세트', re.I)
    setPattern = re.compile('세트상품')
    if p.search(types) and setPattern.search(sale_status) is None and sale_status != '#':
        sale_status += '/세트상품'
    elif p.search(types) and sale_status == '#' :
        sale_status = '세트상품'

    # 품절 경우
    p = re.compile(r'품\s?절|sold\s?out|sold', re.I)
    soldoutPattern = re.compile('품절')
    if p.search(types) and soldoutPattern.search(sale_status) is None and sale_status != '#':
        sale_status += '/품절'
    elif p.search(types) and sale_status == '#':
        sale_status = '품절'
    types = p.sub(' ', types)

    # 할인 여부 구별
    p = re.compile(r'sale|할인|세일|\d+\s?[%]\s?off', re.I)
    discountPattern = re.compile('할인')
    if p.search(types) and discountPattern.search(sale_status) is None and sale_status != '#':
        sale_status += '/할인'
    elif p.search(types) and sale_status == '#':
        sale_status = '할인'
    types = p.sub(' ', types)

def findVolume(jsonString):

'''
def cleanseName(jsonString):
    # 각 내용 순서도 중요!
    name = jsonString.get('name')
    volume = jsonString.get('volume')
    types = jsonString.get('type')

    # 자외선차단지수 SPF00+ PA+ 형식으로 통일
    spf = re.compile(r'spf', re.I) # ignorecase
    if spf.search(name):
        pa = re.compile(r'pa', re.I)
        if pa.search(name):  #이름에 spf, pa 모두 포함 경우
            SpfPa = re.compile(r'spf\s?(\d+)\s?([+]*)(.*)pa\s?([+]*)', re.I)
            name = SpfPa.sub(r'SPF\1\2 PA\4', name)
        else: #이름에 spf만 포함 경우
            Spf = re.compile(r'spf\s?(\d+)\s?([+]*)', re.I)
            name = Spf.sub(r'SPF\1\2', name)

    # 불필요한 수식어와 특수기호 제거
    mod = re.compile(r"""<br>|[#]디렉터파이_추천!|★겟잇뷰티 1위!★|최대\d개구매가능|온라인\s?단독|온라인|online|사은품\s?:\s?샤워볼|기획\s?세트|기획\s?특가|기획|특가|컬러\s?추가|마지막\s?수량|
                    행사|event|이벤트|최대\s?\d*[%]|본품\s?\d?\s?[+]\s?리필\s?\d?|\d\s?[+]\s?\d|[★]|[☆]|추천|증정품|리필\s?증정|[@]|^|[^(re)]new[^(al)]|new!|_|-|~|!
                    """, re.I|re.X) # 제거하고 싶은 단어 추가
    name = mod.sub(' ', name)
    
    
    # 제품이름에 volume이 괄호 안에 포함된 경우 이름에서 제거하고 volume으로 분리
    includingVolume1 = re.compile(r'(.*)[(]([^)]*(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs).*)[)](.*)') # A(숫자+용량단위)C -> name: AC, volume: 숫자+용량단위
    if includingVolume1.search(name) and volume == '#': # volume이 이미 존재한다면 이름에서 제거하지 않고 volume으로 분리하지도 않음
        volume = includingVolume1.sub(r'\2', name)
        name = includingVolume1.sub(r'\1 \3', name)
    
    # 제품이름에 volume이 2개 이상 포함된 경우 이름에서 제거하고 volume으로 분리
    includingVolume2 = re.compile(r'\d+(\s)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I) # 숫자+용량단위 */+/x/none 숫자+용량단위 -> volume 
    if includingVolume2.search(name) and volume == '#': # volume이 이미 존재한다면 이름에서 제거만 함
        volumesFound = includingVolume2.search(name)
        volume = volumesFound.group()
    name = includingVolume2.sub(' ', name)
    
    # 제품이름에 type (대용량/리필/지성용/건성용/복합성) 포함 경우 이름에서 제거하고 type으로 분리
    includingType = re.compile(r'대용량|소용량|리필 포함|리필용|본품[+]리필구성|본품[+]리필|리필|[(]소[)]|[(]중[)]|[(]대[)]|지성용|건선용|복합성')
    if includingTyoe.search(name) and types == '#': # type 이미 존재한다면 이름에서 제거만 함
        typeFound = includingType.search(name)
        types = typeFound.group()
    name = includingType.sub(' ', name)
        
    # 한글명과 영문명 분리
    KorEng_pattern = re.compile(r'(.*[가-힣].*?)\s?([^\d가-힣][a-zA-Z]+)*') # 한글명+영문명 패턴
    notKorEng_pattern = re.compile(r'(.*[가-힣].*?)\s?([^가-힣][a-zA-Z]+)*[가-힣]') # 한글명+영문명 패턴이 아닌 경우
    excludeEng = re.compile('spf|pa|ad|uv|xp|set', re.I) # SPF00+ PA+ 부분 등을 영문명으로 인식하지 않도록. 이 패턴을 가진다면 영문명이 아님

    if KorEng_pattern.search(name) and notKorEng_pattern.search(name) != True: # 한글명+영문명 패턴인 경우 영문명 분리
        en = KorEng_pattern.sub(r'\2', name) 
        if excludeEng.search(en):
            eng_name = '#'
        else:
            eng_name = en 
            name = KorEng_pattern.sub(r' \1 ', name)
    else:
        eng_name = '#'
    
    if eng_name != '#': # 한글명+영문명 분리시 한글명 끝부분에 영어가 있는 경우
        enlist = eng_name.split()
        if len(enlist) > len(set(enlist)) and name.split()[-1]==enlist[0]: # 영문명에 중복된 단어가 있고 한글명의 마지막 단어가 영문명의 첫 단어와 일치할 경우 -> 한글명/영문명 잘못 분리된 것
            i = len(enlist) - len(set(enlist)) # 영문명에 잘못 들어간 한글명 부분의 단어 개수만큼
            name = name + ' ' + enlist[i-1] # 한글명에 추가해 주고
            eng_name = ' '.join(enlist[i:]) # 영문명에서는 제거해 준다
    
    # 괄호 제거
    brackets = re.compile(r'[[]|[]]|[(]|[)]|[<]|[>]|[{]|[}]')
    if brackets.search(name):
        name = brackets.sub(' ', name)
        eng_name = brackets.sub(' ', eng_name)

    # 불필요 공백 제거(name, eng_name)
    space = re.compile(r'\s+')
    name = space.sub(' ', name)
    name = name.strip()
    eng_name = space.sub(' ', eng_name)
    eng_name = eng_name.strip()

    # 공백 제거 후 영문명 잘못 분리된 경우 다시 처리
    digit = re.compile(r'\d')
    if eng_name is None or eng_name == '' or len(eng_name) < 4 or digit.match(eng_name): # 영문명 단어 길이가 너무 짧거나 숫자로 시작한다면 잘못 분리된 것
        eng_name = '#'
    '''
    ex) '나이트크림 UV Night Cream UV' -> [잘못 분리] name : '나이트크림', eng_name : 'UV Night Cream UV' => [처리 후] name : '나이트 크림 UV', eng_name : 'Night Cream UV'
        '플레이펜슬 204 Playpencil 204' -> [잘못 분리] name : '플레이펜슬', eng_name : '204 Playpencil 204' => [처리 후] name : '플레이펜슬 204', eng_name : 'Playpencil 204'
    '''

    # name 클렌징 후 변경된 값들을 update
    result =  dict(jsonString, **{'name': name, 'volume': volume, 'type': types, 'sale_status': sale_status, 'eng_name': eng_name}) # sale_status : 세일상품, 할인, 한정, 품절, # -> 4가지 여부 추가됨
    
    return result
    
def cleanseVolume(jsonString):
    
    volume = jsonString.get('volume')

    volume = str(volume).lower()
    
    # 용량x개수 표기 경우 용량*개수로 변경
    x = re.compile('x', re.I)
    volume = x.sub(r'*', volume)

    # 2가지 이상의 제품 용량이 ,로 분리된 경우
    comma = re.compile(r'[,]')
    if comma.search(volume):
        volumes = volume.split(',') # comma로 split
        newvolumes = []
        for separatedvolume in volumes:
            volumeForm_comma = re.compile(r'([가-힣]+[^()].*?)\s?(\d+)\s?((ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs))') # 분리된 용량을 각각 형식에 맞게 클렌징
            if volumeForm_comma.search(separatedvolume):
                separatedvolume = volumeForm_comma.sub(r'\2\3(\1)', separatedvolume)
            newvolumes.append(separatedvolume)
        volume = ', '.join(newvolumes) # 클렌징된 용량을 다시 ,로 합침

    # 2가지 이상의 제품 용량이 +로 분리된 경우
    plus = re.compile(r'[+]')
    if plus.search(volume):
        volumes = volume.split('+') # +로 split
        newvolumes = []
        for separatedvolume in volumes:
            volumeForm_plus = re.compile(r'([가-힣]+.*?)\s?(\d+)\s?((ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs))') # 분리된 용량을 각각 형식에 맞게 클렌징
            if volumeForm_plus.search(separatedvolume):
                separatedvolume = volumeForm_plus.sub(r'\2\3(\1)', separatedvolume)
            newvolumes.append(separatedvolume)
        volume = ', '.join(newvolumes) # 클렌징된 용량을 다시 ,로 합침
    
    # 단위가 pieces 같은 영어일 경우 한글로 대체
    pieces = re.compile('pieces|piece|pcs', re.I)
    volume = pieces.sub('개', volume)

    # 용량과 단위 사이 띄어쓰기 없음
    volumeNoSpace = re.compile(r'(\d)\s+([가-힣a-zA-Z])')
    volume = VolumeNoSpace.sub(r'\1\2', volume)

    # 용량 여러개 경우 / 로 구분
    multiVolumes = re.compile(r'(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)\s*(\d.)') # 용량단위와 숫자 사이에 / 추가
    volume = multiVolumes.sub(r'\1/\2', volume)

    # 용량*개수 경우 뒷 단위 제거
    setVolume = re.compile(r'\s?[*]\s?(\d+).*[가-힣a-zA-Z]')
    volume = setVolume.sub(r'*\1', volume)

    # 단위 여러개인 경우 ml과 g 우선 (oz 후순위)
    unitOrder = re.compile(r'(\d+\s?oz)(.*?)(\d+\s?(ml|g))', re.I) # oz가 ml, g 보다 먼저 발견될 경우
    if unitOrder.search(volume):
        volume = unitOrder.sub(r'\3\2\1', volume)
    
    # 불필요 공백 제거
    space = re.compile(r'\s+')
    volume = space.sub(' ', volume)
    volume = volume.strip()

    # 클렌징 과정에서 volume이 통째로 다른 항목으로 분류되었을 경우 default값 부여
    if volume == '':
        volume = '#'
    
    result =  dict(jsonString, **{'volume': volume})
    
    return result

def cleanseColor(jsonString):
    
    color = jsonString.get('color')
    sale_status = jsonString.get('sale_status')
    saleprice = jsonString.get('salePrice')
    originalprice = jsonString.get('originalPrice')
    volume = jsonString.get('volume')
    
    color = str(color)
    saleprice = str(saleprice)
    originalprice = str(originalprice)

    # 불필요한 수식어와 특수문자 제거
    mod = re.compile(r"""<br>|[#]디렉터파이_추천!|★겟잇뷰티 1위!★|최대\d개구매가능|온라인\s?단독|온라인|online|사은품\s?:\s?샤워볼|기획\s?세트|기획\s?특가|기획|특가|컬러\s?추가|마지막\s?수량|
                    행사|event|이벤트|최대\s?\d*[%]|본품\s?\d?\s?[+]\s?리필\s?\d?|\d\s?[+]\s?\d|[★]|[☆]|추천|증정품|리필\s?증정|[@]|^|[^(re)]new[^(al)]|new!|_|-|~|!
                    """, re.I|re.X)
    color = mod.sub(' ', color)
    
    # 한글 영문 동시 기재시 한글을 앞으로
    EngKor_pattern = re.compile(r'([a-zA-Z]+.*?)([가-힣]+.*)', re.I) # 영문명+한글명 패턴
    if EngKor_pattern.match(color):
        engColor = EngKor_pattern.sub(r'\1', color)
        if len(engColor) > 3 :
            newOrder = EngKor_pattern.sub(r'\2 \1', color)
            color = newOrder

    # 가격변동
    nonDigit = re.compile(r'\D') # 숫자가 아닌 문자는 가격에서 제거
    saleprice = nonDigit.sub('', saleprice) 
    originalprice = nonDigit.sub('', originalprice)
    priceChange1 = re.compile(r'([+]\s?[^0]\d+)[,]?(\d+)\D?원?') # +0(,)000(원) 패턴
    priceChange2 = re.compile(r'(\d+)[,]?(\d+)\D?원?') # 0(,)000(원) 패턴
    sale = re.compile('할인') # 할인 상품인지 여부 (sale_status 참고)
    if priceChange1.search(color): # 가격변동 (+기호 있는 경우, pattern1 )
        colorCopy = color
        m = priceChange1.search(color)
        color = priceChange1.sub(' ', color)
        priceChange = m.group()
        # 할인 중인 제품일 경우(sale_status 참고) saleprice 변경, +000 (최소 백원단위로 증가 가정, 백원 미만 증가 경우 가격변동으로 잘못 분류된 것으로 판단)
        if sale.search(sale_status) is True and saleprice != '#' and len(priceChange.strip()) > 3 :
            priceChange = nonDigit.sub('', priceChange)
            saleprice = saleprice + '+' + priceChange
            saleprice = eval(saleprice) # eval(기존 가격+priceChange)
        # 할인 중인 제품이 아닐 경우 originalprice 변경,  +000 (최소 백원단위로 증가 가정, 백원 미만 증가 경우 가격변동으로 잘못 분류된 것으로 판단)
        if sale.search(sale_status) is None and originalprice != '#' and len(priceChange.strip()) > 3 :
            priceChange = nonDigit.sub('', priceChange)
            originalprice = originalprice + '+' + priceChange
            originalprice = eval(originalprice) # eval(기존 가격+priceChange)
        # 그 외는 가격변동 아님
        else:
            color = colorCopy
    elif priceChange2.search(color): # 가격변동 (+기호 없는 경우, pattern2 )
        colorCopy = color
        m = priceChange2.search(color)
        color = priceChange2.sub(' ', color)
        # 할인 중인 제품일 경우(sale_status 참고) saleprice 변경
        if sale.search(sale_status) and saleprice == '#' :
            newPrice = m.group()
            newPrice = priceChange2.sub(r' \1\2 ', newPrice)
            newPrice = space.sub('', newPrice)
            if len(newPrice) > 2: # 000 (최소 백원단위로 증가 가정, 백원 미만 증가 경우 가격변동으로 잘못 분류된 것으로 판단)
                saleprice = newPrice
            else:
                color = colorCopy
        # 할인 중인 제품이 아닐 경우 originalprice 변경
        elif sale.search(sale_status) is None and originalprice == '#' :
            newPrice = m.group()
            newPrice = priceChange2.sub(r' \1\2 ', newPrice)
            newPrice = space.sub('', newPrice)
            if len(newPrice) > 2: # 000 (최소 백원단위로 증가 가정, 백원 미만 증가 경우 가격변동으로 잘못 분류된 것으로 판단)
                originalprice = newPrice
            else:
                color = colorCopy

    # 컬러에 volume이 괄호 안에 포함된 경우 이름에서 제거하고 volume으로 분리
    if includingVolume1.search(color) and volume == '#': # volume이 이미 존재한다면 컬러에서 제거하지 않고 volume으로 분리하지도 않음
        volume = includingVolume1.sub(r'\2', color)
        color = includingVolume1.sub(r'\1 \3', color)

    # 컬러에 volume이 2개 이상 포함된 경우 이름에서 제거하고 volume으로 분리
    if includingVolume2.search(color) and volume == '#': # volume이 이미 존재한다면 컬러에서 제거하지 않고 volume으로 분리하지도 않음
        m = includingVolume2.search(color)
        volume = m.group()
    color = includingVolume2.sub(' ', color)  

    # 불필요한 수식어와 특수기호 제거
    color = mod.sub(' ', color)

    # 괄호들 제거
    color = brackets.sub(' ', color)

    # 불필요 공백 제거
    color = space.sub(' ', color)
    color = color.strip()

    # 클렌징 과정에서 color가 통째로 다른 항목으로 분류되었을 경우 default값 부여
    if color == '':
        color = '#'
    
    result =  dict(jsonString, **{'color': color, 'volume': volume, 'originalPrice' : originalprice, 'salePrice': saleprice, 'sale_status' : sale_status})
    
    return result

def cleanseType(jsonString):
    
    types = jsonString.get('type')
    sale_status = jsonString.get('sale_status')
    saleprice = jsonString.get('salePrice')
    originalprice = jsonString.get('originalPrice')
    volume = jsonString.get('volume')

    types = str(types)
    saleprice = str(saleprice)
    originalprice = str(originalprice)
    
    # 불필요한 수식어와 특수문자 제거
    types = mod.sub(' ', types) 

    # 문자와 숫자는 띄어쓰기로 구분
    wordNum = re.compile(r'([가-힣a-zA-Z]+)(\S\d+)') # 문자+숫자 사이 띄어쓰기
    types = wordNum.sub(r'\1 \2', types)
    numWord = re.compile(r'(\d+)(\S[가-힣a-zA-Z]+)') # 숫자+문자 사이 띄어쓰기
    types = numWord.sub(r'\1 \2', types)

    # 가격변동
    nonDigit = re.compile(r'\D') # 숫자가 아닌 문자는 가격에서 제거
    saleprice = nonDigit.sub('', saleprice) 
    originalprice = nonDigit.sub('', originalprice)
    priceChange1 = re.compile(r'([+]\s?[^0]\d+)[,]?(\d+)\D?원?') # +0(,)000(원) 패턴
    priceChange2 = re.compile(r'(\d+)[,]?(\d+)\D?원?') # 0(,)000(원) 패턴
    sale = re.compile('할인') # 할인 상품인지 여부 (sale_status 참고)
    if p.search(types): # 가격변동 (+기호 있는 경우, pattern1 )
        typesCopy = types
        m = priceChange1.search(types)
        types = priceChange1.sub(' ', types)
        priceChange = m.group()
        # 할인 중인 제품일 경우(sale_status 참고) saleprice 변경, +000 (최소 백원단위로 증가 가정, 백원 미만 증가 경우 가격변동으로 잘못 분류된 것으로 판단)
        if sale.search(sale_status) is True and saleprice != '#' and len(priceChange.strip()) > 3 :
            priceChange = nonDigit.sub('', priceChange)
            saleprice = saleprice + '+' + priceChange
            saleprice = eval(saleprice) # eval(기존 가격+priceChange)
        # 할인 중인 제품이 아닐 경우 originalprice 변경,  +000 (최소 백원단위로 증가 가정, 백원 미만 증가 경우 가격변동으로 잘못 분류된 것으로 판단)
        if sale.search(sale_status) is None and originalprice != '#' and len(priceChange.strip()) > 3 :
            priceChange = nonDigit.sub('', priceChange)
            originalprice = originalprice + '+' + priceChange
            originalprice = eval(originalprice) # eval(기존 가격+priceChange)
        # 그 외는 가격변동 아님
        else:
            types = typesCopy
    elif priceChange2.search(types): # 가격변동 (+기호 없는 경우, pattern2 )
        typesCopy = types
        m = priceChange2.search(types)
        types = priceChange2.sub(' ', types)
        # 할인 중인 제품일 경우(sale_status 참고) saleprice 변경
        if sale.search(sale_status) and saleprice == '#' :
            newPrice = m.group()
            newPrice = priceChange2.sub(r' \1\2 ', newPrice)
            newPrice = space.sub('', newPrice)
            if len(newPrice) > 2: # 000 (최소 백원단위로 증가 가정, 백원 미만 증가 경우 가격변동으로 잘못 분류된 것으로 판단)
                saleprice = newPrice
            else:
                types = typesCopy
        # 할인 중인 제품이 아닐 경우 originalprice 변경
        elif sale.search(sale_status) is None and originalprice == '#' :
            newPrice = m.group()
            newPrice = priceChange2.sub(r' \1\2 ', newPrice)
            newPrice = space.sub('', newPrice)
            '''
        001 버건디 + 200 오렌지
        현재 데이터에서는 이 가정이 성립함
        -> 추가 크롤링 => + 1000 오렌지
        '''
            if len(newPrice) > 2: # 000 (최소 백원단위로 증가 가정, 백원 미만 증가 경우 가격변동으로 잘못 분류된 것으로 판단)
                originalprice = newPrice
            else:
                types = typesCopy
        '''
            sale != origin, 할인x , origin = sale
        할인인지 아닌지 /
        할인한다의 기준은 name, color, volume, type 할인이라고 적혀있는 경우 => 할인
        color에 가격변동이 있다면 => sale price(판매가)에 가격변동 반영
        고민 필요
        original + 가격변동, sale + 가격변동  =>
        '''
                



    # 타입에 volume이 괄호 안에 포함된 경우 이름에서 제거하고 volume으로 분리
    if includingVolume1.search(types) and volume == '#': # volume이 이미 존재한다면 타입에서 제거하지 않고 volume으로 분리하지도 않음
        volume = includingVolume1.sub(r'\2', types)
        types = includingVolume1.sub(r'\1 \3', types)
                '''
    만약, volume에 값이 있는데
    type에서 위의 패턴들이 search된다면
    이거는 다른 의미라고 가정(volume 뜻이 아니라고 가정)
    100ml
    대 사이즈(+500ml) + 3000 
    이런 경우 고려해보아야함
    '''

   
    # 타입에 volume이 2개 이상 포함된 경우 이름에서 제거하고 volume으로 분리
    if includingVolume2.search(types) and volume == '#': # volume이 이미 존재한다면 타입에서 제거하고 volume으로 분리하지는 않음
        m = includingVolume2.search(types)
        volume = m.group()
    types = includingVolume2.sub(' ', types)  

    # 괄호들 제거
    if brackets.search(types):
        types = brackets.sub(' ', types)

    # 불필요한 공백은 제거
    types = space.sub(' ', types)
    types = types.strip()
    
    # 클렌징 과정에서 type이 통째로 다른 항목으로 분류되었을 경우 default값 부여
    if types == '':
        types = '#'

    result =  dict(jsonString, **{'type': types, 'volume': volume, 'originalPrice' : originalprice, 'salePrice': saleprice, 'sale_status' : sale_status})
    
    return result

# 달러표시 및 천단위 콤마 표기
def cleansePrice(jsonString):
    brand = jsonString.get('brand')
    saleprice = jsonString.get('salePrice')
    originalprice = jsonString.get('originalPrice')
    
    if brand == 'TOMFORD': # 'tomford' 브랜드의 경우 달러 기호 포함
        nonDigit = re.compile(r'\D') # 숫자 아닌 문자 제거
        saleprice = nonDigit.sub('', saleprice)
        originalprice = nonDigit.sub('', originalprice)
        saleprice = '$' + '{:,}'.format(int(saleprice)) # 달러기호 추가 및 천단위 콤마 표기 포맷
        originalprice = '$' + '{:,}'.format(int(originalprice))
    elif saleprice != '#' and originalprice != '#': # 'tomford' 브랜드가 아니고 price가 default값이 아닌 경우
        saleprice = str(saleprice)
        originalprice = str(originalprice) 
        saleprice = nonDigit.sub('', saleprice) # 가격에 있는 숫자는 가격만을 의미한다고 가정. (ex : 3000원 (+500원) 이런 경우는 없다고 가정)
        originalprice = nonDigit.sub('', originalprice)
        if saleprice:
            saleprice = '{:,}'.format(int(saleprice))
        else:
            saleprice = '#'
        if originalprice:
            originalprice = '{:,}'.format(int(originalprice))
        else:
            originalprice = '#'
        
    result =  dict(jsonString, **{'salePrice': saleprice, 'originalPrice': originalprice})

    return result

# 최종 데이터 칼럼 13개: 'brand', 'name', 'category', 'image', 'url', 'color', 'type', 'volume', 'salePrice', 'orignialPrice', 'skuid', 'sale_status', 'eng_name'

