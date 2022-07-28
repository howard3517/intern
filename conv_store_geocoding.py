'''
這個程式會將由https://data.gcis.nat.gov.tw/od/detail?oid=0202BFA9-8116-4E63-A41A-58A5F4EAF7A2
此平台下載之五大超商csv檔做geocoding
'''

import requests
from pprint import pprint
import pandas as pd
import time
from math import radians, cos, sin, asin, sqrt
import csv


'''
變數設定在此
'''
api_key = [your_key_here] 
data_path = [your_data_path] # input 為 M_五大超商[年份]原始檔.csv的路徑
output_path = [your_output_data_path] # output 檔案想要放的位置

df = pd.read_csv(data_path)

place_list = []
for i in range(len(df)):
    address = df.loc[i, '分公司地址']
    payload = {
            'address': address,
            'key':api_key,
            }
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?',params=payload)
    api_response_dict = r.json()

    if api_response_dict['status'] == 'OK':
        google_lat = api_response_dict['results'][0]['geometry']['location']['lat']
        google_lng = api_response_dict['results'][0]['geometry']['location']['lng']

        df.loc[i, 'google_id'] = api_response_dict['results'][0]['place_id']
        df.loc[i, 'lat'] = google_lat
        df.loc[i, 'lng'] = google_lng
        print(google_lat, google_lng)
    else:
        df.loc[i, 'google_id'] = 'none'
        df.loc[i, 'lat'] = 'none'
        df.loc[i, 'lng'] = 'none'
        print('none')

df.to_csv(output_path)

