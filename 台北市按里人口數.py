
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    path = os.getcwd()+r'\input'
    prefs = {'profile.default_content_settings.popups': 0,'download.default_directory':path}
    options.add_experimental_option('prefs', prefs)
    print(' Crawling 人口數 ...')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://data.gov.tw/dataset/136896')



    #element (s)
    print('Downloading ...')
    num = driver.find_elements_by_class_name("el-button.el-button--primary.el-button--mini.is-plain")
    for i in range(len(num)):
        driver.find_elements_by_class_name('el-button.el-button--primary.el-button--mini.is-plain')[i].click()

    sleep(3)

    driver.close()
    
    print('Done')
    print('='*85)