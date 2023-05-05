#!/usr/bin/env python
# coding: utf-8

# In[5]:


import argparse
import json
import pandas as pd
import numpy as np
from pathlib import Path
import requests
import datetime
import time

parser = argparse.ArgumentParser()
#adding --path as positional argument (u need to write --path then the path for the jason file)
parser.add_argument('path',help="u need to write a valid path for the jason file")

#adding -u as an optional arqument
parser.add_argument("-u","--unix", action="store_true")

args = parser.parse_args()  

if args.unix:
    u=True
else: 
    u=False

#converting the file passed from the --path argumnet to dataframe
df = pd.read_json(args.path, lines=True)

#intialization df_2 with cols (the target dataframe)
df_2 = pd.DataFrame(columns = ['web_browser', 'operating_sys'])

# creating the web_browser col by using split to col "a" in df
df_2["web_browser"]= df.a.str.split("/").str.get(0)

# creating the web_browser col by using split to col "a" in df
df_2["operating_sys"]= df.a.str.split(" ").str.get(1).str[1:]

#converting "r" and "u" to "from_url" and "to_url" cols and using findall which search for url
df_2["from_url"]=df["r"].str.findall('://([\w\-\.]+)',flags=0).str.get(0)
df_2["to_url"]=df["u"].str.findall('://([\w\-\.]+)',flags=0).str.get(0)

#the city col will be the same as in the jason
df_2["city"]=df["cy"]

# converting "ll" in source into two cols "lang" and "lat"
df_2["langitude"]= df.ll.apply(str).str.split(",").str.get(0)
df_2["langitude"]=df_2["langitude"].str.split("[").str.get(-1)
df_2["latitude"]= df.ll.apply(str).str.split(",").str.get(1)
df_2["latitude"]= df_2["latitude"].str.split("]").str.get(0)

#creating "time_zone" col
df_2["time_zone"]= df["tz"]

#creating "time_in" and "time_out" cols using lambda 
#importing requests, datetime to display time in details(from year to seconds)

#if u write -u the time will be in timestamp
if (u==False ):
    df_2['time_in'] = df['t'].apply(lambda x: datetime.datetime.fromtimestamp(x).ctime())
    df_2['time_out'] = df['hc'].apply(lambda x: datetime.datetime.fromtimestamp(x).ctime())
else:
#if u don't write -u time will be converted to a readable time    
    df_2['time_in'] = df['t']
    df_2['time_out'] = df['hc']



#replacing null values as required
df_2 = df_2.replace(['nan'], '  ')
df_2 = df_2.replace([np.NaN], '  ')

#printing required exexecution  Time for the opertions of this task
startTime = time.time()
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

#printing the number of rows transformed
print("number of rows transformed ",len(df_2))

#converting the dataframe into csv on the same path
df_2.to_csv(r'gov_click_data2.csv')

import os
print(str(os.path.abspath("gov_click_data2.csv")))


# In[ ]:




