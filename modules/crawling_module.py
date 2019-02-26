import os
from selenium import webdriver
from datetime import datetime

def openChromedriver():
    '''
    크롤링을 headless로 돌린다.
    window size를 고정시켜, 크기에 따라 항목위치가 바뀌는 반응형웹에서 생기는 오류를 방지한다.
    '''
    options = webdriver.chrome.options.Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    return driver

def writeJSON(jsonString):
    brandname = os.getcwd().split('\\')[-1]
    output_path = brandname+'.json'
    with open(output_path,'w',encoding='UTF-8') as file:
        file.write(jsonString)

    print('crawling complete :',datetime.now())
