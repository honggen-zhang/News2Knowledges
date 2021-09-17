#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 13:35:50 2021

@author: user1
"""
import os
import pandas as pd
from urllib.request import urlopen
import re
from datetime import datetime
'''
url = 'https://blog.feedspot.com/celebrity_gossip_blogs/'
page = urlopen(url)


html_bytes = page.read()
html = html_bytes.decode("utf-8")

title_index = html.find("<title>")
#nn = re.findall("nofollow\">(...)<", html)
web_n = re.findall('(?:nofollow\"|ftp)>([^/\r\n]+)(<)?',html)
goosip = []
for coarse in web_n:
    website = coarse[0]
    if website[-4:] =='com<':
        goosip.append(website[:-5])

url_big = 'https://blog.feedspot.com/usa_news_websites/'
page = urlopen(url_big)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

title_index = html.find("<title>")
#nn = re.findall("nofollow\">(...)<", html)
web_n = re.findall('(?:nofollow\"|ftp)>([^/\r\n]+)(<)?',html)
big_news = []
for coarse in web_n:
    website = coarse[0]
    if website[-4:] =='com<':
        big_news.append(website[:-5])
'''        
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
def clean_spaces(s):
    s = s.replace('\r', '')
    s = s.replace('\t', ' ')
    s = s.replace('\n', ' ')
    return s

def remove_noisy(content):
    """Remove brackets"""
    p1 = re.compile(r'（[^）]*）')
    p2 = re.compile(r'\([^\)]*\)')
    return p2.sub('', p1.sub('', content))

def write_file(dir,data):
    file = open(dir, 'w')
    for d in data:
        file.write(d)
        file.write('\n')
    file.close()   

def read_url(str):
    df = pd.read_csv(str, usecols=['url','num'])    
    content_test = df.values.tolist()
    sample_url_list = []
   
    for url, num in content_test:
        sample_url_list.append(url)
    return sample_url_list
    

filelist = os.listdir(r'/home/user1/deskdata/IranPlane/Smollett/')
filelist.sort()
time = []
#newslist = ['bbc','nytimes','bloomberg','reuters','cbs','nbc','cnn','wsj','washingtonpost','economist','newyorker','foreignaffairs','theatlantic','politico']
#newslist = ['bbc','nytimes','bloomberg','reuters','cbs','nbc','cnn','wsj','washingtonpost']
newslist = read_url('/home/user1/deskdata/data generator/sample2.csv')
s=0
for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    print(tmpfn)
    tt=tmpfn[:-4].split('-')
    t = tt[0]+tt[1]+tt[2]
    
        
    #week = datetime.strptime(t,'%Y%m%d').weekday()
    #if week!=9 and week!=10:
    time.append(tmpfn[:-4])
    n=0
    data = []
    df = pd.read_csv('/home/user1/deskdata/IranPlane/Smollett/'+tmpfn, usecols=['url','text'])    
    content_test = df.values.tolist()
    
    for url, article in content_test:
        #print(article)

        #url_name = url.split('.')[1]
        news_url_list = url.split('/')
        try:
            url_name = news_url_list[2]
        except:
            try:
                url_name = news_url_list[1]
            except:
                url_name = news_url_list[0]
                
        if url_name in newslist:

            article = str(article)
            art = clean_spaces(article)
            art = remove_noisy(art)
            art = remove_emoji(art)
            art = art.replace(r"\n\n", r" ")
            data.append(art)

    if len(data)==0:
        article = content_test[0][1]
        article = str(article)
        art = clean_spaces(article)
        art = remove_noisy(art)
        art = remove_emoji(art)
        art = art.replace(r"\n\n", r" ")
        data.append(art)
    #write_file('/home/user1/deskdata/IranPlane/JS/Js_gossip_n/'+tmpfn[:-4]+'.txt', data)
    write_file('/home/user1/deskdata/JS/samples2TXT/file_'+str(j)+'.txt', data)
    
