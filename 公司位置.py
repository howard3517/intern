import pandas as pd
from time import sleep
import re
import sys
import time
import random
import os
import shutil
import requests
from bs4 import BeautifulSoup 
#import argparse
# import fake_useragent as fua
from selenium import webdriver
from selenium.webdriver.common.by import By
#sys.path.append(r'..')
# import check_driver_version
import string
import zipfile
from pathlib import Path
import zipfile



def crawler():
    options = webdriver.ChromeOptions()
    path = os.getcwd()+r'\input'
    prefs = {'profile.default_content_settings.popups': 0,'download.default_directory':path}
    options.add_experimental_option('prefs', prefs)
    print(' Crawling ... ')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://data.gov.tw/datasets/search?p=1&size=10&rft=%E5%8F%B0%E5%8C%97%E5%B8%82%E5%85%AC%E5%8F%B8%E7%99%BB%E8%A8%98%E8%B3%87%E6%96%99')
    sleep(3)
    print('Downloading ...')
    driver.find_element_by_xpath('//*[@id="app"]/main/div/div[2]/div[2]/div[2]/ul/li[1]/div[1]/div[1]/a').click()

    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.XPATH,'/html/body/div/div/div/main/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/button[1]').click()

    
    sleep(5)
def unziper():
    status = True
    while status:
        for file in os.listdir(os.getcwd()+r'\input'):
            regex = re.compile(r'.+公司.+\.zip')
            match = regex.search(file)
            
            if match:
                if not os.path.exists(os.getcwd()+f"\\input\\{file}"):
                    print("還未完成下載...")
                    continue
                else:
                    try:
                        print("正在解壓縮zip...",file)
                        path = os.getcwd()+r"\input"
                        print(os.getcwd()+f"\\input\\{file}")
                        #****解決壓縮檔內中文檔名編碼問題****
                        with zipfile.ZipFile(os.getcwd()+f"\\input\\{file}", 'r') as f:
                            for fn in f.namelist(): #以zipfile之namelist()獲取壓縮檔內的檔案名稱
                                extracted_path = Path(f.extract(fn,path)) #先解壓縮檔案, 再透過Pathlib獲取該檔案路徑
                                print(extracted_path)
                                extracted_path.rename('.\\input\\' + fn.encode('cp437').decode('cp950'))   #重新命名路徑成中文編碼檔案名稱(zip裡面是用cp437做編碼的，而windows系統繁體中文是cp950)
                                status = False
                    except:
                        os.remove('.\\input\\'+file)

    """filepath = os.getcwd()+r'\input'
    filename = max([filepath + '\\' + f for f in os.listdir(filepath)] , key=os.path.getctime)
    #shutil.move(filename,os.path.join(filepath,fname))
    with zipfile.ZipFile(filename,"r") as zip_ref:
        zip_ref.extractall(filepath)
    
    print('Done')
    print('-'*30)"""


    


    #//*[@id="app"]/main/div/div[2]/div[2]/div[2]/ul/li[1]/div[1]/div[1]/a
    #//*[@id="app"]/main/div/div[2]/div[2]/div[2]/ul/li[2]/div[1]/div[1]/a
    #//*[@id="app"]/main/div/div[2]/div[2]/div[2]/ul/li[10]/div[1]/div[1]/a




def crawler_all():
    options = webdriver.ChromeOptions()
    path = os.getcwd()+r'\input'
    prefs = {'profile.default_content_settings.popups': 0,'download.default_directory':path}
    options.add_experimental_option('prefs', prefs)
    print(' Crawling ... ')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://data.gov.tw/datasets/search?p=1&size=10&rft=%E5%8F%B0%E5%8C%97%E5%B8%82%E5%85%AC%E5%8F%B8%E7%99%BB%E8%A8%98%E8%B3%87%E6%96%99')
    sleep(3)
    print('Downloading ...')
    for i in range(1,11):
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element_by_xpath('//*[@id="app"]/main/div/div[2]/div[2]/div[2]/ul/li['+str(i)+']/div[1]/div[1]/a').click()

        
        driver.find_element(By.XPATH,'/html/body/div/div/div/main/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/button[1]').click()
                                        
        
        sleep(5)

        status = True
        while status:
            for file in os.listdir(os.getcwd()+r'\input'):
                regex = re.compile(r'.+公司.+\.zip')
                match = regex.search(file)
                
                if match:
                    if not os.path.exists(os.getcwd()+f"\\input\\{file}"):
                        print("還未完成下載...")
                        continue
                    else:
                        try:
                            print("正在解壓縮zip...",file)
                            path = os.getcwd()+r"\input"
                            print(os.getcwd()+f"\\input\\{file}")
                            #****解決壓縮檔內中文檔名編碼問題****
                            with zipfile.ZipFile(os.getcwd()+f"\\input\\{file}", 'r') as f:
                                for fn in f.namelist(): #以zipfile之namelist()獲取壓縮檔內的檔案名稱
                                    extracted_path = Path(f.extract(fn,path)) #先解壓縮檔案, 再透過Pathlib獲取該檔案路徑
                                    print(extracted_path)
                                    extracted_path.rename('.\\input\\' + fn.encode('cp437').decode('cp950'))   #重新命名路徑成中文編碼檔案名稱(zip裡面是用cp437做編碼的，而windows系統繁體中文是cp950)
                                    status = False
                        except:
                            os.remove('.\\input\\'+file)

if __name__ == '__main__':
    crawler_all()