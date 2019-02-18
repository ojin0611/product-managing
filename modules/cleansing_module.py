#%%
import json
import re

global ref

#%%
# 크롤링되지 않은 칼럼이 존재할 수 있음
def cleanseColumns1(jsonString):
    columnList = jsonString.keys()
    if 'category' not in columnList:
        jsonString = dict(jsonString, **{'category':'#'})
    #if 'url' not in columnList:
    #    jsonString = dict(jsonString, **{'url':'#'})
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
    return jsonString

#%%
# 브랜드명 클렌징 + 취급안하는 브랜드 제거 + skuid의 브랜드명 약어 부여
def cleanseBrand(jsonString):
    
    with open('./brandReference.json', encoding="UTF-8") as json_data: 
        ref = json.load(json_data)
  
    brand = jsonString.get('brand')
    brandList = list(ref.get('영문명').values()) # 취급 브랜드의 영문명 리스트
    abbList = list(ref.get('약어').values()) # 브랜드 약어 리스트
    
    p = re.compile(r'\s+') #띄어쓰기 없음
    brand = re.sub(p, '',brand) 
    brand = brand.upper() #영문 대문자 표기
    
    if brand not in brandList:
        return None
    
    # skuid 브랜드 약어 부분 부여
    else:
        idx = brandList.index(brand)
        skuid = abbList[idx]
        result = dict(jsonString, **{'brand': brand, 'skuid': skuid})
    
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
        sale_status = '*'
    # 세트 이름에서 지워야하나?
    # name = p.sub(' ', name)
        

    # 할인 여부 구별 -> 할인으로 구분되지 않은 상품 존재할 수 있음
    p = re.compile('sale|할인|세일', re.I)
    if p.search(name) and sale_status != '*':
        sale_status += '/할인'
    elif p.search(name) and sale_status == '*':
        sale_status = '할인'
    elif sale_status != '*':
        pass
    else:
        sale_status = '*'
    name = p.sub(' ', name)

    
    # 불필요한 수식어와 특수기호 제거 -> 별표사이사이에 있는 문구 삭제? ex)★~가 추천한 상품★   [리미티드] 추가하면 안됨.->리/미/티/드 다 제거
    p = re.compile(r'<br>|#디렉터파이_추천!|★겟잇뷰티 1위!★|(최대3개구매가능)|온라인 단독|온라인|online|사은품 : 샤워볼|기획세트|기획 세트|기획', re.I)
    name = p.sub(' ', name)
    p = re.compile(r'리미티드|★리미티드★|[[]리미티드[]]|한정|한정판|행사|event|이벤트|1[+]1|1 [+] 1|☆|추천|!|@|^|new\s|[[]new[]]|_|-', re.I)
    # * () [] / , .  _ 제외 특수기호 ? \W
    name = p.sub(' ', name)
    
    # 제품이름에 volume 포함 경우
    p = re.compile(r'(.*)[(]([^)]*(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs).*)[)](.*)')
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
    
    p = re.compile(r'\d+(\s)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I)
    if p.search(name) and volume == '#':
        m = p.search(name)
        volume = m.group()
    name = p.sub(' ', name)
    # \d+(\s)?ml(\s)?[*](\s)?\d+매
    # \d+(\s)?ml[^+]
    # \d+(\s)?mg|\d+(\s)?g|\d+(\s)?oz|\d+(\s)?매|\d+(\s)?매입|\d+(\s)?ea|\d+(\s)?each
    
    
    # 제품이름에 type (대용량/리필) 포함 경우
    p = re.compile(r'대용량|소용량|리필 포함|리필용|본품+리필구성|본품+리필|리필|(대용량)|(리필)')
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
    p = re.compile(r'(.*[가-힣].*?)\s?([^가-힣][a-zA-Z]*)+$')
    p2 = re.compile('spf|pa', re.I) # SPF00+ PA+ 부분을 영문명으로 인식하지 않도록
    if p.search(name):
        en = p.sub(r'\2', name) 
        if p2.search(en):
            eng_name = '*'
        else:
            eng_name = en 
            name = p.sub(r'\1', name)  # 이 부분을 eng_name 지정하는 윗줄보다 먼저 쓰면 안됨 
    else:
        eng_name = '*'
    
    # RMK 스펀지(UV) RMK SPONGE(UV) -> name = RMK 스펀지, eng_name = (UV) RMK SPONGE(UV) 이런 경우 해결
    if eng_name != '*':
        enlist = eng_name.split()
        if len(enlist) > len(set(enlist)):
            i = len(enlist) - len(set(enlist))
            name = name + ' ' + enlist[i-1]
            eng_name = ' '.join(enlist[i:])
    
    # 괄호들 제거
    #p = re.compile(r'[(]([^)]*)[)]|[[]([^]]*)[]]|[<]([^>]*)[>]|[{]([^>]*)[}]') # (), [], <>, {}
    p = re.compile(r'[[]|[]]|[(]|[)]|[<]|[>]|[{]|[}]')
    if p.search(name):
        name = p.sub(' ', name)

    # 한 칸 이상의 공백 제거
    p = re.compile(r'\s+')
    name = p.sub(' ', name)
    name = name.strip() # 앞뒤 공백 제거
    eng_name = p.sub(' ', eng_name)
    eng_name = eng_name.strip()


    # sale_status칼럼: 세일상품, 할인, 세일상품/할인 -> 3가지 값
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
            p = re.compile(r'([가-힣]+.*?)\s?(\d+)\s?((ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs))')
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


def cleanseColor(jsonString):
    
    color = jsonString.get('color')
 
    #1-1 특수문자/수식어 하나하나 따로 제거할 경우..
    p = re.compile(r'new\s|추천|-|_', re.I) # 제거하고 싶은 단어 추가  renewal 주의
    color = p.sub(' ', color) # space 한 칸 줘야 한글끼리, 영어끼리 띄어쓰기가 유지됨. 하지만 필요 이상의 공백이 생길 수 있으므로 한칸 이상 공백 제거하는 식 필요
    
    #2 문자와 숫자는 띄어쓰기로 구분  -> 'A01 레드' 경우 ? 
    p1 = re.compile(r'([가-힣a-zA-Z]+)(\S\d+)') # 문자+숫자 사이 띄어쓰기
    color = p1.sub(r'\1 \2', color)
    p2 = re.compile(r'(\d+)(\S[가-힣a-zA-Z]+)') # 숫자+문자 사이 띄어쓰기
    color = p2.sub(r'\1 \2', color)

    #3 한글 영문 동시 기재시 한글을 앞으로
    p = re.compile('([a-zA-Z]+.*?)([가-힣]+)')
    color = p.sub(r'\2 \1', color)
    
    # 괄호 안 부가설명 있을 경우 (품절, 가격변동)
    p = re.compile(r'품절')


    # 한 칸 이상의 공백은 제거
    p = re.compile(r'\s+')
    color = p.sub(' ', color)
    color = color.strip()
    
    result =  dict(jsonString, **{'color': color})
    
    return result

def cleanseType(jsonString):
    
    types = jsonString.get('type')
    
    #1-1 특수문자/수식어 하나하나 따로 제거할 경우..
    p = re.compile(r'new\s|추천', re.I) # 제거하고 싶은 단어 추가  renewal 주의
    types = p.sub(' ', types) # space 한 칸 줘야 한글끼리, 영어끼리 띄어쓰기가 유지됨. 하지만 필요 이상의 공백이 생길 수 있으므로 한칸 이상 공백 제거하는 식 필요
    
    #2 문자와 숫자는 띄어쓰기로 구분
    p1 = re.compile(r'([가-힣a-zA-Z]+)(\S\d+)') # 문자+숫자 사이 띄어쓰기
    types = p1.sub(r'\1 \2', types)
    p2 = re.compile(r'(\d+)(\S[가-힣a-zA-Z]+)') # 숫자+문자 사이 띄어쓰기
    types = p2.sub(r'\1 \2', types)

    #3 한글 영문 동시 기재시 한글을 앞으로
    p = re.compile('([a-zA-Z]+.*?)([가-힣]+)')
    types = p.sub(r'\2 \1', types)
    
    # 괄호 안 부가설명 있을 경우
    
    # 한 칸 이상의 공백은 제거
    p = re.compile(r'\s+')
    types = p.sub(' ', types)
    types = types.strip()
    
    result =  dict(jsonString, **{'type': types})
    
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
    elif saleprice != '#' and originalprice != '#':
        saleprice = '{:,}'.format(int(saleprice))
        originalprice = '{:,}'.format(int(originalprice))
        
    result =  dict(jsonString, **{'salePrice': saleprice, 'originalPrice': originalprice})
    
    return result

def cleanseColumns2(jsonString):
    columnList = jsonString.keys()
    if 'sale_status' not in columnList:
        jsonString = dict(jsonString, **{'sale_status':'*'})
   
    return jsonString

# 최종 데이터 칼럼 13개: 'brand', 'name', 'category', 'image', 'url', 'color', 'type', 'volume', 'salePrice', 'orignialPrice', 'skuid', 'sale_status', 'eng_name'

#%%
sample = {'name':'[클리오] [텍스쳐도 용량도 UP!]킬커버 팟 컨실러','volume':'#', 'brand':'clio','category':'카테고리','type':'#'}
sample = cleanseColumns1(sample)
s=cleanseBrand(sample)
s=cleanseName(s)
cleanseVolume(s)

#%%
# 제품이름에 volume 포함 경우
def test(name):
    p = re.compile(r'\d+(\s)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)(\s?[*|+|x]\s?\d+)?(ml|mg|mm|g|oz|매입|개입|매|개|입|each|ea|pcs)?', re.I)
    if p.search(name):
        volumes = p.findall(name)

        #volume = ' '.join(volumes)
    #name = p.sub(' ', name)
    return volumes #{'name':name, 'volume':volume}
test('로맨틱 체리블러섬 퍼퓸 바디워시 기획(체리 900g 2입 + 체리 120g)')