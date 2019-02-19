#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as bs              # 데이터파싱 라이브러리
from selenium import webdriver
import json
import re
import platform
import time

from urllib.request import urlopen
import sys
sys.path.append('../../modules')
from crawling_module import *

# In[2]:


def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))
    


# In[3]:


def getPrdCount(driver):
    html = driver.page_source
    soup = bs(html,'html.parser')
    prdCount = soup.find('p',{'class':'prdCount'})
    
    return getNumber(prdCount.get_text())
    


# In[4]:


def getItems(category, categoryname):
    driver.find_element_by_id(category).click()
    time.sleep(3)
    
    productsImages = driver.find_elements_by_class_name('prdImg')
    total_len = len(productsImages)
    prdCount = getPrdCount(driver)
    
    result_json = []
    
    for i in range(total_len - prdCount, total_len):
        result_dict = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':categoryname, 
                   'salePrice':'#', 'originalPrice':'#', 'brand':'woodbury','volume':'#'}
        productsImages = driver.find_elements_by_class_name('prdImg')
        productsImages[i].click()

        html = driver.page_source
        soup = bs(html,'html.parser')

        # 상품명, 가격 적힌 태그 뽑기
        tags = soup.find_all('tr',{'class':'xans-record-'})
        
        for tag in tags:
            if '상품명' in tag.get_text().strip():
                result_dict['name'] = tag.get_text().strip()[4:]
                
            elif '소비자가' in tag.get_text().strip():
                result_dict['originalPrice'] = getNumber(tag.get_text().strip()[5:])

            elif '판매가' in tag.get_text().strip():
                result_dict['salePrice'] = getNumber(tag.get_text().strip()[4:])
                if result_dict['originalPrice'] == '#':
                    result_dict['originalPrice'] = getNumber(tag.get_text().strip()[4:])
            
        # url, image 
        result_dict['url']  = driver.current_url
        result_dict['image'] = 'http:'+ soup.find_all('img',{'class':'BigImage'})[0]['src']
        
        # 색깔 개수만큼 output
        for j, item in enumerate(soup.find_all('option')):
            if j>1:
                color = ''.join(str(item.find(text=True)))
                if '-----' in color:
                    continue
                result_dict = result_dict.copy()
                result_dict['color'] = color 
                result_json.append(result_dict)

        driver.find_element_by_id(category).click()
        time.sleep(3)
        
    return result_json


# In[5]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[6]:

driver = openChromedriver()

# In[7]:


driver.get("http://woodbury.co.kr/")


# In[8]:


eyeLiner = 'cate_img_45'
eyeBrow = 'cate_img_46'
lipPencilTint = 'cate_img_49'
Mascara = 'cate_img_50'
baseMakeUp = 'cate_img_87'
concealer = 'cate_img_82'
accessory = 'cate_img_48'


# In[9]:


result = []
result += getItems(eyeLiner,'아이라이너')
result += getItems(eyeBrow,'아이브로우')
result += getItems(lipPencilTint,'립펜슬, 틴트')
result += getItems(Mascara,'마스카라')
result += getItems(baseMakeUp,'베이스 메이크업')
result += getItems(concealer,'컨실러')
result += getItems(accessory,'악세서리')


# In[10]:


output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'woodbury.json')


# In[ ]:




