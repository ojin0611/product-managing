#!/usr/bin/env python
# coding: utf-8

# # skinfood

# In[6]:


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

# In[7]:


def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))
    


# In[8]:


def seeAllProducts():
    try:
        driver.find_element_by_xpath('//ul[@id="category"]/li[@class="first"]').click() # 전체상품 보기
    except:
        driver.find_element_by_xpath('//ul[@id="category"]/li[@class="first on"]').click() # 전체상품 보기


# In[9]:


def clickSeeMoreButton():
    while True:
        try:
            seeMoreButton = driver.find_element_by_id('moreA') 
            driver.execute_script('arguments[0].scrollIntoView(true);', seeMoreButton)
            seeMoreButton.click()
            time.sleep(1)
        except:
            break


# In[10]:


def getItemList():
    html = driver.page_source
    soup = bs(html,'html.parser')
    items = soup.find('ul',{'id':'tbodyList'})
    

    itemList = []
    for i, item in enumerate(items):
        try:
            itemList.append(url_home + item.a['href'])
        except:
            pass
    return itemList


# In[11]:


def getItem(itemURL):
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()
    soup = bs(html, 'html.parser')
    item = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':'#', 
                   'salePrice':'#', 'originalPrice':'#', 'brand':'#','volume':'#'}
    # name
    for i, name in enumerate(soup.find('h3',{'class':'productTitle'})):
        if i==2:
            item['name'] = name.strip()
            break

    # image
    item['image'] = 'http:'+soup.find('img',{'id':'productImg'})['src']

    # category
    categoryList = soup.find('div',{'class':'location'}).h2
    category=''
    for c in categoryList:
        if category:
            category += c.get_text().strip()
        else:
            category += c.get_text().strip()
            category += ' > '
    item['category']=category
    # volume
    item['volume'] = soup.find('li',{'class':'capacity'}).get_text().strip()

    # salePrice, originalPrice
    price = soup.find('span',{'id':'selPr'})
    for p in price:
        try:
            price_class = p['class']
            if price_class == ['text-del']:
                item['originalPrice'] = getNumber(p.get_text())
            elif price_class == ['price-pic']:
                item['salePrice'] = getNumber(p.get_text())
        except:
            continue
    if item['originalPrice']=='#':
        item['originalPrice']=item['salePrice']

    # brand
    item['brand'] = 'skinfood'

    # url 
    item['url'] = itemURL

    # color
    # 품절, 수량
    colors=[]
    items=[]
    colorList = soup.find('ul',{'class':'heapOptions'})
    if colorList:
        for i, color in enumerate(colorList):
            if i==0:
                continue
            color =  color.a['title'].strip()
            if '수량' in color:
                color = color[:color.find('수량')].strip()
            item_copy = copy.deepcopy(item)
            item_copy['color'] = color
            items.append(item_copy)
    else:
        items.append(item)

    return items


# In[12]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[13]:


driver = openChromedriver()

url_home = 'http://www.theskinfood.com'
url_products = 'http://www.theskinfood.com/goods/goodsList.do?catCd=4000000000&flag=4000000001&gubun=B'


# In[14]:


start_time = time.time() 
#-------------------------------------------------------------#
driver.get(url_products)
seeAllProducts()

clickSeeMoreButton()
result = []
itemList = getItemList()
itemList = list(set(itemList))
print('상품 개수 :',len(itemList))
for i, item in enumerate(itemList):
    # driver.get(item)
    print(i)
    result += getItem(item)
#-------------------------------------------------------------#
print("--- %0.2f seconds ---" %(time.time() - start_time))

driver.close()
# In[15]:


output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'skinfood.json')


# In[ ]:




