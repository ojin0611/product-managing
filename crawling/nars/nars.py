#!/usr/bin/env python
# coding: utf-8

# In[124]:


from bs4 import BeautifulSoup as bs              # 데이터파싱 라이브러리
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import platform
import re
import time
import copy

from urllib.request import urlopen
import sys
sys.path.append('../../modules')
from crawling_module import *

driver = openChromedriver()
base_url = 'http://www.narscosmetics.co.kr/'



def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)



categorys = ["lips", "cheeks", "face", "eyes", "multi-use", "cult-classics", "narsskin", "makeup-removers", "brushes-tools", ]



def getUrlList():
    urlList = []
    for category in categorys:
        #카테고리별로 접속
        driver.get(base_url + category)
        last_height = driver.execute_script("return document.body.scrollHeight")
        #상품 긁기
        while True:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        html = driver.page_source
        soup = bs(html,'html.parser')
        products = driver.find_elements_by_xpath("//div[@class='product-image']//a[@class='thumb-link']")
        print(len(products))
        for product in products:
            urlList.append(product.get_attribute("href"))
    return urlList
        
        #다음 페이지가 있으면 다음 페이지로 이동



urlList = getUrlList()
urlList = list(set(urlList))
print(len(urlList))



def getItemDetailByUrl(urlList):
    
    result_json = []
    for idx, item in enumerate(urlList):
        driver.get(item)
        html = driver.page_source
        soup = bs(html,'html.parser')
        # dictionary 생성
        result = {'name':'', 'url':'', 'image':'', 'salePrice':'', 'originalPrice':'', 'color':'', 
                   'category':'', 'brand':'나스','volume':''}
        
        result['name'] = soup.find('h1',{'class':'product-name page-title'}).get_text()
        result['url'] = driver.current_url
        images = []
        
        #Color만큼 
        if soup.find('div',{'class':'selectricItems'}) is None:
            #단품
            if soup.find('div',{'id':'thumbnails'}) is None:
                images.append(soup.find('div',{'class':'product-primary-image'}).find('img')['src'])
                result['image'] = images
            else:
                images = driver.find_elements_by_xpath("//div[@id='thumbnails']//li//a")
                result['image'] = [image.get_attribute('href') for image in images]
            result['salePrice'] = soup.find('span',{'class':'price-sales'}).get_text()
            result['originalPrice'] = result['salePrice']
            result['volume'] = "#"
            result['color'] = "#"
            result_json.append(result)
        else:
            
            colors = driver.find_elements_by_xpath("//div[@class='selectricHideSelect']//option")
            htmlList = [color.get_attribute('data-href') for color in colors]
            totalColors = len(colors)
            for html in htmlList:
                driver.get(html)
                html = driver.page_source
                soup = bs(html,'html.parser')
                result['name'] = soup.find('h1',{'class':'product-name page-title'}).get_text()
                result['url'] = driver.current_url
                if soup.find('div',{'id':'thumbnails'}) is None:
                    images.append(soup.find('div',{'class':'product-primary-image'}).find('img')['src'])
                    result['image'] = images
                else:
                    images = driver.find_elements_by_xpath("//div[@id='thumbnails']//li//a")
                    result['image'] = [image.get_attribute('href') for image in images]
                result['salePrice'] = soup.find('span',{'class':'price-sales'}).get_text()
                result['originalPrice'] = result['salePrice']
                result['volume'] = "#"
                result['color'] = soup.find('span',{'class':'colorName'}).get_text()
                result_json.append(result)
        if idx % (len(urlList)//50) == 0:
            print("%3.1f 퍼센트 진행중" % round(idx / len(urlList) * 100))
#             for color in colors:
                
#                 color.click()
#                 time.sleep(2)
#                 html = driver.page_source
#                 soup = bs(html,'html.parser')
#                 result_dict = copy.deepcopy(result)
#                 result_dict['name'] = soup.find('h1',{'class':'product-name page-title'}).get_text()
#                 result_dict['url'] = driver.current_url
#                 result_dict['color'] = color.text
                
                
#                 if soup.find('div',{'id':'thumbnails'}) is None:
#                     images.append(soup.find('div',{'class':'product-primary-image'}).find('img')['src'])
#                     result_dict['image'] = images
#                 else:
#                     images = driver.find_elements_by_xpath("//div[@id='thumbnails']//li//a")
#                     result_dict['image'] = [image.get_attribute('href') for image in images]
#                 result_dict['salePrice'] = soup.find('div',{'id':'product-content'}).find('span',{'class':'price-sales'}).get_text()
#                 result_dict['salePrice'] = result_dict['originalPrice']
#                 result_dict['volume'] = "#"
                
#                 display(result_dict)
#                 result_json.append(result_dict)
        
    return result_json



result_json = getItemDetailByUrl(urlList)


output = json.dumps(result_json,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'nars.json')

