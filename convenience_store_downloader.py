import pandas as pd
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

#爬蟲機
def crawler(url):
    # 檢查Chrome版本和Chrome Driver版本是否相同
    ############################################################
    # Chrome.exe的位置
    # chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    # chrome_driver_path = r'..\CHROME_DRIVER'
    # ############################################################
    # DC = check_driver_version.DriverCheck(chrome_path,chrome_driver_path)
    # driver_path_to_use = DC.check_chromedriver_version()
    
    #webDriver基本設定
    options = webdriver.ChromeOptions()
    # options.add_argument("--disable-popup-blocking")
    out_path = os.getcwd()+r'\input'  # 設定瀏覽器檔案下載目的地路徑
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path} # 設定瀏覽器檔案下載目的地路徑
    options.add_experimental_option('prefs', prefs) # 設定瀏覽器檔案下載目的地路徑
    # driver = webdriver.Chrome(driver_path_to_use, chrome_options=options)
    driver = webdriver.Chrome(chrome_options=options)

    #拜訪網站
    driver.get(url)
    time.sleep(5)
    print('hello')
    r = driver.find_element(By.CSS_SELECTOR, "button.el-button.el-button--primary.el-button--mini.is-plain")
    r.click()
    time.sleep(5)  
    

#解壓縮機器
def unziper():
    status = True
    while status:
        for file in os.listdir(os.getcwd()+r'\input'):
            regex = re.compile(r'.+5大超商.+\.zip')
            match = regex.search(file)
            time.sleep(10)
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
                        os.remove('.\\input\\全國5大超商資料集.csv')

"""
def teldiff():
    #讀取最新下載的超商資料
    df_target = pd.read_csv('./input/全國5大超商資料集.csv', encoding='utf-8')
    #讀取前一期output資料
    df_ref = pd.read_csv('./前一期output資料/M_Convenience_Store_OLD.csv', encoding='utf-8')

    df = df_ref[['分公司地址','lat','lng']]
    #讀取歷史經緯度清單
    if os.path.exists('.\\地址經緯度對照表\\already_geocoding_addr_Conv.csv'):
        df_geolist = pd.read_csv('.\\地址經緯度對照表\\already_geocoding_addr_Conv.csv', encoding='utf-8')
        df = pd.concat([df, df_geolist], ignore_index=True)
        df= df.drop_duplicates(subset=['分公司地址']).reset_index(drop=True)
        df.to_csv('.\\地址經緯度對照表\\already_geocoding_addr_Conv.csv', encoding='utf-8-sig', index=False )
    else:
        df= df.drop_duplicates(subset=['分公司地址']).reset_index(drop=True)
        df.to_csv('.\\地址經緯度對照表\\already_geocoding_addr_Conv.csv', encoding='utf-8-sig', index=False )



    #最新資料 Left Join 地址經緯度對照表
    df_m = df_target.iloc[:,:10].merge(df, on='分公司地址', how='left')

    print('沒轉換資料地址數量:',df_m['lat'].isna().sum())

    mask = df_m['lat'].isna()
    df_m[mask]['分公司地址'].to_list()
    df_diff = df_m[mask]
    #存一份沒轉換過地址的csv
    df_diff.to_csv('.\\input\\None_geocoding_addr_Conv.csv', encoding='utf-8-sig', index=False )
    print('儲存尚未轉換過地址資料')
    df_same = df_m[~mask]
    #存一份轉換過地址的csv
    df_same.to_csv('.\\input\\geocoded_addr_Conv.csv', encoding='utf-8-sig', index=False )
    print('儲存轉換過地址資料')
"""

if __name__ == '__main__':
    
    print('Crawling 五大超商...')
    #刪除下載的壓縮檔
    
    for file in os.listdir(os.getcwd()+r'\input'):
        os.remove(f".\\input\\{file}")
    
#     #執行爬蟲
    print('下載HTML壓縮檔')
    crawler(url='https://data.gov.tw/dataset/32086') 

    #解壓縮下載完成檔案
    print('正在解壓縮...')
    unziper()

    """
    #複製一份 全國5大超商資料集.csv 到./input/前一期資料 中
    if os.path.exists('.\\前一期output資料\\M_Convenience_Store_OLD.csv'):
        os.remove('.\\前一期output資料\\M_Convenience_Store_OLD.csv')
        shutil.copy('.\\output\\M_Convenience_Storec.sv', '.\\前一期output資料\\M_Convenience_Store_OLD.csv')
    else:
        shutil.copy('.\\output\\M_Convenience_Store.csv', '.\\前一期output資料\\M_Convenience_Store_OLD.csv')
    """
    #teldiff()

    print('Done Crawling 五大便利超商！')
    print('='*85)