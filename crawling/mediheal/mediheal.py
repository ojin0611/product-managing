#!/usr/bin/env python
# coding: utf-8

# # mediheal

# In[1]:


from bs4 import BeautifulSoup as bs              # 데이터파싱 라이브러리
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


# In[2]:


def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))
    


# In[3]:


def getCategoryList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    categories = soup.find('ul',{'class':'listWrap depthListWrap depth1'}).find_all('li')
    categoryList = [url_home + category.a['href'] for category in categories]
    categoryName = [category.get_text().strip() for category in categories]
    return categoryList, categoryName


# In[4]:


def getPageList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    pages = soup.find('div',{'class':'paginate'}).find_all('a')
    
    pageList = []
    for page in pages:
        pageList.append(url_home + page['href'])
    return list(set(pageList))


# In[5]:


def getItemList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.find_all('dl',{'class':'item-list'})
    itemList = [url_home + item.dt.a['href'] for item in items]
    
    return itemList


# In[6]:


def getItem(categoryName):
    html = driver.page_source
    soup = bs(html, 'html.parser')

    name = soup.find('div',{'class':'prdInfoWrap'}).h3.get_text().strip()
    if '메디힐' in name: name = name[name.find('메디힐')+3:].strip()
    image = url_home + soup.find('img',{'class':'originImg'})['src']
    
    # categoryName 위에서 받아오자
    category = categoryName
    
    volume = soup.find('span',text='용량 또는 중량')
    volume = volume.parent.parent.td.get_text().strip() if volume else '#'

    salePrice = getNumber(soup.find('span',{'class':'priceVal'}).get_text())
    
    originalPrice = soup.find('em',text='소비자가')
    originalPrice = getNumber(originalPrice.parent.span.get_text()) if originalPrice else salePrice


    item = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':'#', 'type':'#', 'salePrice':'#', 'originalPrice':'#', 'brand':'#','volume':'#'}
    item['name'] = name
    item['image']= image
    item['category']=category
    item['volume']=volume
    item['salePrice']=salePrice
    item['originalPrice']=originalPrice
    item['brand']='mediheal'
    item['url']=driver.current_url
    
    items=[]
    items.append(item)
    return items


# In[7]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[8]:


driver = openChromedriver()

url_home = 'http://www.medihealshop.com'
url_products = 'http://www.medihealshop.com/shop/shopbrand.html?xcode=003&type=X'


# In[9]:


driver.get(url_products)
result = []
categoryList, categoryName = getCategoryList()
for c,category in enumerate(categoryList):
    driver.get(category)
    pageList = getPageList()
    itemList = []
    cName = categoryName[c]
    for page in pageList:
        driver.get(page)
        itemList += getItemList()
    for i, item in enumerate(itemList):
        driver.get(item)
        result += getItem(cName)

driver.close()
# In[10]:


output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'mediheal.json')


# In[ ]:




