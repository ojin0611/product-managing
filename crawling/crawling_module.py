import os, sys
import platform
from selenium import webdriver
from datetime import datetime

def openChromedriver():
    '''
    if platform.system() == 'Windows':
        path = 'chromedriver.exe'  
    elif platform.system() == 'Linux':
        path = '/home/ec2-user/chromedriver'
    else:
        path = '/Users/jg/Desktop/develop/DataTeam/DataProcessing/product/crawling/chromedriver'
    driver = webdriver.Chrome(path)
    '''
    # another way
    options = webdriver.chrome.options.Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)


    return driver

def writeJSON(jsonString):
    brandname = os.getcwd().split('\\')[-1]
    output_path = '../../data/'+brandname+'/crawling'

    # 첫 크롤링이면 디렉토리 생성
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    new_file = output_path + '/new.json'
    old_file = output_path + '/old.json'

    # 기존 new file 덮어쓰기
    if os.path.isfile(new_file):
        # old file 존재 시 삭제 후 덮어쓰기
        if os.path.isfile(old_file):
            os.remove(old_file)
        os.rename(new_file, old_file)

    with open(new_file,'w',encoding='UTF-8') as file:
        file.write(jsonString)

    print(datetime.now())
