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
stop_words.remove('s')
from nltk.stem.wordnet import WordNetLemmatizer


def write_file(str,all_triplets,all_sentences):
    all_tripels = []

    with open(str, 'w', newline='') as csvfile:
        fieldnames = ['head', 'relation','tail','sentence']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        for k in range(len(all_triplets)):
            node = all_triplets[k]
            if node not in all_tripels:
                all_tripels.append(node)
                a = node.split('@')
                #print(node)
                writer.writerow({'head': a[0], 'relation': a[1],'tail':a[2],'sentence':all_sentences[k]})

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

def clear_pronoun1(word):
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
def clear_pronoun(word):
    #v= ' '
    word_list = word.split()
    word_new = re.sub(r'  ','',word)
    try:
        if len(word_list) ==1 and word_list[0] in pronorn_list:
            #print(word_list)
            word_new = ''

    #word_new = re.sub(r'  ','',word_new)
    except:
        word_new = ''
    return word_new

def clear_nothing(word):
    head_list = word.split(' ')
    new_head_list = []
    for i in range(len(head_list)):
        #if head_list[i] = ''
        if len(head_list[i]) != 0 and head_list[i] not in stop_words:
            new_head_list.append(head_list[i])
            
    #print(new_head_list)
    v = ' '
    head = v.join(new_head_list)
    return head

def tense_relation(word):
    head_list = word.split(' ')
    new_head_list = []
    for i in range(len(head_list)):
        #if head_list[i] = ''
        try:
            w1 = WordNetLemmatizer().lemmatize(head_list[i],'v')
        #if len(head_list[i]) != 0 and head_list[i] not in stop_words:
        except:
            w1 = head_list[i]
        new_head_list.append(w1)
            
    #print(new_head_list)
    v = ' '
    head = v.join(new_head_list)
    return head
pronorn_list = ['us','him','it','this','he','they','his','us','her','she','their','we','my','its','himself','them','that','which','i','you','me','your','herself','themselves']        
filelist = os.listdir(r'/home/user1/deskdata/JS/bignews/coreference/')
filelist.sort()
input_filename = '/home/user1/deskdata/JS/bignews/coreference/'
output_filename = '/home/user1/deskdata/JS/bignews/coreference_clearnoise/'
time = []
node_list = []
edge_list = []
all_node = []
all_edge = []
ortinal_edge = []
ori_nodes = []
for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    tmpfn = 'file_'+str(j)+'.csv'
    ##print(tmpfn)
    time.append(tmpfn[:-4])
    triplet_set = []
    sentence_set = []
    

    content_test = open(input_filename+tmpfn, "r").readlines()
    for i in range(1,len(content_test)):
        lines = content_test[i]
        a=lines.split(',')
        ori_nodes.append(a[0])
        ori_nodes.append(a[2])
        #print(a[1])
        if a[0] == 'the us':
            a[0] = 'u.s.'
        head0 = re.sub(r'[^\w\s]',' ',a[0])# clear brackets
        
        #print('---:',head)
            
        head = re.sub(r'   ',' ',head0)
        head = re.sub(r'  ',' ',head)
        
        head_1 = clear_pronoun(head)
        head_ = clear_nothing(head_1)
        if head_ == 'us':
            print(a[0])
            #print('----:',head_1)
        #print('---:',head_)
        all_node.append(head_)
        if head_ not in node_list:
            if head_ != '' and head_ != ' ':
                node_list.append(head_)
        ortinal_edge.append(a[1])
        relation = re.sub(r'[^\w\s]',' ',a[1])
        relation = re.sub(r'  ','',relation)
        relation = tense_relation(relation)
        if relation not in edge_list:
            if relation != '' and relation !=' ':
                edge_list.append(relation)
        #tail_ = clear_pronoun(a[3])
        if ' n t ' in relation:
            relation = re.sub(r'n t','not',relation)
        all_edge.append(relation)
        if a[2] == 'the us':
            a[2] = 'u.s.'
        tail = re.sub(r'[^\w\s]',' ',a[2])
        
        tail_ = re.sub(r'   ',' ',tail)
        tail_ = re.sub(r'  ',' ',tail)
        
        tail_ = clear_pronoun(tail_)
        tail_ = clear_nothing(tail_)
        all_node.append(tail_)        
        if tail_ not in node_list:
            if tail_ !='' and tail_ !=' ':
                node_list.append(tail_)
        if head_ != tail_ and head_ !='' and tail_ !='' and head_ !=' ' and tail_ !=' ':
            if relation !='' and relation !=' ':
                triplet_set.append(head_+'@'+relation+'@'+tail_)
                sen = ','.join(a[4:])
                sentence_set.append(sen[:-1])
                
    write_file(output_filename+tmpfn,list(triplet_set),sentence_set)
node_list_dic = Counter(all_node).most_common()
node_list1 = []
for node in node_list_dic:
    if node[0] != '' and node[0] != ' ':
        node_list1.append(node[0])
edge_list_dic = Counter(all_edge).most_common()
edge_list1 = []
for edge in edge_list_dic:
    if edge[0] != '' and edge[0] != ' ':
        edge_list1.append(edge[0])
       
write_code('/home/user1/deskdata/JS/bignews/node_code_core_cle.csv',node_list1)        
write_code('/home/user1/deskdata/JS/bignews/edge_code_core_cle.csv',edge_list1)
#duplication_dic = IntersectionWord(node_list)
#word_all = word_sequences(node_list)
#dic_url = Counter(word_all).most_common(10)