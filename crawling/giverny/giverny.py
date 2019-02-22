#!/usr/bin/env python
# coding: utf-8

# In[18]:


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

# In[19]:
driver = openChromedriver()

def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[20]:


driver.get("https://www.e-giverny.com/product/sublist.asp?branduid=3")
html = driver.page_source
soup = bs(html,'html.parser')
moreButton = soup.find('div',{'id':'more_btn'})
while moreButton['style'] != 'display: none;':
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    driver.find_element_by_id('more_btn').click()
    html = driver.page_source
    soup = bs(html,'html.parser')
    moreButton = soup.find('div',{'id':'more_btn'})
items = soup.find_all('div',{'class':'list_top'})


# In[48]:


base_url = 'https://www.e-giverny.com'
result_json = []
for idx, item in enumerate(items):
    print(idx)
    itemClass = {'name':'#', 'url':'#', 'image':[], 'color':'#', 'category':'#', 'volume':'#', 'type':'#', 'salePrice':'#', 'originalPrice':'#', 'brand':'지베르니'}
    driver.get(base_url + item.a['href'])
    html = driver.page_source
    soup = bs(html,'html.parser')
    itemClass['name'] = ''.join(soup.find('div',{'class':'infoBox'}).h1.contents[0].split()).replace("지베르니", "")
    itemClass['url'] = driver.current_url
    itemClass['originalPrice'] = ''.join(soup.find('div',{'class':'prd_mkprc'}).get_text().split())
    itemClass['salePrice'] = ''.join(soup.find('div',{'class':'prd_prc'}).em.get_text().split())
    infoOptions = soup.find_all('dl',{'class':'option_section'})
    for option in infoOptions:
        if option.dt.get_text() == "용량":
            itemClass['volume'] = option.dd.get_text()
            break
    images = soup.find('div', {'id': 'subImg'})
    images = images.find_all('img')
    #print(len(images.div.span))
    for i in images:
        itemClass['image'].append(base_url + i['src'])
    
    select = soup.find('select', {'class': 'select_fild'})
    if select is None:
        itemClass['color'] = '#'
        result_json.append(itemClass)
    else:
        colors = select.find_all('option')
        for color in colors:
            if color['value'] == "0":
                continue
            else:
                item_dict = copy.deepcopy(itemClass)
                item_dict['color'] = color.get_text()
                result_json.append(item_dict)

# driver.close()
# In[49]:


output = json.dumps(result_json,ensure_ascii=False, indent='\t')
writeJSON(output, output_name = 'giverny.json')


# In[ ]:




