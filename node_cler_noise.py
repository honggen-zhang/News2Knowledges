#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:49:55 2021

@author: user1

This scripe is tring to clear some noise symbols and pronorn words because we cannot clear all pronorn from the coreference operation.
Note that there are some empity string such as '',' ' after clearing the noise. In the final writing part, we filter the empity string.
"""


import gensim 
from gensim.models import Word2Vec 
import os
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import re
from nltk.corpus import stopwords
stop_words = list(stopwords.words('english'))



def write_file(str,all_triplets):

    with open(str, 'w', newline='') as csvfile:
        fieldnames = ['head', 'relation','tail']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        for node in all_triplets:
            a = node.split('@')
            #print(node)
            writer.writerow({'head': a[0], 'relation': a[1],'tail':a[2]})

def write_code(str,all_nodes):

    with open(str, 'w', newline='') as csvfile:
        fieldnames = ['idx', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        i = 1
        for node in all_nodes:
            writer.writerow({'idx': '{0:05}'.format(i), 'label': node})
            i = i+1            

def word_sequences(node_list):
    node_fre = []
    for node in node_list:
        a = node.split()
        for word in a:
            if word not in stop_words:
                node_fre.append(word)
    return node_fre

def clear_pronoun(word):
    v= ' '
    word_list = word.split()
    try:
        for i in range(len(word_list)):
            w  = word_list[i]
            if w in pronorn_list:
                #print(word_list)
                word_list.pop(i)
        #print(word_list)
        word_new = v.join(word_list)
        word_new = re.sub(r'  ','',word_new)
    except:
        word_new = 'null'
    return word_new


pronorn_list = ['him','it','this','he','they','his','us','her','she','their','we','my','its','himself','them','that','which','i','you','me','your','herself','themselves']        
filelist = os.listdir(r'/home/user1/deskdata/JS/data1/coreference1/')
filelist.sort()

time = []
node_list = []
edge_list = []
all_node = []
for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    ##print(tmpfn)
    time.append(tmpfn[:-4])
    triplet_set = []
    

    content_test = open('/home/user1/deskdata/JS/data1/coreference1/'+tmpfn, "r").readlines()
    for i in range(1,len(content_test)):
        lines = content_test[i]
        a=lines.split(',')
        head = re.sub(r'[^\w\s]','',a[1])# clear brackets
        head = re.sub(r'  ','',head)
        head_ = clear_pronoun(head)
        all_node.append(head_)
        if head_ not in node_list:
            if head_ != '' and head_ != ' ':
                node_list.append(head_)
        relation = re.sub(r'[^\w\s]','',a[2])
        relation = re.sub(r'  ','',relation)
        if relation not in edge_list:
            if relation != '' and relation !=' ':
                edge_list.append(relation)
        #tail_ = clear_pronoun(a[3])
        tail = re.sub(r'[^\w\s]','',a[3])
        tail_ = re.sub(r'  ','',tail)
        tail_ = clear_pronoun(tail_)
        all_node.append(tail_)        
        if tail_ not in node_list:
            if tail_ !='' and tail_ !=' ':
                node_list.append(tail_)
        if head_ != tail_ and head_ !='' and tail_ !='' and head_ !=' ' and tail_ !=' ':
            if relation !='' and relation !=' ':
                triplet_set.append(head_+'@'+relation+'@'+tail_)
    write_file('/home/user1/deskdata/JS/data1/coreference_clearnoise/'+tmpfn,list(set(triplet_set)))
        
write_code('/home/user1/deskdata/JS/data1/node_code_core_cle.csv',node_list)        
write_code('/home/user1/deskdata/JS/data1/edge_code_core_cle.csv',edge_list)
#duplication_dic = IntersectionWord(node_list)
#word_all = word_sequences(node_list)
#dic_url = Counter(word_all).most_common(10)