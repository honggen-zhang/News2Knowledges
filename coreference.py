#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 15:04:08 2020

@author: user1
"""
import os
import neuralcoref
import spacy
import pandas as pd
nlp = spacy.load('en_core_web_lg')
neuralcoref.add_to_pipe(nlp)

def core_dic(coreference_list):
    pronoun_dic = {}
    
    for core in coreference_list:
        #print(core[0])
        #a = core[0]
        new_list = []
        for word in core[1:]:
            new_list.append(str(word))
        pronoun_dic[core[0]] = new_list
    #print(pronoun_dic)
    return pronoun_dic

def find_entity(pronorn, word_dic):
    for key, value in word_dic.items():
        #print(pronorn)
        #print(value[0].type())
        if pronorn in list(value):
            return key
    return pronorn

def pronorn(content_test):
    
    triplets=[]

    for i in range(0,len(content_test),20):
        
        s_current = []
        for k in range(i,i+20):
            if k<len(content_test):
            
                lines = content_test[k].lower()
                a=lines.split('\t')
                if a[12] not in s_current:
                    s_current.append(a[12])
        v = '. '        
        doc1 = nlp(v.join(s_current))
        coreference_word = doc1._.coref_clusters
        pro_dic = core_dic(coreference_word)

        
        for j in range(i,i+20):
            if j<len(content_test):
            
                data = {}
                lines = content_test[j].lower()
                a=lines.split('\t')
    
                subj = a[2]
                relation = a[3]
                obj = a[4]
                subj1 = subj.split()[0]
                obj1 = obj.split()[0]
                if subj1 in pronorn_list:               
                    sub_new = find_entity(str(subj1),pro_dic)                
                    try:
                        v = ' '
                        rest_words = v.join(subj.split()[1:])               
                        subj = sub_new+' '+str(rest_words)
                    except:
                        subj = sub_new                            
                    
                if obj1 in pronorn_list:
                    obj_new = find_entity(str(obj1),pro_dic)
                    try:                            
                        v = ' '
                        rest_words = v.join(obj.split()[1:])                            
                        obj = obj_new+' '+str(rest_words)
                    except:
                        obj = obj_new
                data['subj']=subj
                data['relation']=relation
                data['obj']=obj
                data['score']=a[11]
                data['sentence']=a[12]
                triplets.append(data)
    return triplets
        #triplets.append([subj,relation,obj])    
pronorn_list = ['him','it','this','he','they','his','us','her','she','their','we','my','its','himself','them','that','which','i','you','me','your','herself','themselves']   
filelist = os.listdir(r'/home/user1/deskdata/JS/data2/reverb2csv/')
filelist.sort()
for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    ner = []
    triplets = []
    content_test = open('/home/user1/deskdata/JS/data2/reverb2csv/'+tmpfn, "r").readlines()
    bigdata=pronorn(content_test)
    df=pd.DataFrame.from_dict(bigdata)
    print(tmpfn)
    df.to_csv('/home/user1/deskdata/JS/data2/coreference2/'+tmpfn)


            
            