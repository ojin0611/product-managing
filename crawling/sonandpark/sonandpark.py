#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup as bs              # 데이터파싱 라이브러리
from selenium import webdriver
import json
import platform
import re
import time
import copy

import sys
sys.path.append('../../modules')
from crawling_module import *


def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))


def getItemList():
    itemList = []
    while True:
        html = driver.page_source
        soup = bs(html, 'html.parser')
        items = soup.find('div',{'class':
                    'xans-element- xans-product xans-product-listnormal ec-base-product'}).ul
        
        for item in items.find_all('li'):
            if item.has_attr('id'):
                hrefs = item.div.div.find_all('a')
                for href in hrefs:
                    if href.has_attr('href'):
                        itemList.append(url_home + href['href'])

        
        nextPage = soup.find('img',{'alt':'다음 페이지'}).parent['href']
        if '?' in nextPage:
            driver.get(url_products + nextPage)
        else:
            break
            
    return itemList


def getItem():
    html = driver.page_source
    soup = bs(html, 'html.parser')

    name = soup.find('div',{'class':'headingArea'}).h2.get_text()
    
    image = 'http:'+soup.find('img',{'class':'BigImage'})['src']
            
    salePrice = getNumber(soup.find('strong',{'id':'span_product_price_text'}).get_text())
    originalPrice = soup.find('span',{'id':'span_product_price_custom'})
    originalPrice = getNumber(originalPrice.get_text()) if originalPrice else salePrice

    brand = 'sonandpark'
    
    url = driver.current_url
    
    item = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':'#', 
                   'salePrice':'#', 'originalPrice':'#', 'brand':'#','volume':'#'}
    item['name'] = name
    item['image']= image
    item['salePrice']=salePrice
    item['originalPrice']=originalPrice
    item['brand']=brand
    item['url']=url
    
    items=[]
    colors = soup.find('select',{'id':'product_option_id1'})
    if colors:
        colorList = []
        colors = soup.find('select',{'id':'product_option_id1'}).find_all('option')
        for color in colors:
            color = color.get_text().strip()
            if '필수' in color:
                continue
            if '------' in color:
                continue
            if '품절' in color:
                color = color[:color.find('[품절')].strip()
            item_copy = copy.deepcopy(item)
            item_copy['color'] = color
            items.append(item_copy)
    
    else:
        items.append(item)

    return items


driver = openChromedriver()
'''
path = 'chromedriver.exe' if (platform.system() == 'Windows') else '/Users/jg/Desktop/develop/DataTeam/DataProcessing/product/crawling/chromedriver';
driver = webdriver.Chrome(path)
'''
url_home = 'http://sonandpark.com'
url_products = 'http://sonandpark.com/category/all/48/'


driver.get(url_products)
itemList = getItemList()

result = []
for i, item in enumerate(itemList):
    driver.get(item)
    result += getItem()
    print(i)

driver.close()

output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output)





