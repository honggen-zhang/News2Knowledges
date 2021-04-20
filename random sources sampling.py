#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 21:23:39 2021

@author: user1
"""


import os
import re
from collections import Counter
import spacy
from wordcloud import WordCloud
import csv
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from fuzzywuzzy import fuzz
import statistics 
import math
import numpy as np
import scipy
import pandas as pd

import random


def write_file(str,main_url):
    with open(str, 'w', newline='') as csvfile:
        fieldnames = ['url', 'num']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        for u in main_url:
            #print(node)
            
            writer.writerow({'url':u[0], 'num':u[1]})


filelist = os.listdir(r'/home/user1/deskdata/IranPlane/Smollett/')
filelist.sort()

url_set = []

for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    #time.append(tmpfn[:-4])
    #print(tmpfn)

    #triplets_objective, nodes_obj = read_file('/home/user1/Desktop/IE_js/sim/sub_space/object_graph/'+tmpfn)
    df = pd.read_csv('/home/user1/deskdata/IranPlane/Smollett/'+tmpfn, usecols=['url','text'])    
    content_test = df.values.tolist()
    for news in content_test:
        news_url = news[0]           
        news_url_list = news_url.split('/')

        try:
            url_set.append(news_url_list[2])
        except:
            try:
                url_set.append(news_url_list[1])
            except:
                url_set.append(news_url_list[0])
dic_url = Counter(url_set).most_common()
main_num = 0
all_num = 0
url_main = []
while main_num<2000:
    random.shuffle(dic_url)
    if int(dic_url[0][1])>10:
        main_num = main_num + int(dic_url[0][1])
        url_main.append(dic_url[0])
        dic_url.pop(0)
    
write_file('/home/user1/deskdata/data generator/sample1.csv',url_main)
main_num2 = 0        
url_main2 = []
while main_num2<2000:
    random.shuffle(dic_url)
    if int(dic_url[0][1])>10:
        main_num2 = main_num2 + int(dic_url[0][1])
        url_main2.append(dic_url[0])
        dic_url.pop(0)    
write_file('/home/user1/deskdata/data generator/sample2.csv',url_main2)