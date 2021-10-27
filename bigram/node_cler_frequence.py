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

def write_file(str,all_triplets,sentences):
    triples_all = []

    with open(str, 'w', newline='') as csvfile:
        fieldnames = ['head', 'relation','tail','sentence']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        for k in range(len(all_triplets)):
            node = all_triplets[k]
            if node not in triples_all:
                triples_all.append(node)
                a = node.split('@')
                #print(node)
                #if a[0] in node_most_common_500 and a[2] in node_most_common_500 and a[1] in edge_most_common_500:
                writer.writerow({'head': a[0], 'relation': a[1],'tail':a[2],'sentence':sentences[k][3:-3]})

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
        #if label == 'jussie' or label ==
        nodes.append(label)
    print('read done')
    return nodes,id2node,node2id         

def IntersectionWord(node_list):
    dup_dic = {}
    print('begainning diction...')
    #node_list2 = node_list
    print(len(node_list))
    while len(node_list)>=2:
        #print(node_list)
        node1  = node_list[0]
        node1_dup = []
        node_list.remove(node1)
        #print(node1)
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
                if ratio>0.5:
                    node1_dup.append(node2)
                    node_list.remove(node2)
        dup_dic[node1] = node1_dup
    print('diction done')
    return dup_dic

def IntersectionWord2(node_list):
    dup_dic = {}
    print('begainning diction...')
    #node_list2 = node_list
    print(len(node_list))
    while len(node_list)>=2:
        node1  = node_list[0]
        node1_dup = []
        node_list.remove(node1)
        print(node1)
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
                if ratio>0.5:
                    node1_dup.append(node2)
                    node_list.remove(node2)
        dup_dic[node1] = node1_dup
    print('diction done')
    return dup_dic

def IntersectionEdge(node_list):
    dup_dic = {}
    
    #node_list2 = node_list
    no_list = ["not","nt","dont"]
    while len(node_list)>=1:
        node1  = node_list[0]
        node1_dup = []
        node_list.remove(node1)
        node_list2 = node_list.copy()        
        for node2 in node_list2:
            a = node1.split()
            b = node2.split()
            inter = list(set(a).intersection(set(b)))

            if set(inter).issubset(set(stop_words)) or 'not' in a:
                pass
            else:
                ratio1 = len(inter)/len(a)
                ratio2 = len(inter)/len(b)
                ratio  = min(ratio1,ratio2)#for edge
                if ratio>0.5:
                    #print(node1,node2)
                    node1_dup.append(node2)
                    node_list.remove(node2)
        dup_dic[node1] = node1_dup
    return dup_dic

#The section of cluster similarity words together based on word itself

node_list,id2node_dic,node2id_dic = read_file('/home/user1/deskdata/JS/bignews/node_code_core_cle.csv') # the all nodes load from coreference node code
duplication_dic = IntersectionWord(node_list) # cluster node
new_id2node = id2node_dic.copy()
for ker, value in duplication_dic.items():# build new diction to storage id and label
    #ker_id = node2id_dic[ker]
    for node in value:
        idx = node2id_dic [node] 
        new_id2node[idx] = ker
        

#-------------------------------------------------------------------------------
edge_list,id2edge_dic,edge2id_dic = read_file('/home/user1/deskdata/JS/bignews/edge_code_core_cle.csv')     
duplication_dic_edge = IntersectionEdge(edge_list) #cluster edge
new_id2edge = id2edge_dic.copy()
for ker, value in duplication_dic_edge.items():
    #ker_id = node2id_dic[ker]
    for node in value:
        idx = edge2id_dic [node] 
        new_id2edge[idx] = ker
#-----------------------------------------------------------------------------------------
#The part trys to rewrite the triples based on above node and edge cluster
filelist = os.listdir(r'/home/user1/deskdata/JS/gossip/coreference_clearnoise/')
filelist.sort()

time = []
node_list = []
edge_list = []
#all_node = []
daily_triples_set = []
for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    tmpfn = 'file_'+str(j)+'.csv'
    print(tmpfn)
    time.append(tmpfn[:-4])
    triplet_set = []
    sentences = []

    content_test = open('/home/user1/deskdata/JS/bignews/coreference_clearnoise/'+tmpfn, "r").readlines()
    for i in range(1,len(content_test)):
        lines = content_test[i]
        a=lines.split(',')
        head = a[0]
        relation = a[1]                 
        tail = a[2]
        idx_head = node2id_dic[head]
        idx_tail = node2id_dic[tail]
        idx_relation = edge2id_dic[relation]
        
        new_head = new_id2node[idx_head]
        if new_head == 'smollett' or new_head =='jussie':
            new_head = 'jussie smollett'
        
        if new_head == 'plane' or new_head =='ukrainian plane':
            new_head = 'plane'
        if new_head == 'trump' or new_head =='president donald trump':
            new_head = 'donald trump' 
        if new_head == 'u s' or new_head =='united states':
            new_head = 'united states'
        node_list.append(new_head)
        
        new_tail = new_id2node[idx_tail]
        if new_tail == 'smollett' or new_tail =='jussie':
            new_tail = 'jussie smollett'
        if new_tail == 'plane' or new_tail =='ukrainian plane':
            new_tail = 'plane'   
        if new_tail == 'trump' or new_tail =='president donald trump':
            new_tail = 'donald trump'  
        if new_tail == 'u s' or new_tail =='united states':
            new_tail = 'united states'
        node_list.append(new_head)
        node_list.append(new_tail)
      
        new_relation = new_id2edge[idx_relation]
        edge_list.append(new_relation)
        
        if new_head != new_tail:
            triple = new_head+'@'+new_relation+'@'+new_tail
            triplet_set.append(triple)
            sen = ','.join(a[3:])
            sentences.append(sen[:-1])
        
    write_file('/home/user1/deskdata/JS/bignews/edge_fre_clear/'+tmpfn,list(triplet_set),sentences)
    daily_triples_set.append(triplet_set)
# =============================================================================
# node_most_common_500_dic = Counter(node_list).most_common(6000)
# edge_most_common_500_dic = Counter(edge_list).most_common()
# 
# node_most_common_500 = []
# edge_most_common_500 = []
# for node in node_most_common_500_dic:
#     node_most_common_500.append(node[0])
# for edge in edge_most_common_500_dic:
#     edge_most_common_500.append(edge[0])
# for k in range(len(filelist)):
#     triplet_set = daily_triples_set[k]
#     tmpfn = 'file_'+str(k)+'.csv'
#     write_file('/home/user1/deskdata/JS/gossip/edge_fre_clear/'+tmpfn,list(set(triplet_set)))
# 
# =============================================================================

