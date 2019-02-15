import os
from selenium import webdriver
from datetime import datetime

def openChromedriver():
    '''
    options = webdriver.chrome.options.Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    '''

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    return driver

def writeJSON(jsonString):
    brandname = os.getcwd().split('\\')[-1]
    output_path = './'+brandname+'.json'
    with open(output_path,'w',encoding='UTF-8') as file:
        file.write(jsonString)

    print('crawling complete :',datetime.now())
