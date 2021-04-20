#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 23:20:22 2021

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
import gensim 
from gensim.models import Word2Vec 

def write_KG(str,all_triplets):
    with open(str, 'w', newline='') as csvfile:
        fieldnames = ['Source', 'Target','Label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        for node in all_triplets:
            a = node.split('@')
            #print(node)
            if a[0] != 'null' and a[1] != 'null':
                writer.writerow({'Source': a[0], 'Target': a[2],'Label':a[1]})
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
        id2node[a[0]] = label
        node2id[label] = a[0]
        nodes.append(label)
    return nodes,id2node,node2id    

def write_code(str,all_nodes):

    with open(str, 'w', newline='') as csvfile:
        fieldnames = ['idx', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        i = 1
        for node in all_nodes:
            writer.writerow({'idx': '{0:05}'.format(i), 'label': node})
            i = i+1   

def encode_node(str):
    
    filelist = os.listdir(str)
    filelist.sort()
    print(filelist)
    
    time = []
    node_list = []
    edge_list = []
    triplet_list = []
    for j in range(len(filelist)):
        tmpfn=filelist[j]
        ##print(tmpfn)
        time.append(tmpfn[:-4])    
        content_test = open(str+tmpfn, "r").readlines()
        for i in range(1,len(content_test)):
            lines = content_test[i]
            a=lines.split(',')
            head = a[0]
            node_list.append(head)
            relation = a[1]   
            edge_list.append(relation)              
            tail = a[2][:-1]
            node_list.append(tail)
            if head != tail:
                triple = head+'@'+relation+'@'+tail
                if triple not in triplet_list:
                    triplet_list.append(triple)
    print(len(triplet_list))
    topnodes = Counter(node_list).most_common()
    topedges = Counter(edge_list).most_common()
    #print(topnodes)
    write_code('/home/user1/deskdata/JS/data2/node_code_frequence_cle.csv',list(set(node_list)))
    write_code('/home/user1/deskdata/JS/data2/edge_code_frequence_cle.csv',list(set(edge_list)))
    return topnodes,topedges
def sim(phrase1, phrase2):
    p1 = phrase1.split()
    p2 = phrase2.split()
    score = 0
    n = 0.01
    for w1 in p1:
        if w1 not in stop_words:
            n = n+1
            score_list = [0.0]
            for w2 in p2:
                if w2 not in stop_words:
                    try:
                        s_tmp = model.wv.similarity(w1,w2)
                        score_list.append(s_tmp)
                    except:
                        score_list.append(0.0)
            w1_s_m = max(score_list)
            score = score + w1_s_m
        
    return score/n
                
                
        
    

def sim_dis(nodes):
    dic_sim = {}
    while len(nodes)>=1:
        node1 = nodes[0]
        nodes.remove(node1)
        nodes2 = nodes.copy()
        tmp_list = []
        
        for node2 in nodes2:
            sim_bw = sim(node1,node2)
            if sim_bw>=0.8:
                #print(node2)
                if len(tmp_list)<10:
                    nodes.remove(node2)
                    tmp_list.append(node2)
        dic_sim[node1] = tmp_list
    return dic_sim
def sim_dis_edge(nodes):
    dic_sim = {}
    while len(nodes)>=1:
        node1 = nodes[0]
        nodes.remove(node1)
        nodes2 = nodes.copy()
        tmp_list = []
        
        for node2 in nodes2:
            sim_bw = sim(node1,node2)
            if sim_bw>=0.8:
                #print(node2)
                if len(tmp_list)<10:
                    nodes.remove(node2)
                    tmp_list.append(node2)
        dic_sim[node1] = tmp_list
    return dic_sim

model = gensim.models.Word2Vec.load('/home/user1/deskdata/JS/data2/model_JS2')
topnode_frequence, topedge_frequence= encode_node('/home/user1/deskdata/JS/data2/edge_fre_clear/')
#=====================================================================================

#node_list,id2node_dic,node2id_dic = read_file('/home/user1/deskdata/JS/data1/node_code_frequence_cle.csv')
new_node_list = []
for tf in topnode_frequence:
    if tf[1]>2:
        new_node_list.append(tf[0])
print(len(new_node_list))
new_node_list1 = new_node_list.copy()
cluster = sim_dis(new_node_list1)

old2new_dic = {}
for key, value in cluster.items():
    old2new_dic[key] = key
    try:
        for node in value:
            old2new_dic[node] = key
    except:
        pass
#--------------------------------------------------------------------------------------------------------
new_edge_list = []
for tf in topedge_frequence:
    if tf[1]>1:
        new_edge_list.append(tf[0])
print(len(new_edge_list))
new_edge_list1 = new_edge_list.copy()
cluster_edge = sim_dis_edge(new_edge_list1)

old2new_edge_dic = {}
for key, value in cluster_edge.items():
    old2new_edge_dic[key] = key
    try:
        for node in value:
            old2new_edge_dic[node] = key
    except:
        pass
#----------------------------------------------------------------------------------------------
filelist = os.listdir(r'/home/user1/deskdata/JS/data2/edge_fre_clear/')
filelist.sort()

#time = []
node_list = []
edge_list = []
all_node = []
for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    ##print(tmpfn)
    #time.append(tmpfn[:-4])
    triplet_set = []
    

    content_test = open('/home/user1/deskdata/JS/data2/edge_fre_clear/'+tmpfn, "r").readlines()
    for i in range(1,len(content_test)):
        lines = content_test[i]
        a=lines.split(',')
        head = a[0]
        relation = a[1]                 
        tail = a[2][:-1]
        try:
            head_new = old2new_dic[head]
            tail_new = old2new_dic[tail]
            relation_new = old2new_edge_dic[relation]

            if head_new != tail_new:
                triple = head_new+'@'+relation_new+'@'+tail_new
                triplet_set.append(triple)
        except:
            triplet_set = triplet_set
    #write_file('/home/user1/deskdata/JS/data2/edge_after_embedding/'+tmpfn,list(set(triplet_set)))
    write_KG('/home/user1/deskdata/JS/data2/knowledge_graph/file_'+str(j+1)+'.csv',list(set(triplet_set)))
    
    
