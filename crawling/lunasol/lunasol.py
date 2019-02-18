#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
import platform, sys, re
import copy

from urllib.request import urlopen
sys.path.append('../../modules')
from crawling_module import *


def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)

def getItemList(categoryURL):
    fp = urlopen(categoryURL)
    html = fp.read().decode("utf8")
    fp.close()
    soup = bs(html,'html.parser')

    items = soup.find('div',{'class':'product_cat product_cat_first'})
    items = items.find_all('a')
    items = list(set(items))
    return items


def getItem(itemURL): 
    fp = urlopen(itemURL)
    html = fp.read().decode("utf8")
    fp.close()

    soup = bs(html,'html.parser')
    
    name = soup.find('div',{'class':'product_summary'}).h1.get_text()    
    url = itemURL
    category = soup.find('div',{'id':'directory_link'}).get_text().replace(' > '+name,"")
    imageList = []
    image_main = url_home + soup.find('div',{'class':'product_photo'}).img['src']
    imageList.append(image_main)
    
    
    # item 설정
    item = {'name':'#', 'url':'#', 'image':'#', 'color':'#', 'category':'#', 
                   'salePrice':'#', 'originalPrice':'#', 'brand':'lunasol','volume':'#'}
    
    item['name']=name
    item['url'] = url
    item['category']=category.strip()
    item['image'] = imageList
    
    # return 할 json 설정
    item_json = []
    
    # color로 상품 구분
    colors= soup.find('div',{'class':'product_color'})
    
    if colors: # 색상이 있는 경우
        colors = colors.find_all('img')
        for color in colors:
            image_color = url_home + color['src']
            name_color = color['alt']

            item_dict = copy.deepcopy(item)
            item_dict['image'].append(image_color)
            item_dict['color'] = name_color
            item_json.append(item_dict)
            
    else:
        colors='#'
        item_dict = copy.deepcopy(item)
        item_dict['color'] = colors
        item_json.append(item_dict)
        
    return item_json

'''
path = 'chromedriver.exe' if (platform.system() == 'Windows') else '/Users/jg/Desktop/develop/DataTeam/DataProcessing/product/crawling/chromedriver'
driver = webdriver.Chrome(path)
'''
driver = openChromedriver()


url_home = 'https://www.lunasol-net.com'
url_product = 'https://www.lunasol-net.com/kr/product/index.html'
driver.get(url_product)


html = driver.page_source
soup = bs(html,'html.parser')
category_total = soup.find('div',{'class':'product_mn_list png_fix'})
category_big = category_total.find_all('div')



# open category, item
result = []
for categories in category_big:
    list_category = categories.find_all('li')
    for category in list_category:
        categoryURL = category.a['href'] # get url of category
        items = getItemList(categoryURL)
        print('item 개수 :', len(items))
        for i, item in enumerate(items):
            print(i+1)
            itemURL = url_home + item['href']
            result += getItem(itemURL)


        
            
        driver.get(url_product)


output = json.dumps(result,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'lunasol.json')




