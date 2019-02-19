#!/usr/bin/env python
# coding: utf-8

# # thefaceshop

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
    categories = soup.find('ul',{'class':'gnb_d2'}).find_all('li')

    categoryList = []
    for category in categories:
        categoryList.append(url_home + category.a['href'])
    return categoryList


# In[4]:


def clickSeeMoreButton():
    while True:
        try:
            seeMoreButton = driver.find_element_by_link_text('상품 더보기') 
            driver.execute_script('arguments[0].scrollIntoView(true);', seeMoreButton)
            seeMoreButton.click()
            time.sleep(3)
        except:
            break


# In[5]:


def getItemList():
    html = driver.page_source
    soup = bs(html,'html.parser')
    items = soup.find('ul',{'id':'prdtList'})
    itemList = []
    for i, item in enumerate(items):
        try:
            itemList.append(url_home + item.a['href'])
        except:
            pass
    return itemList


# In[6]:


def getItem(itemURL):
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()
    soup = bs(html, 'html.parser')

    name = soup.find('div',{'class':'page_title_2'}).span.get_text()

    imageList = soup.find('ul',{'class':'pn_container slide_thumb_list'}).find_all('li')
    images = [image.img['src'] for image in imageList]

    categoryList = soup.find('ul',{'class':'loc'}).find_all('li')
    category = ''
    for c in categoryList:
        category += c.get_text() + ' > '        
    category = category[:-3]

    volume = soup.find('span',string='용량/사이즈')
    volume = volume.parent.parent.td.get_text().strip()

    salePrice = getNumber(soup.find('span',{'class':'prdt_price_2'}).get_text())

    originalPrice = soup.find('span',{'class':'prdt_price_3'})
    originalPrice = getNumber(originalPrice.get_text()) if originalPrice else salePrice

    brand = 'thefaceshop'
    url = itemURL


    item = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':'#', 'type':'#', 'salePrice':'#', 'originalPrice':'#', 'brand':'#','volume':'#'}
    item['name']=name
    item['image']=images
    item['category']=category
    item['volume']=volume
    item['originalPrice']=originalPrice
    item['salePrice']=salePrice
    item['brand']=brand
    item['url']=url

    colors = soup.find_all('ul',{'class':'euiSelectList'})
    colors = colors[1].find_all('li') if colors else ''
    colors = [color.get_text().strip() for color in colors]

    items=[]
    if colors:
        for color in colors:
            item_copy = copy.deepcopy(item)
            item_copy['color'] = color
            items.append(item_copy)
    else:
        items.append(item)

    return items


# In[7]:


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)


# In[8]:


driver = openChromedriver()
url_home = 'http://thefaceshop.com'
url_products = 'http://www.thefaceshop.com/mall/product/category.jsp?cate_seq=7'
driver.get(url_products)


# In[9]:


start_time = time.time() 
#-------------------------------------------------------------#
categoryList = getCategoryList(url_products)
result = []
for category in categoryList:
    driver.get(category)
    clickSeeMoreButton()
    itemList = getItemList()
    totalItemNumber = getNumber(driver.find_element_by_xpath('//div[@class="result"]/span').text)
    print('상품 개수:', max(totalItemNumber,len(itemList))) # 총 상품 개수보다 표시된 상품 개수가 더 많은 경우도 존재
    if totalItemNumber > len(itemList):
        print('크롤링된 개수:',len(itemList))
        print('error')
        raise 

    for i, item in enumerate(itemList):
        print(i)
        result += getItem(item)

#-------------------------------------------------------------#
print("--- %0.2f seconds ---" %(time.time() - start_time))


# In[10]:


output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'thefaceshop.json')


# In[ ]:




