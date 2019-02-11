#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup as bs          
from selenium import webdriver
from urllib.request import urlopen
import json
import platform
import time
import copy
import os

import sys
sys.path.append('../')
from crawling import *


def readNextPage():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    pages = soup.find('div',{'class':'paginate'}).find_all('a')
    nextPage= False
    for page in pages:
        if nextPage:
            driver.get(url_products + page['href'])
            nextPage= False
        if page.find('strong'):
            nextPage= True

def getItemList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.find('div',{'id':'pro_list'}).ul.find_all('li')
    itemList=[]
    for item in items:
        itemList.append('http://www.cliocosmetic.com/ko/product/' + item.a['href'])

    return itemList

def seeDetailInfo(itemURL):
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()
    soup = bs(html, 'html.parser')
    seeDetail = soup.find('button',text='구매하러가기')['onclick']
    return seeDetail[seeDetail.find('http://'):-1]
    


def getItem(itemURL):
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()
    soup = bs(html, 'html.parser')

    info = soup.find('div',{'class':'info_area'})

    brandName = 'clio'

    name = info.find('div',{'class':'tit'}).get_text().strip()
    if brandName in name: name = name[len(brandName)+2:].strip()

    image = soup.find('img',{'id':'overimage'})['src']

    category = '#'

    volume = soup.find('th',text='용량 또는 중량').parent.td.get_text().strip()
    if not volume: volume = '#'

    salePrice = getNumber(info.find('em',{'class':'point'}).get_text())

    originalPrice = info.find('del')
    originalPrice = getNumber(originalPrice.get_text()) if originalPrice else salePrice


    item={'name':'#', 'url':'#', 'image':'#', 'salePrice':'#', 'originalPrice':'#', 'color':'#', 
                       'category':'#', 'brand':'#','volume':'#'}
    item['name'] = name
    item['image']= image
    item['category']=category
    item['volume']=volume
    item['salePrice']=salePrice
    item['originalPrice']=originalPrice
    item['brand']=brandName
    item['url']=driver.current_url

    items=[]
    colorList = soup.find('select',{'id':'O_1'})
    if colorList:
        colors = colorList.find_all('option')
        for color in colors:
            color = color.get_text().strip()
            if '옵션' in color:
                continue
            if '색상' in color:
                continue
            if '선택' in color:
                continue

            if 'NEW' in color:
                color = color[4:].strip()
                
            item_copy = copy.deepcopy(item)
            item_copy['color'] = color
            items.append(item_copy)
    else:
        item['color']='#'
        items.append(item)
    return items


path = 'chromedriver.exe' if (platform.system() == 'Windows') else '/Users/jg/Desktop/develop/DataTeam/DataProcessing/product/crawling/chromedriver'
driver = webdriver.Chrome(path)

url_home = 'http://www.cliocosmetic.com/ko/product/list.asp'
url_products = 'http://www.cliocosmetic.com/ko/product/list.asp'

driver.get(url_products)

itemList = []
while True:
    try:
        itemList += getItemList()
        readNextPage()
    except:
        break

itemList = list(set(itemList))
print('상품 개수 :', len(itemList))
result=[]
for i, itemURL in enumerate(itemList):
    print(i)
    itemURL = seeDetailInfo(itemURL)
    result += getItem(itemURL)

driver.close()
output = json.dumps(result,ensure_ascii=False, indent='\t')
writeJSON(output)


# In[ ]:




