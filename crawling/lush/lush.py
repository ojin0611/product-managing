#!/usr/bin/env python
# coding: utf-8

# lush

from bs4 import BeautifulSoup as bs 
from selenium import webdriver
from urllib.request import urlopen
import json
import platform
import re
import time
import copy
import os

import sys
sys.path.append('../../modules')
from crawling_module import *



def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))


def getCategoryList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    categories = soup.find('div',{'class':'all-category-layer category db'}).div.ul.li.ul

    categoryList=[]
    for category in categories:
        if '베스트' in category.a.get_text():
            continue
        categoryList.append(url_home + category.a['href'][2:])    
    return categoryList


def getItemList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.find('ul',{'class':'prdList'}).find_all('li')
    itemList = []
    for item in items:
        itemList.append(url_home + item.a['href'][2:])
    return itemList


def readNextPage():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.find('ul',{'class':'pagination pagination-sm'})
    nextPage = False
    for item in items:
        if nextPage:
            driver.get(url_home +'/goods' + item.a['href'][1:])
            nextPage = False
        if not item.find('a'):
            nextPage = True
            if item.get_text() == str(len(items)):
                raise

def getItem(itemURL):
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()
    soup = bs(html, 'html.parser')
    item={}

    # name
    name = soup.find('div',{'class':'tit'}).get_text().strip()

    # image
    images = soup.find('div',{'class':'more-thumbnail'})
    images = images.find_all('span')

    imageList = []
    for image in images:
        imageList.append(url_home + image.img['src'])

    # category
    categories = soup.find('div',{'class':'path'}).find_all('div',{'class':'navi'})
    category = ''
    for c in categories:
        category += c.a.get_text().strip()+' > '
    category = category[:-3]

    # price
    salePrice = getNumber(soup.find('strong',text = ' 판매가').parent.div.strong.get_text())
    originalPrice = salePrice
    
    item = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':'#', 
                   'salePrice':'#', 'originalPrice':'#', 'brand':'#','volume':'#'}

    item['name']=name
    item['image']=imageList
    item['category']=category
    item['salePrice']=salePrice
    item['originalPrice']=originalPrice
    item['brand'] = 'lush'
    item['url'] = itemURL

    items = []    
    # volume
    volumes = soup.find('select',{'name':'optionSnoInput'})
    if volumes:
        volumes = volumes.find_all('option')
        for volume in volumes:
            volume = ''.join(volume.get_text().split())
            if '옵션' in volume:
                continue

            item_copy = copy.deepcopy(item)
            item_copy['volume'] = volume
            items.append(item_copy)
    else:
        items.append(item)
    return items



driver = openChromedriver()

url_home = 'https://lush.co.kr'
url_products = 'https://lush.co.kr/goods/goods_list.php?cateCd=001013'
driver.get(url_products)


categoryList = getCategoryList()
result = []
itemList = []
for category in categoryList:
    driver.get(category)
    while True:
        try:
            itemList += getItemList()
            readNextPage()
        except:
            break
    

driver.close()
itemList = list(set(itemList))
print('상품 개수 :', len(itemList))
for i, itemURL in enumerate(itemList):
    print(i)
    result += getItem(itemURL)


output = json.dumps(result,ensure_ascii=False, indent='\t')
writeJSON(output)




