#!/usr/bin/env python
# coding: utf-8

# In[124]:


from bs4 import BeautifulSoup as bs              # 데이터파싱 라이브러리
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
import json
import platform
import re
import time
import copy

from urllib.request import urlopen
import sys
sys.path.append('../../modules')
from crawling_module import *




def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)




def getUrlList():
    urlList = []
    for category in categorys:
        #카테고리별로 접속
        driver.get("http://apieu.beautynet.co.kr/goods.list.do?upperDisplayCategoryNumber=" + str(category) + "&displayCategoryNumber=0")
        
        #상품 긁기
        while True:
            html = driver.page_source
            soup = bs(html,'html.parser')
            products = driver.find_elements_by_xpath("//p[@class='pname']//a")
            for product in products:
                urlList.append(product.get_attribute("href"))
            try:
                driver.find_element_by_xpath("//a[@class='nextBtn']").click()
            except NoSuchElementException:
                break
    return urlList
        
        #다음 페이지가 있으면 다음 페이지로 이동

driver = openChromedriver()

#categorys = [115015010000]
categorys = [115015007000, 115015008000, 115015017000, 115015015000, 115015014000, 115015009000, 115015010000, 120000000328, 120000000333, 115015013000]

urlList = getUrlList()
driver.close()

urlList = list(set(urlList))
print(len(urlList))



def getItemDetailByUrl(urlList):
    driver = openChromedriver()
    result_json = []
    for idx, item in enumerate(urlList):
        driver.get(item)
        html = driver.page_source
        soup = bs(html,'html.parser')
        # dictionary 생성
        result = {'name':'', 'url':'', 'image':'', 'salePrice':'', 'originalPrice':'', 'color':'', 
                   'category':'', 'brand':'어퓨','volume':''}
        
        fullName = soup.find('h2',{'id':'goodsProdName'}).get_text().strip('[어퓨]')
        checkContainsColor = fullName.find('[')
        if checkContainsColor == -1:
            result['name'] = fullName
            result['color'] = "#"
        else:
            result['name'] = fullName[:checkContainsColor]
            result['color'] = fullName[checkContainsColor + 1: len(fullName)]
        
        result['url'] = driver.current_url
        categorys = []
        findCategory = soup.find('div',{'class':'tit_path'}).find_all('li')
        for category in findCategory:
            categorys.append(category.get_text().strip('\n'))
        result['category'] = '>'.join(categorys)
        
        #컬러가 있는지 체크
#         if soup.find('div', {'class':'colorList'}) is None:
            #단품
        images = driver.find_elements_by_xpath("//ul[@class='simg']//li//a//img")
        result['image'] = [image.get_attribute('src') for image in images]
        result['salePrice'] = soup.find('div',{'class':'itemBox priceInfo'}).find('span',{'class':'price'}).get_text()
        result['originalPrice'] = result['salePrice'] if soup.find('div',{'class':'itemBox priceInfo'}).find('span',{'class':'fixedPrice'}) is None else soup.find('div',{'class':'itemBox priceInfo'}).find('span',{'class':'fixedPrice'}).get_text()
        infoOptions = soup.find('div',{'class':'itemBox dtlInfo'}).find_all('dl')
        for option in infoOptions:
            if option.dt.get_text() == "용량":
                result['volume'] = option.dd.get_text()
                break
        
        #display(result)
        result_json.append(result)
#         else:
#             #컬러 있음
#             #Check # of Colors
#             colorList = driver.find_elements_by_xpath("//div[@class='bx-viewport']//li")
#             for idx, color in enumerate(colorList):
#                 color.click()
#                 result_dict = copy.deepcopy(result)
#                 images = driver.find_elements_by_xpath("//ul[@class='simg']//li//a//img")
#                 result_dict['image'] = [image.get_attribute('src') for image in images]
#                 result_dict['salePrice'] = soup.find('div',{'class':'itemBox priceInfo'}).find('span',{'class':'price'}).get_text()
#                 result_dict['originalPrice'] = result_dict['salePrice'] if soup.find('div',{'class':'itemBox priceInfo'}).find('span',{'class':'fixedPrice'}) is None else soup.find('div',{'class':'itemBox priceInfo'}).find('span',{'class':'fixedPrice'}).get_text()
#                 infoOptions = soup.find('div',{'class':'itemBox dtlInfo'}).find_all('dl')
#                 for option in infoOptions:
#                     if option.dt.get_text() == "용량":
#                         result_dict['volume'] = option.dd.get_text()
#                         break;
#                 result_dict['color'] = color.find_element_by_tag_name('a').get_attribute('data-option_goods_name')
#                 result_json.append(result_dict)
#                 display(result_dict)
        if idx % (len(urlList)//50) == 0:
            print("%3.1f 퍼센트 진행중" % round(idx / len(urlList) * 100))
    return result_json



for idx, category in enumerate(categorys):
    t = Thread(target = getItemDetailByUrl, args=(urlList,))
    t.start()
    t.join()
#result_json = getItemDetailByUrl(urlList)


# In[123]:


output = json.dumps(result_json,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'apieu.json')


# In[ ]:




