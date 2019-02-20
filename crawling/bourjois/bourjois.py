#!/usr/bin/env python
# coding: utf-8

# # bourjois

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
    categories = soup.find('ul',{'id':'Category_Menu'}).find_all('li')
    categoryList = [url_home + category.a['href'] for category in categories]

    return categoryList    


# In[4]:


def readNextPage():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    nextPage_url = soup.find('a',{'class':'fa-angle-right'})['href']
    if '#' in nextPage_url:
        raise
    driver.get(url_products + nextPage_url)
        
    


# In[5]:


def getItemList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.find('div',{'id':'Product_ListMenu'}).find('ul',{'class':'ProductList Column3'}).find_all('li')
    itemList=[]
    for item in items:
        itemList.append(url_home + item.a['href'])
    return itemList


# In[6]:


def getItem(itemURL):
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()
    soup = bs(html, 'html.parser')

    name = soup.find('span',text='상품명').parent.parent.td.get_text().strip()
    images = soup.find('div',{'class':"xans-element- xans-product xans-product-addimage listImg"
                            }).ul.find_all('img',{'class':'ThumbImage'})
    imageList = ['http:'+image['src'] for image in images]

    category = soup.find('span',text='현재 위치').parent.ol.get_text().strip()
    
    volume = soup.find('td',text='용량')
    volume = volume.parent.get_text().strip()[2:].strip() if volume else '#'
    try:
        salePrice = getNumber(soup.find('strong',{'id':'span_product_price_text'}).get_text())
    except:
        salePrice = '#'
    originalPrice = soup.find('span',{'id':'span_product_price_custom'})
    originalPrice = getNumber(originalPrice.get_text()) if originalPrice else salePrice
    
    item={'name':'#', 'url':'#', 'image':'#', 'salePrice':'#', 'originalPrice':'#', 'color':'#', 'type':'#', 'category':'#', 'brand':'#','volume':'#'}
    item['name']  = name
    item['image'] = imageList
    item['category'] = ' > '.join(category.split())
    item['volume'] = volume
    item['salePrice'] = salePrice
    item['originalPrice']=originalPrice
    item['brand']='bourjois'
    item['url']=itemURL
    
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
        item['color']='#'
        items.append(item)
    return items


# In[7]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[8]:


driver = openChromedriver()

url_home = 'http://bourjois-mall.com'
url_products = 'http://bourjois-mall.com/product/list.html'


# In[9]:


driver.get(url_products)

categoryList = getCategoryList()
result = []
for category in categoryList:
    driver.get(category)
    itemList = []
    while True:
        itemList += getItemList()
        try:
            readNextPage()
        except:
            break
    for i, itemURL in enumerate(itemList):
        result += getItem(itemURL)


# In[10]:

driver.close()
output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'bourjois.json')


# In[ ]:




