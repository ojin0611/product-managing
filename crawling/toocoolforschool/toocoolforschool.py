#!/usr/bin/env python
# coding: utf-8

# # toocoolforschool

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
    categories = soup.find('ul',{'class':'menulist'}).find_all('li') # 사이트마다 다름
    categoryList=[]
    for category in categories:
        if '신제품' in category.get_text():
            continue
        if '베스트' in category.get_text():
            continue
        categoryList.append(url_home + category.a['href'])
    return categoryList


# In[4]:


def getItemList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.find('div',{'class':'product_line'}).ul.find_all('li') # 사이트마다 다름
    itemList=[]
    for item in items:
        itemList.append(url_home + '/shop'+item.a['href'][2:])

    return itemList


# In[5]:


def goToNextPage():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    try:
        nextPage = url_home + soup.find('a',{'class':'next2'})['href']
        driver.get(nextPage)
        return True
    except:
        return False


# In[6]:


def getCategoryItemList():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    goto = True
    itemList = []
    while goto:
        itemList += getItemList()
        goto = goToNextPage()
    return itemList


# In[7]:


def getItem(itemURL):
    html = driver.page_source
    soup = bs(html, 'html.parser')
    item = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':'#', 
                   'salePrice':'#', 'originalPrice':'#', 'brand':'#','volume':'#'}
    item['name'] = soup.find('p',{'class':'title_en'}).get_text().strip()
    image = soup.find('img',{'id':'objImg'})['src']

    item['image'] = url_home + '/shop' + image[2:]

    categoryList = soup.find('div',{'id':'path'}).ul.find_all('li')
    category=''
    for c in categoryList:
        if len(category)<1:
            pass
        else:
            category += ' > '
        category += c.get_text().strip()
    item['category'] = category
    
    item['volume'] = soup.find('th',text='용량 및 규격').parent.td.get_text().strip()
    
    price = soup.find('div',{'class':'value'})
    salePrice = getNumber(price.find('input')['value'])
    originalPrice = price.find('del')
    originalPrice = getNumber(originalPrice.get_text()) if originalPrice else salePrice
    item['originalPrice'] = originalPrice
    item['salePrice'] = salePrice
    
    item['brand'] = 'toocoolforschool'
    
    item['url'] = itemURL

    colorList = soup.find('select',{'name':'opt[]'})
    items=[]
    if colorList:
        colorList = colorList.find_all('option')
        for c, color in enumerate(colorList):
            if c==0:
                continue
            item_copy = copy.deepcopy(item)
            item_copy['color'] = color.get_text().strip() 
            items.append(item_copy)
    else:
        items.append(item)

    return items


# In[8]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[9]:

driver = openChromedriver()
url_home = 'http://www.toocoolforschool.com'
url_products = 'http://www.toocoolforschool.com/shop/goods/goods_list.php?&category=001'


# In[10]:


driver.get(url_products)
result= []
categoryList = getCategoryList()
for category in categoryList:
    driver.get(category)
    itemList=[]
    itemList += getCategoryItemList()
    itemList = list(set(itemList))
    print('상품 개수 :', len(itemList))
    for i, item in enumerate(itemList):
        print(i)
        driver.get(item)
        result += getItem(item)


# In[11]:


output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'toocoolforschool.json')


# In[ ]:




