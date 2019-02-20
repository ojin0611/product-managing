#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import platform
import re
import time
import copy

from urllib.request import urlopen
import sys
sys.path.append('../../modules')
from crawling_module import *

def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))
    


def getCategoryList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    categories = soup.find('ul',{'class':'menuCategory'}).find_all('a')
    categoryList=[]
    categoryNameList =[]
    for category in categories:
        categoryList.append(url_home + category['href'])
        categoryNameList.append(category.get_text().strip()[:-2].strip())
    return categoryList, categoryNameList



def getItemList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.find('ul',{'class':'prdList grid4 april_list'}).find_all('div',{'class':'thumbnail'})
    itemList=[]
    for item in items:
        itemList.append(url_home + item.a['href'])

    return itemList




def getItem(categoryName, itemURL):
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()
    soup = bs(html, 'html.parser')
    item={}

    name = soup.find('div',{'class':'infoArea'}).h2.get_text().strip()

    imageList = soup.find('div',
        {'class':'xans-element- xans-product xans-product-addimage listimg2'}).ul.find_all('li')
    images = ['http:'+image.img['src'] for image in imageList]

    category = categoryName

    volume = '#'

    salePrice = getNumber(soup.find('strong',{'id':'span_product_price_text'}).get_text())
    try:
        originalPrice = getNumber(soup.find('span',{'id':'span_product_price_custom'}).get_text())
    except:
        originalPrice = salePrice

    item['name']=name
    item['image']=images
    item['category']=category
    item['volume']=volume
    item['salePrice']=salePrice
    item['originalPrice']=originalPrice
    item['brand'] = 'aprilskin'
    item['url'] = itemURL

    items=[]

    colorList = soup.find('th',text='색상')
    if colorList:
        colorList = colorList.parent.td.find_all('option')
        for color in colorList:
            color = color.get_text().strip()
            if '-----' in color:
                continue
            if '옵션을' in color:
                continue

            item_copy = copy.deepcopy(item)
            item_copy['color'] = color.strip()
            items.append(item_copy)

    else:
        item['color']='#'
        items.append(item)

    return items



def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)



driver = openChromedriver()

url_home = 'http://aprilskin.com'
url_products = 'http://aprilskin.com/product/list.html?cate_no=48'



driver.get(url_products)
result=[]

categoryList, categoryNameList = getCategoryList()
for c,category in enumerate(categoryList):
    driver.get(category)
    categoryName = categoryNameList[c]
    itemList = getItemList()
    for i, itemURL in enumerate(itemList):
        print(i)
        result += getItem(categoryName, itemURL)


driver.close()

output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'aprilskin.json')





