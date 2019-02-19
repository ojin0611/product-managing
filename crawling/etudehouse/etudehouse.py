#!/usr/bin/env python
# coding: utf-8

# # etudehouse

# In[1]:


from bs4 import BeautifulSoup as bs              # 데이터파싱 라이브러리
from selenium import webdriver
import json
import platform
import re
import time
import copy
from selenium.webdriver.support.ui import WebDriverWait

from urllib.request import urlopen
import sys
sys.path.append('../../modules')
from crawling_module import *

# In[2]:


def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))
    


# In[3]:


def getCategoryList(url_products):
    driver.get(url_products)
    html = driver.page_source
    soup = bs(html,'html.parser')
    categories = soup.find('dl',{'class':'focus_target'}).dd.ul.find_all('li')
    categoryList = [url_home + category.a['href'] for category in categories]
    categoryNameList = [category.a.get_text() for category in categories]
    return categoryList, categoryNameList


# In[4]:


def clickNextPage():
    html = driver.page_source
    soup = bs(html,'html.parser')
    nextPage = soup.find('a',{'class':'navi next'})
    if nextPage:
        driver.find_element_by_link_text('next page').click()
    else:
        raise


# In[5]:


def getItemList():
    html = driver.page_source
    soup = bs(html,'html.parser')
    items = soup.find('div',{'class':'item_list column2'}).find_all('div',{'class':'item item-apply'})
    itemList = [url_home + item.find('div',{'class':'item_images'}).a['href'] for item in items]
        
    return itemList


# In[6]:


def getItem(categoryName, itemURL):
    html = driver.page_source
    '''
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()
    '''
    soup = bs(html, 'html.parser')
    print(itemURL)
    name = soup.find('h3',{'class':'h_title'}).get_text().strip()
    images = soup.find('div',{'class':'prd_thm_wrap preview_thumbs'}).find_all('img')
    imageList = [image['src'] for image in images]
    category = categoryName
    volume = soup.find('th',text='용량')
    volume = volume.parent.td.get_text() if volume else '#'
    originalPrice = getNumber(soup.find('span',{'class':'price'}).get_text())
    salePrice = originalPrice
    brand = 'etudehouse'
    url = itemURL
    colors = soup.find('button',text='옵션선택')
    if colors: 
        image_colors = colors.parent.find_all('img')
        image_colorList = [image_color['src'] for image_color in image_colors] if image_colors else []
    colors = colors.parent.ul.find_all('code') if colors else '#'
    colorList = [color.get_text().strip() for color in colors] if colors != '#' else '#'
    pd_type = soup.find('th',text='제품 주요 사양 - 피부타입, 색상(호,번)등')
    pd_type = pd_type.parent.td.get_text() if pd_type else '#'
    
    
    item = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':'#', 
                   'salePrice':'#', 'originalPrice':'#', 'brand':'#','volume':'#','type':'#'}
    item['name']=name
    item['image']=imageList
    item['category']=category.strip()
    item['volume']=volume.strip()
    item['originalPrice']=originalPrice
    item['salePrice']=salePrice
    item['brand']=brand
    item['url']=url
    item['type']=pd_type.strip()

    items = []
    if colorList != '#':
        for co, color in enumerate(colorList):
            item_copy = copy.deepcopy(item)
            item_copy['color'] = color.strip()
            if image_colorList:
                item_copy['image'].append(image_colorList[co])
            items.append(item_copy)
    else:
        items.append(item)
    print(item['name'])
    return items


# In[7]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[8]:


driver = openChromedriver()

url_home = 'https://www.etudehouse.com'
url_products = 'https://www.etudehouse.com/kr/ko/main'


# In[9]:


start_time = time.time() 
#---------------------------------------------------------------------#
driver.get(url_products)
categoryList, categoryNameList = getCategoryList(url_products)
result = []
for c, category in enumerate(categoryList):
    driver.get(category)
    categoryName = categoryNameList[c]
    itemList = []
    while True:
        try:
            newItemList = getItemList()
            if len(newItemList)==0:
                time.sleep(2)
                continue
                
            if newItemList[0] not in itemList:
                itemList += newItemList
                clickNextPage()
            else:
                time.sleep(2)
                continue
            
        except:
            break
    
    itemList = list(set(itemList))
    print('상품 개수 :', len(itemList))
    for i,item in enumerate(itemList):
        print(i)
        driver.get(item)
        result += getItem(categoryName, item)
    
#---------------------------------------------------------------------#
print("--- %0.2f seconds ---" %(time.time() - start_time))


# In[10]:


output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'etudehouse.json')


# In[ ]:




