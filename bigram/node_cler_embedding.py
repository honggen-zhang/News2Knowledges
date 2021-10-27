#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 23:20:22 2021

@author: user1
"""

import gensim 
from gensim.models import Word2Vec 
from nltk.stem.wordnet import WordNetLemmatizer
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
import numpy as np

def write_KG(str,all_triplets):
    triple_all = []
    with open(str, 'w', newline='') as csvfile:
        fieldnames = ['Source', 'Target','Label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        for node in all_triplets:
            if node not in triple_all:
                triple_all.append(node)
                a = node.split('@')
                writer.writerow({'Source': a[0], 'Target': a[2],'Label':a[1]})
def write_file(str,all_triplets,sentences_all):
    triples_all = []

    with open(str, 'w', newline='') as csvfile:
        fieldnames = ['head', 'relation','tail','sentences']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        for k in range(len(all_triplets)):
            node = all_triplets[k]
            if node not in triples_all:
                triples_all.append(node)
                a = node.split('@')
                #print(node)
                writer.writerow({'head': a[0], 'relation': a[1],'tail':a[2],'sentences':sentences_all[k]})

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

def bi_gram(head):
    new_head = []
    head_list = head.split()
    nn = 0
    while nn < len(head_list)-1:
        bi_words = '_'.join(head_list[nn:nn+2])
        try:
            #print(bi_words)
            model.wv[bi_words] 
            new_head.append(bi_words)
            nn = nn+2
        except:
            if nn == len(head_list)-2:
                new_head.append(head_list[nn])
                new_head.append(head_list[nn+1])
            else:
                new_head.append(head_list[nn])
            nn = nn+1
    return ' '.join(new_head)
            

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
            if len(head.split())>=2:
                head = bi_gram(head)

                        
            node_list.append(head)
            relation = a[1]   
            if len(relation.split())>=2:
                relation = bi_gram(relation)
            edge_list.append(relation)   
            
            tail = a[2]
            if len(tail.split())>=2:
                tail = bi_gram(tail)
            node_list.append(tail)
            #if head != tail:
            triple = head+'@'+relation+'@'+tail
            if triple not in triplet_list:
                triplet_list.append(triple)
    print(len(triplet_list))
    
    topnodes = Counter(node_list).most_common()
    topedges = Counter(edge_list).most_common()
    #print(topedges)
    write_code('/home/user1/Desktop/Big_Gossip/node_code_frequence_cle.csv',list(set(node_list)))
    write_code('/home/user1/Desktop/Big_Gossip/edge_code_frequence_cle.csv',list(set(edge_list)))
    return topnodes,topedges
def sim(phrase1, phrase2):
    p1 = phrase1.split()
    p2 = phrase2.split()
    score = 0
    n = 0.001
    if len(set(p1).intersection(set(p2))) != 0:
        #print(p1)
        #print(p2)
        for w1 in p1:
        #if w1 not in stop_words:
            n = n+1
            score_list = []
            for w2 in p2:
            #if w2 not in stop_words:
                try:
                    s_tmp = model.wv.similarity(w1,w2)
                    score_list.append(s_tmp)
                except:
                    score_list.append(0.0)
            w1_s_m = np.average(score_list)
            #print(w1,p2,score_list)
            score = score + w1_s_m
        
    return score/n
                
def sim_edge(phrase1, phrase2):
    p1 = phrase1.split()
    p2 = phrase2.split()
    score = 0
    n = 0.001
    
        #print(p1)
        #print(p2)
    for w1 in p1:
        score_list = []
        if w1 not in stop_words:
# =============================================================================
#             try:
#                 w1 = WordNetLemmatizer().lemmatize(w1,'v')
#             except:
#                 w1 = w1
# =============================================================================
            n = n+1
                #score_list = []
            for w2 in p2:
                if w2 not in stop_words:
# =============================================================================
#                     try:
#                         w2 = WordNetLemmatizer().lemmatize(w2,'v')
#                     except:
#                         w2 = w2
# =============================================================================
                    
                    if w1 == w2:
                        s_tmp = 1
                    else:
                        try:
                            s_tmp = model.wv.similarity(w1,w2)
                            #print(w1,w2,s_tmp)
                            
                        except:
                            s_tmp = 0.0
                    score_list.append(s_tmp)
            w1_s_m = np.average(score_list)
            #print(w1_s_m)
            score = score + w1_s_m
        
    return score/n                
        
def sim_dis(keynodes,allnodes):
    dic_sim = {}
    while len(keynodes)>=1:
        node1 = keynodes[0]
        keynodes.remove(node1)
        try:
            allnodes.remove(node1)
        except:
            pass
        nodes2 = allnodes.copy()
        tmp_list = []
        #print('node1:--',node1)
        for node2 in nodes2:
            sim_bw = sim(node1,node2)
            if sim_bw>=0.8:
                #print(node2)
                if len(tmp_list)<50:
                    allnodes.remove(node2)
                    tmp_list.append(node2)
                    try:
                        keynodes.remove(node2)
                    except:
                        pass
        dic_sim[node1] = tmp_list
    for node in allnodes:
        dic_sim[node]=[]
    return dic_sim    


def sim_dis_edge(nodes):
    dic_sim = {}
    while len(nodes)>=1:
        node1 = nodes[0]
        nodes.remove(node1)
        nodes2 = nodes.copy()
        tmp_list = []
        
        for node2 in nodes2:
            sim_bw = sim_edge(node1,node2)
            #print(node1,'--',node2,'--',sim_bw)
            if sim_bw>=0.7:
                #print(sim_bw)
                if len(tmp_list)<50:
                    nodes.remove(node2)
                    tmp_list.append(node2)
        dic_sim[node1] = tmp_list
    return dic_sim

model = gensim.models.Word2Vec.load('/home/user1/deskdata/JS/bignews/model_bignews')
topnode_frequence, topedge_frequence= encode_node('/home/user1/deskdata/JS/bignews/edge_fre_clear/')
#=====================================================================================

#node_list,id2node_dic,node2id_dic = read_file('/home/user1/deskdata/JS/data1/node_code_frequence_cle.csv')
new_node_list = []
keynodes_list = []
for tf in topnode_frequence:
    #if tf[1]>2:
    new_node_list.append(tf[0])
    if tf[1]>6:
        keynodes_list.append(tf[0])
        
print(len(new_node_list))

new_node_list1 = new_node_list.copy()
keynodes = keynodes_list.copy()
#cluster = sim_dis(new_node_list1)
cluster = sim_dis(keynodes,new_node_list1)
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
    #if tf[1]>1:
    new_edge_list.append(tf[0])

new_edge_list1 = new_edge_list.copy()
Counter(new_edge_list1).most_common()
cluster_edge = sim_dis_edge(new_edge_list1)

old2new_edge_dic = {}
for key, value in cluster_edge.items():
    old2new_edge_dic[key] = key
    try:
        for node in value:
            old2new_edge_dic[node] = key
    except:
        pass
print('done-------------')
#----------------------------------------------------------------------------------------------
filelist = os.listdir(r'/home/user1/deskdata/JS/bignews/edge_fre_clear/')
filelist.sort()

#time = []
node_list = []
edge_list = []
all_node = []
for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    tmpfn = 'file_'+str(j)+'.csv'
    #time.append(tmpfn[:-4])
    print(tmpfn)
    triplet_set = []
    sentences_set = []
    

    content_test = open('/home/user1/deskdata/JS/bignews/edge_fre_clear/'+tmpfn, "r").readlines()
    for i in range(1,len(content_test)):
        lines = content_test[i]
        a=lines.split(',')
        head = a[0]
        if len(head.split())>=2:
            head = bi_gram(head)        
        relation = a[1]  
        if len(relation.split())>=2:
            relation = bi_gram(relation)                 
        tail = a[2]
        if len(tail.split())>=2:
            tail = bi_gram(tail)  
        try:
            head_new = old2new_dic[head]
            tail_new = old2new_dic[tail]
            relation_new = old2new_edge_dic[relation]

            if head_new != tail_new:
                triple = head_new+'@'+relation_new+'@'+tail_new
                triplet_set.append(triple)
                sentences_set.append(a[3:])
        except:
            triplet_set = triplet_set
            sentences_set = sentences_set
    write_file('/home/user1/deskdata/JS/bignews/KG_with_sentence/'+tmpfn,list(triplet_set),sentences_set)
    write_KG('/home/user1/deskdata/JS/bignews/knowledge_graph/file_'+str(j+1)+'.csv',list(triplet_set))
      