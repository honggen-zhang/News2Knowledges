#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 22:37:11 2021

@author: user1
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

def read_file(str):
    nodes = []
    id2node = {}
    node2id = {}
    content_test = open(str, "r").readlines()
    for i in range(1,len(content_test)):
        lines = content_test[i]
        a=lines.split(',')
        #subj_id = a[0]
        label = a[1][:-1]
        #a = label.split()
        #if len(a)>0:
        id2node[a[0]] = label
        node2id[label] = a[0]
        nodes.append(label)
    return nodes,id2node,node2id         

def IntersectionWord(node_list):
    dup_dic = {}
    
    #node_list2 = node_list
    while len(node_list)>=1:
        node1  = node_list[0]
        node1_dup = []
        node_list.remove(node1)
        node_list2 = node_list.copy()        
        for node2 in node_list2:
            a = node1.split()
            b = node2.split()
            inter = list(set(a).intersection(set(b)))

            if set(inter).issubset(set(stop_words)):
                pass
            else:
                ratio1 = len(inter)/len(a)
                ratio2 = len(inter)/len(b)
                ratio  = min(ratio1,ratio2)
                if ratio>=0.5:
                    node1_dup.append(node2)
                    node_list.remove(node2)
        dup_dic[node1] = node1_dup
    return dup_dic

def IntersectionEdge(node_list):
    dup_dic = {}
    
    #node_list2 = node_list
    no_list = ["not","nt","don't"]
    while len(node_list)>=1:
        node1  = node_list[0]
        node1_dup = []
        node_list.remove(node1)
        node_list2 = node_list.copy()        
        for node2 in node_list2:
            a = node1.split()
            b = node2.split()
            inter = list(set(a).intersection(set(b)))

            if set(inter).issubset(set(stop_words)) or len(set(no_list).intersection(set(a))) != 0:
                pass
            else:
                ratio1 = len(inter)/len(a)
                ratio2 = len(inter)/len(b)
                ratio  = min(ratio1,ratio2)#for edge
                if ratio>=0.5:
                    node1_dup.append(node2)
                    node_list.remove(node2)
        dup_dic[node1] = node1_dup
    return dup_dic

#The section of cluster similarity words together based on word itself

node_list,id2node_dic,node2id_dic = read_file('/home/user1/deskdata/JS/data2/node_code_core_cle.csv') # the all nodes load from coreference node code
duplication_dic = IntersectionWord(node_list) # cluster node
new_id2node = id2node_dic.copy()
for ker, value in duplication_dic.items():# build new diction to storage id and label
    #ker_id = node2id_dic[ker]
    for node in value:
        idx = node2id_dic [node] 
        new_id2node[idx] = ker
#-------------------------------------------------------------------------------
edge_list,id2edge_dic,edge2id_dic = read_file('/home/user1/deskdata/JS/data2/edge_code_core_cle.csv')     
duplication_dic_edge = IntersectionEdge(edge_list) #cluster edge
new_id2edge = id2edge_dic.copy()
for ker, value in duplication_dic_edge.items():
    #ker_id = node2id_dic[ker]
    for node in value:
        idx = edge2id_dic [node] 
        new_id2edge[idx] = ker
#-----------------------------------------------------------------------------------------
#The part trys to rewrite the triples based on above node and edge cluster
filelist = os.listdir(r'/home/user1/deskdata/JS/data2/coreference_clearnoise/')
filelist.sort()

time = []
#node_list = []
#edge_list = []
#all_node = []
for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    ##print(tmpfn)
    time.append(tmpfn[:-4])
    triplet_set = []
    

    content_test = open('/home/user1/deskdata/JS/data2/coreference_clearnoise/'+tmpfn, "r").readlines()
    for i in range(1,len(content_test)):
        lines = content_test[i]
        a=lines.split(',')
        head = a[0]
        relation = a[1]                 
        tail = a[2][:-1]
        idx_head = node2id_dic[head]
        idx_tail = node2id_dic[tail]
        idx_relation = edge2id_dic[relation]
        new_head = new_id2node[idx_head]
        new_tail = new_id2node[idx_tail]
        new_relation = new_id2edge[idx_relation]
        if new_head != new_tail:
            triple = new_head+'@'+new_relation+'@'+new_tail
        triplet_set.append(triple)
    write_file('/home/user1/deskdata/JS/data2/edge_fre_clear/'+tmpfn,list(set(triplet_set)))


