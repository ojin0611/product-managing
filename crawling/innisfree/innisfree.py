#!/usr/bin/env python
# coding: utf-8

# # innisfree

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


def getCategories(driver):
    driver.get(url_products)    # click main page
    html = driver.page_source
    soup = bs(html,'html.parser')
    categories = driver.find_elements_by_xpath("//ul[@class='tabArea']/li/a")
    for c, category in enumerate(categories):
        categories[c]=category.text
    return categories


# In[4]:


def clickCategory(driver, category):
    target = driver.find_element_by_link_text(category)
    driver.execute_script('arguments[0].scrollIntoView(true);', target)
    target.click()
#    return driver


# In[5]:


def getItems(driver):
    # after click category
    html = driver.page_source 
    soup = bs(html,'html.parser')
    items = soup.find_all('span',{'class':'prdWrap'})
    return items # item.a['href']를 통해 링크 얻기


# In[6]:


def getItem(driver, url, category):
    # Start!
    fp = urlopen(url)
    html = fp.read().decode("utf8")
    fp.close()
    
    soup = bs(html,'html.parser')

    result_json = []

    #name
    name = soup.find('p',{'class':'pdtName'}).get_text().strip()
    
    #image
    images = soup.find('ul',{'class':'imgList'}).find_all('img')
    images = [image['src'] for image in images]

    # color, price
    isOption = False
    selectArea = soup.find_all('div',{'class':'selectArea'})
    for select in selectArea:
        if select.button['id']=='selTitOpt': 
            options = select.find('ul',{'class':'selList'}).find_all('li')
            options = [option.get_text().strip() for option in options]
            isOption = True

        if select.button['id']=='selTitAdd': 
            additions = select.find('ul',{'class':'selList'}).find_all('li')
            additions = [addition.get_text().strip() for addition in additions]

    if isOption:
        price = soup.find('p',{'id':'pdtPrice'})
        price = getNumber(price.get_text()) if price else ''

    else:
        price = soup.find('p',{'id':'sum'})
        price = getNumber(price.get_text()) if price else ''


    # dictionary 생성
    result = {'name':'#', 'url':'#', 'image':'#', 'salePrice':'#', 'originalPrice':'#', 'type':'#', 'color':'#', 'category':'#', 'brand':'innisfree','volume':'#'}

    result['name']=name
    result['url']=url
    result['image']=images
    result['salePrice']=price
    result['originalPrice']=price
    result['category']=category

    # JSON으로 저장
    if isOption:
        for option in options:
            if '- 일시품절' in option:
                option = option[:-7]
            result_dict = copy.deepcopy(result)
            result_dict['color']=option
            result_json.append(result_dict)
    else:
        result_dict = copy.deepcopy(result)
        result_json.append(result_dict)
    
    return result_json


# In[7]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[8]:

driver = openChromedriver()

url_home = 'http://www.innisfree.com'
url_products = 'http://www.innisfree.com/kr/ko/ShopProductMap.do'
driver.get(url_products)
categories = getCategories(driver)


# In[9]:


start_time = time.time() 
#-------------------------------------------------------------#
result_json = []
for category in categories:
    category=category.strip()
    clickCategory(driver,category)
    time.sleep(3)
    print('category :', category)
    
    items = getItems(driver)
    print('상품 개수 :', len(items))
    for i, item in enumerate(items):
        print(i)
        url = url_home + item.a['href']
        result_json += getItem(driver,url,category)

    driver.get(url_products)
    time.sleep(3)
#-------------------------------------------------------------#
print("--- %s seconds ---" %(time.time() - start_time))


# In[10]:


output = json.dumps(result_json,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'innisfree.json')


# In[ ]:




