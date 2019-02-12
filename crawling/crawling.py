import os, sys, re
import json
import platform
import time
import copy

from bs4 import BeautifulSoup as bs          
from selenium import webdriver
from urllib.request import urlopen

def getNumber(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))
    


def writeJSON(jsonString):
    brandname = os.getcwd().split('\\')[-1]
    output_path = '../../data/'+brandname

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
