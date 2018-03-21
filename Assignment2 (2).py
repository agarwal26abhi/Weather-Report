
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[2]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[4]:

import numpy as np
df=pd.read_csv("data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv")
df.sort_values(["ID","Date"],inplace=True)
ld=list(df[df["Date"]=="2008-02-29"].index)
df.drop(ld,inplace=True)
ld=list(df[df["Date"]=="2012-02-29"].index)
df.drop(ld,inplace=True)
df1=df[df["Date"]<"2015-01-01"]
df2=df[df["Date"]>="2015-01-01"]
gp=df1.groupby("Date")
min_temp=gp.Data_Value.min()
max_temp=gp.Data_Value.max()
min_temp=min_temp.reset_index()
lt=[]
for i in range(0,len(min_temp)):
    lt.append(min_temp["Date"].loc[i][5:])
min_temp.drop("Date",axis=1,inplace=True)
min_temp["Date"]=lt
max_temp=max_temp.reset_index()
max_temp.drop("Date",axis=1,inplace=True)
max_temp["Date"]=lt
gp=min_temp.groupby("Date")
min_temp=gp.Data_Value.min()
gp=max_temp.groupby("Date")
max_temp=gp.Data_Value.max()
plt.figure()
plt.plot(min_temp.values,"b",label="record low",alpha=.7)
plt.plot(max_temp.values,"r",label="record high",alpha=.7)
plt.ylim(-700,500)
plt.fill_between(range(0,365),min_temp,max_temp,facecolor='yellow',alpha=.7)
plt.xlabel("Number of Days")
plt.ylabel("Temperature(tenths of degrees C)")
plt.title("Temperature Summary plot near Ann Arbor, Michigan")
min_2015=df2.groupby("Date").Data_Value.min().reset_index()
max_2015=df2.groupby('Date').Data_Value.max().reset_index()
min_2015.drop("Date",axis=1,inplace=True)
min_2015['Date']=min_temp.index
min_2015.set_index("Date",inplace=True)
max_2015.drop("Date",axis=1,inplace=True)
max_2015['Date']=max_temp.index
max_2015.set_index("Date",inplace=True)
min_2015=min_2015.where(min_temp>min_2015["Data_Value"])
max_2015=max_2015.where(max_temp<max_2015["Data_Value"])
min_2015.reset_index(drop=True,inplace=True)
min_2015.dropna(inplace=True)
max_2015.reset_index(drop=True,inplace=True)
max_2015.dropna(inplace=True)
plt.scatter(max_2015.index,max_2015["Data_Value"].values,color='g',s=5,label="broken high")
plt.scatter(min_2015.index,min_2015["Data_Value"].values,color='orange',s=5,label="broken low")
ob=plt.gca()
ob.legend(loc=4,frameon=False)
plt.show()
plt.savefig("graph1.png")


# In[ ]:



