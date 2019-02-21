#!/usr/bin/env python
# coding: utf-8

# In[88]:


from bs4 import BeautifulSoup as bs              # 데이터파싱 라이브러리
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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


def getUrlList(urlList):
    categoryList = driver.find_elements_by_xpath("//*[@class='tit-gnb ctgr1_pc']")
    categoryCount = len(categoryList)
    for i in range(categoryCount):
        #print(categoryList[i].text)
        categoryList[i].click()
        #카테고리 진입

        WebDriverWait(driver, 30
            ).until_not(EC.presence_of_element_located((By.XPATH, "//*[@id='loader']")))

        #Page 진입
        #다음 페이지로 이동
        nextPage = driver.find_element_by_xpath("//li[@class='paging_next']")
        checkTagName = nextPage.find_element_by_tag_name('a')
        while checkTagName is not None and checkTagName.get_attribute("href") != "javascript:;":
            #로드 완료 체크
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='paging_next']")))

            #상품 긁기
            products = driver.find_elements_by_xpath("//ul[@class='product-list']//div[@class='prod-box']//input[@name='i_sProductcd']")

            for product in products:
                urlList.append("http://tonystreet.com/shop/prod/shop_prod_product_view.do?i_sProductcd="+product.get_attribute("value")+"&i_sTypecd=0001")

            #다음 상품으로 건너가기
            nextPage.click()
            WebDriverWait(driver, 30).until_not(EC.presence_of_element_located((By.XPATH, "//*[@id='loader']")))
            nextPage = driver.find_element_by_xpath("//li[@class='paging_next']")
            checkTagName = nextPage.find_element_by_tag_name('a')
        #로드 완료 체크
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='paging_next']")))

        #상품 긁기
        products = driver.find_elements_by_xpath("//ul[@class='product-list']//div[@class='prod-box']//input[@name='i_sProductcd']")

        for product in products:
            urlList.append("http://tonystreet.com/shop/prod/shop_prod_product_view.do?i_sProductcd="+product.get_attribute("value")+"&i_sTypecd=0001")
        

        driver.find_element_by_class_name('btn-menu').click()
        categoryList = driver.find_elements_by_xpath("//*[@class='tit-gnb ctgr1_pc']")
    return urlList



def getItemDetailByUrl(urlList):
    result_json = []
    for idx, item in enumerate(urlList):
        driver.get(item)
        html = driver.page_source
        soup = bs(html,'html.parser')
        # dictionary 생성
        result = {'name':'', 'url':'', 'image':'', 'salePrice':'', 'originalPrice':'', 'color':'', 
                   'category':'', 'brand':'토니모리','volume':''}
        result['name'] = soup.find('section',{'class':'prd-info-wrap dtl_prd_info_wrap'}).find('h3',{'class':'prod-name'}).get_text()
        result['url'] = driver.current_url
        images = soup.find('div',{'class':'slick-slide slick-current slick-active'}).find_all('img')
        result['image'] = [image['src'] for image in images]
        result['salePrice'] = soup.find('section',{'class':'prd-info-wrap dtl_prd_info_wrap'}).find('em',{'class':'price-after'}).get_text().strip()
        result['originalPrice'] = soup.find('section',{'class':'prd-info-wrap dtl_prd_info_wrap'}).find('span',{'class':'price-before'}).get_text().strip() if soup.find('section',{'class':'prd-info-wrap dtl_prd_info_wrap'}).find('span',{'class':'price-before'}) is not None else result['salePrice']
        result['volume'] = "#"
        infoOptions = soup.find_all('dl',{'class':'dl-list'})
        for option in infoOptions:
            if option.dt.get_text() == "용량 또는 중량":
                result['volume'] = option.dd.get_text()
                break
        categorys = []
        findCategory = soup.find('div',{'class':'snb-group'}).find_all('span',{'class':'ui-selectmenu-text'})
        for category in findCategory:
            categorys.append(category.get_text())
        result['category'] = '>'.join(categorys)
        
        colors = soup.find('select',{'id':'ui-id-5'}).find_all('option')
        
        if soup.find('div',{'id':'dtl_selectOpt_top'}).has_attr('style') == True  or len(colors) == 1:
            result['color'] = "#"
            result_json.append(result)
            #display(result)
        else:
            for i in range(1,len(colors)):
                result_dict = copy.deepcopy(result)
                result_dict['color']= colors[i].get_text().strip()
                result_json.append(result_dict)
                #display(result_dict)
        if idx % (len(urlList)//50) == 0:
            print("%3.1f 퍼센트 진행중" % round(idx / len(urlList) * 100))
        

    return result_json


if (platform.system() == 'Linux'):
    print('system : Linux')
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
else:
    driver = openChromedriver()
url_home = 'http://tonystreet.com/'
driver.get(url_home)


html = driver.page_source
soup = bs(html,'html.parser')

if soup.find('a',{'class':'btn_popup_close'}) is not None:
    driver.find_element_by_class_name('btn_popup_close').click()



driver.find_element_by_xpath("//div[@class='gnb group']//a[@class='btn-menu']").click()



urlList=[]
print('check 95')
getUrlList(urlList)
print('urlList :', urlList)
urlList = list(set(urlList))
print(len(urlList))



result_json = getItemDetailByUrl(urlList)


driver.close()

output = json.dumps(result_json,ensure_ascii=False, indent='\t')

writeJSON(output, output_name = 'tonymoly.json')


# In[ ]:




