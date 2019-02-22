#!/usr/bin/env python
# coding: utf-8

# # eglips

# In[3]:


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

# In[4]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[5]:


def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))
    


# In[6]:


def crawlingStart(driver, url_home):
    html = driver.page_source
    soup = bs(html,'html.parser')
    url_items = soup.find_all('div',{'class':'thumb'})
    url_page = soup.find('ol',{'class':'paging'}).find('a')['href']
    page_numbers = len(soup.find('ol',{'class':'paging'}).find_all('li'))

    result_json=[]
    for page in range(1,page_numbers):
        url = url_home+url_page[:-1]+str(page)
        print(page, 'page crawling start!')
        driver.get(url)

        html = driver.page_source
        soup = bs(html,'html.parser')
        url_items = soup.find_all('div',{'class':'thumb'})
        url_items = list(set(url_items))
        print('상품 개수 :',len(url_items))
        for i, url_item in enumerate(url_items):
            print(i)
            url = url_home + url_item.a['href']
            itemURL = url

            '''
            fp = urlopen(itemURL)
            html = fp.read().decode("utf8")
            fp.close()
            '''
            driver.get(itemURL)
            html = driver.page_source
            soup = bs(html,'html.parser')

            name = soup.find('div',{'class':'info'}).h3.get_text().strip()
            if '이글립스' in name:
                name = name[name.find('이글립스')+4:].strip()

            salePrice = soup.find('span',{'id':'pricevalue'})
            salePrice = getNumber(salePrice.get_text()) if salePrice else ''

            originalPrice = soup.find('strike')
            originalPrice = getNumber(originalPrice.get_text()) if originalPrice else salePrice
            image = url_home + soup.find('img',{'class':'detail_image'})['src']
            tblefts = soup.find_all('div',{'class':'tb-left'})
            volume_switch = False
            for tbleft in tblefts:
                if volume_switch:
                    volume = tbleft.get_text().strip()
                    volume_switch = False
                if '특이사항' in tbleft:
                    volume_switch = True
                    
            result = {'name':'#', 'url':'#', 'image':'#', 'salePrice':'#', 'originalPrice':'#', 'color':'#', 'category':'#', 'brand':'EGLIPS','volume':'#', 'type':'#'}

            result['name']=name
            result['salePrice']=salePrice
            result['originalPrice']=originalPrice
            result['image']=image
            result['volume']=volume
            result['url']=itemURL

            colors = soup.find_all('option')
            for color in colors:

                if '--옵션 선택--' not in color:
                    name_color = color.get_text().strip()
                    result_dict = copy.deepcopy(result)
                    result_dict['color']=name_color
                    result_json.append(result_dict)
    return result_json


# In[7]:


driver = openChromedriver()


# In[8]:


url_home = 'http://www.eglips.com'
url_products = 'http://www.eglips.com/shop/shopbrand.html?type=P&xcode=003'
driver.get(url_products)


# In[9]:


result_json = crawlingStart(driver, url_home)
driver.get(url_products)


# In[10]:
driver.close()

output = json.dumps(result_json,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'eglips.json')


# In[ ]:




