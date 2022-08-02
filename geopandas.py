from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split
import numpy as np
import geopandas as gpd
from shapely.geometry import MultiPolygon , Polygon
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import folium
from xgboost import Booster, XGBRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import ExtraTreesRegressor


#create geometry

polygons = []
for i in range(gdf.shape[0]):
    gdf['geometry'][i] = Polygon(([(float(gdf['LeftBottom_x'][i]),float(gdf['LeftBottom_y'][i])), (float(gdf['LeftBottom_x'][i]),float(gdf['RightTop_y'][i])),(float(gdf['RightTop_x'][i]),float(gdf['RightTop_y'][i])), (float(gdf['RightTop_x'][i]),float(gdf['LeftBottom_y'][i]))]))



gdf['geometry']

gdf

map = folium.Map(location = [25.1,121.55] , zoom_start = 11)
map


#白格黑線+重點格
ax = gdf.plot(color='white',edgecolor='black',figsize=(15,10))
xgcgdf.plot(ax=ax,column='change',color='r')
ax.set_title('xgboost',fontsize=25)


#兩張圖並排放
fig,(ax1,ax2) = plt.subplots(1,2,figsize=(25,20))
color = {'bed':'black','good':'red'}
ax11 = gdf.plot(ax=ax1,color='white',edgecolor='black',figsize=(15,10))
xgcgdf.plot(ax=ax11,column='future',cmap=colors.ListedColormap(list(color.values())))
ax1.set_title('xgboost',fontsize=25)

ax22 = gdf.plot(ax=ax2,color='white',edgecolor='black',figsize=(15,10))
catcgdf.plot(column='future',ax=ax22,cmap=colors.ListedColormap(list(color.values())))
ax2.set_title('catboost',fontsize=25)

#多層疊圖
map = folium.Map(location = [25.055,121.55] , zoom_start = 12)
c = {'bed':'black','good':'red'}
xgcgdf.explore(m=map,column='future',cmap=colors.ListedColormap(list(c.values())))
catcgdf.explore(m=map,column='future',cmap=colors.ListedColormap(list(c.values())))
excgdf.explore(m=map,column='future',cmap=colors.ListedColormap(list(c.values())))
folium.LayerControl().add_to(map)
map



#取交集
map = folium.Map(location = [25.06,121.55] , zoom_start = 11.5)
c = {'bed':'black','good':'red'}
over =xgcgdf.overlay(catcgdf, how="intersection")
over = over.overlay(excgdf, how='intersection')
print(over.shape[0])
over.explore(column='future',m=map,cmap=colors.ListedColormap(list(c.values())))

