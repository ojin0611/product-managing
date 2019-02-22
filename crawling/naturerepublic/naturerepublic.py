#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup as bs              # 데이터파싱 라이브러리
from selenium import webdriver
from urllib.request import urlopen
import json
import platform, os, re, time, copy, sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

sys.path.append('../../modules')
from crawling_module import *

def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))
    

def getCategoryList(url_products):
    driver.get(url_products)
    html = driver.page_source
    soup = bs(html,'html.parser')
    categories = soup.find('ul',{'class':'tab_category'})
    categoryList = []
    for category in categories:
        try:
            categoryList.append(url_home + category.li.a['href'])
        except:
            pass

    return categoryList

# WebDriverWait(driver, 30).until_not(EC.presence_of_element_located((By.XPATH, "//a[@class='btn_more']")))

# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='paging_next']")))
def clickSeeMoreButton():
    html = driver.page_source
    soup = bs(html,'html.parser')
    seemore = soup.find('a',{'class':'btn_more arrow'})
    if seemore is None:
        return
    while not seemore.has_attr('style'):
        '''
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn_more']")))
        '''
        seeMoreButton = driver.find_element_by_class_name('btn_more')
        seeMoreButton.click()
        time.sleep(3)
        html = driver.page_source
        soup = bs(html,'html.parser')
        seemore = soup.find('a',{'class':'btn_more arrow'})

def getItemList():
    html = driver.page_source
    soup = bs(html,'html.parser')
    items = soup.find('ul',{'product_list contents_list'})
    itemList = []
    for item in items:
        try:
            itemList.append(url_home + item.a['href'])
        except:
            pass
    return itemList


def getItem(itemURL):
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()
    soup = bs(html, 'html.parser')
    name = soup.find('div',{'class':'sub_tit_wrap tit_pro_view'}).h2.get_text().strip()
    imageList = soup.find('div',{'class':'thumb_img'})
    images = [image['rel'] for image in imageList.ul.find_all('img')]

    categoryTexts = soup.find('div',{'class':'line-nav'}).find_all('a')
    category = ''
    for categoryText in categoryTexts:
        category += categoryText.get_text()+' > '
    category = category[:-3]

    volume = soup.find('dl',{'class':'volume'}).dd.get_text().strip()
    if not volume: volume = '#'

    price = soup.find('dl',{'class':'wrap-price-area money'}).find_all('dd')
    originalPrice = getNumber(price[0].get_text())
    if len(price)>1:
        salePrice = getNumber(price[1].get_text())
    else:
        salePrice = originalPrice

    brand = 'naturerepublic'

    url = itemURL

    item = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':'#', 
                   'salePrice':'#', 'originalPrice':'#', 'brand':'#','volume':'#'}
    item['name']=name
    item['image']=images
    item['category']=category
    item['volume']=volume
    item['originalPrice']=originalPrice
    item['salePrice']=salePrice
    item['brand']=brand
    item['url']=url

    items = []
    colors = soup.find('ul',{'class':'txt_img'})
    if colors:
        colors = [color.get_text().strip() for color in colors.find_all('li')]
        for color in colors:
            item_copy = copy.deepcopy(item)
            item_copy['color'] = color
            items.append(item_copy)
    else:
        items.append(item)
#    display(items)
    return items




driver = openChromedriver()

url_home = 'https://www.naturerepublic.com'
url_products = 'https://www.naturerepublic.com/shop/goods_list.php?cid=000000000000000&depth=0'
driver.get(url_products)


start_time = time.time() 
#-------------------------------------------------------------#
categoryList = getCategoryList(url_products)
result = []
itemList = []
for category in categoryList:
    driver.get(category)
    driver.execute_script("window.scrollTo(0, 0)") 
    clickSeeMoreButton()
    thisItemList = getItemList()
    itemList += thisItemList
    print('카테고리 상품 수:',len(thisItemList))

driver.close()
itemList = list(set(itemList))
print('전체 상품 수 :',len(itemList))        
for i, item in enumerate(itemList):
    print('%d' %(i+1))
    try:
        result += getItem(item)
    except:
        pass
        print('error url :',item)

#-------------------------------------------------------------#
print("--- %0.2f seconds ---" %(time.time() - start_time))

driver.close()
output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output)




