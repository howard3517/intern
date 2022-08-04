import pandas as pd
import os 
from selenium import webdriver
from time import sleep
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import shutil
import xlrd #讀取xls檔

def crawler(url,out_path,file):
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values.automatic_downloads': 1, 'profile.default_content_settings.popups': 0, 'download.default_directory': out_path} # 設定瀏覽器檔案下載目的地路徑
    options.add_experimental_option('prefs', prefs) # 設定瀏覽器檔案下載目的地路徑
    driver = webdriver.Chrome(chrome_options=options)

    #拜訪網頁
    driver.get(url)
    sleep(2)

    #點擊Download
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/h1/div/div/button').click()
    sleep(2)
    
    print(f'Downloading {file} ... ')

    #選擇格式
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div/div[1]/h1/div/div/ul/li[1]/a/span"))).click()
    sleep(3)

    driver.close()

    #更改檔案名
    filename = max([out_path+'\\'+ f for f in os.listdir(out_path)], key = os.path.getctime)
    shutil.move(filename, os.path.join(out_path,file))

    print('Done')    

def converter(out_path,file):
    df = xlrd.open_workbook(f'{out_path}\{file}')
    data = pd.DataFrame()
    #存放統計時間與指數
    date = []
    number = []

    #第1個 sheet
    table = df.sheets()[0]
    for i in range(11,table.nrows): #前10筆非數據
        number.append(table.row_values(i)[1])
        #轉換時間 number -> day_str
        datenumber = table.row_values(i)[0]
        day =  xlrd.xldate_as_tuple(datenumber,df.datemode)
        day_str = f'{day[0]}/{day[1]}/{day[2]}' #Y/M/D
        date.append(day_str)
                
    data['統計時間'] = date
    data['DGS10'] = number
    return data



if __name__ == '__main__':

    out_path = os.getcwd()+r'\output'
    if not os.path.exists(out_path):
        os.mkdir(out_path)
        print(out_path)
    else:
        for file in os.listdir(out_path):
            os.remove(f'{out_path}\{file}')
        print(out_path)


    file = '美國10年期公債殖利率.xls'
    url = 'https://fred.stlouisfed.org/series/DGS10'

    crawler(url,out_path,file)
    df = converter(out_path,file)

    print(df.tail())
