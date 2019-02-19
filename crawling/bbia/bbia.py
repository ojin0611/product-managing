#!/usr/bin/env python
# coding: utf-8

# In[218]:


from bs4 import BeautifulSoup as bs              # 데이터파싱 라이브러리
from selenium import webdriver
import json
import platform
import re
import copy

from urllib.request import urlopen
import sys
sys.path.append('../../modules')
from crawling_module import *

# In[219]:


driver = openChromedriver()


# In[220]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[223]:


driver.get("http://www.bbia.co.kr/shop/shopbrand.html?xcode=007&mcode=001&type=X")
page = driver.find_element_by_class_name('item-page').text
page = ''.join(page.split())


# In[224]:


driver.get("http://www.bbia.co.kr/shop/shopbrand.html?xcode=007&mcode=002&type=X")
page2 = driver.find_element_by_class_name('item-page').text
page2 = ''.join(page2.split())


# In[232]:


def getCategoryItem(mcode='001',pageNumber=1):
    result_json = []
    # item 설정
    

    for i in range(1, pageNumber+1):
        driver.get("http://www.bbia.co.kr/shop/shopbrand.html?xcode=007&mcode={0}&sort=&page={1}".format(mcode,i))
        html = driver.page_source
        soup = bs(html,'html.parser')
        items = soup.find_all('div',{'class':'prd-thumb'})
        for item in items:
            itemClass = {'name':'', 'url':'', 'image':[], 'color':'#', 'volume':'#','category':'#', 'salePrice':'#', 'originalPrice':'#', 'brand':'삐아', 'type':'#'}
            driver.get('http://www.bbia.co.kr/' + item.a['href'])
            html = driver.page_source
            soup = bs(html,'html.parser')
            itemClass['name'] = soup.find('div',{'class':'titlearea'}).h2.get_text()
            itemClass['url'] = driver.current_url
            itemClass['image'].append('http://www.bbia.co.kr/' + item.img['src'])
            
            if soup.find('span',{'id':'pricevalue'}):
                itemClass['salePrice'] = ''.join(soup.find('span',{'id':'pricevalue'}).get_text().split())
                itemClass['originalPrice'] = ''.join(soup.find('strike').get_text().split()) if soup.find('strike') else itemClass['salePrice']
            else:
                itemClass['originalPrice'] = ''.join(soup.find('div',{'class':'prd-price'}).get_text().split())
                itemClass['salePrice'] = itemClass['originalPrice']
            color = []
            color = soup.find_all('option')
            selection = soup.find('select')
            if len(color) != 0 and (selection.get('style') is None or (selection.get('style') and selection['style'] != "display: none;")):
                for option in color:
                    item_dict = copy.deepcopy(itemClass)
                    if option.get_text() != "--옵션 선택--":
                        item_dict['color'] = option.get_text()
                        result_json.append(item_dict)
            else:
                item_dict = copy.deepcopy(itemClass)
                item_dict['color'] = '#'
                result_json.append(item_dict)
    return result_json


# In[234]:


result = []
result += getCategoryItem('001',len(page))
result += getCategoryItem('002',len(page2))


# In[235]:


output = json.dumps(result,ensure_ascii=False, indent='\t')
writeJSON(output, output_name = 'bbia.json')


# In[ ]:




