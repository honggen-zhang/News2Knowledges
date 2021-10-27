"""
Created on Tue Oct 12 17:56:30 2021

@author: user1
Fast coreference method. We only collect tripels with strong confidence a[11]

Process triples every four sentences

"""
import os
from collections import Counter
import pandas as pd
import spacy
import neuralcoref
#nlp = spacy.load('en_core_web_lg')
nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)
pronorn_list = ['him','it','he','they','his','us','her','she','their','we','my','its','himself','them','that','which','i','you','me','your','herself','themselves']
def pronorn(current_sentences):
    v = ' '
    doc1 = nlp(v.join(current_sentences))
    coreference_word = doc1._.coref_clusters
    dic_e2pronorn = {}
    #print(coreference_word[1][1:])
    
    try:
        for e in coreference_word:
            #print(e)
            for value in e[1:]:
                #print(value)
                if str(value) in pronorn_list:
                    dic_e2pronorn[str(value)] = e[0]
    except:
        pass
    #print(dic_e2pronorn)
    return dic_e2pronorn
    
def replace(entity,dic_):
    #print(dic_)
    #print(dic_['his'])
    new_node_all = []
    for node in entity:
        b = node.split(' ')
        if b[0] in pronorn_list:
            #print(b[0])
            try:
                true_e = str(dic_[str(b[0])])
                try:
                    #print(b[1:])
                    newB = [true_e]+b[1:]
                    #print(newB)
                    new_node = ' '.join(newB)
                    #print(new_node)
                    
                except:
                    new_node = true_e
                    
            except:
                #print(b)
                new_node = node
        else:
            new_node = node
        #if node != new_node:
            #print(node+'--->',new_node)
        #if new_node not in pronorn_list:
        new_node_all.append(new_node)
    return new_node_all
        
def coreference(filename):            
    content_test = open('/home/user1/deskdata/JS/gossip/reverb/'+filename, "r").readlines()
    triples_all = []
    head = []
    tail = []
    edge = []
    scores = []
    sentences = []
    s_current = []
    core_node = []
    bigdata = []
    for i in range(len(content_test)):
            
        lines = content_test[i].lower()
        a=lines.split('\t')
        
        if float(a[11])>=0.7:#only collect triples with socre large than 0.7
            if a[12] not in s_current and len(s_current)<= 4:
                s_current.append(a[12])
            #triple = a[2]+'@'+a[3]+'@'+a[4]
            #if triple not triple_all
            #triples_all.append(triple)
            head.append(a[2])
            tail.append(a[4])
            edge.append(a[3])
            scores.append(a[11])
            sentences.append(a[12])
            if len(s_current) == 4:
                dic_pro = pronorn(s_current)  
                new_head = replace(list(head),dic_pro)
                new_tail = replace(list(tail),dic_pro)
                core_node = core_node+new_head+new_tail
                for k in range(len(new_head)):
                    triple = new_head[k]+'@'+edge[k]+'@'+new_tail[k]
                    if triple not in triples_all:
                        data = {}
                        data['subj']=new_head[k]
                        data['relation']=edge[k]
                        data['obj']=new_tail[k]
                        data['score']=scores[k]
                        data['sentence']=sentences[k]
                        bigdata.append(data)
                        triples_all.append(triple)
                s_current.clear()
                head.clear()
                tail.clear()
                edge.clear()
                scores.clear()
                sentences.clear()
    dic_node = {}
    for tri in triples_all:
        a = tri.split('@')
        head = a[0]
        tail = a[2]
        relation = a[1]
        nodes = head+'@'+tail
        dic_node[nodes] = []
    for tri in triples_all:
        a = tri.split('@')
        head = a[0]
        tail = a[2]
        relation = a[1]
        nodes = head+'@'+tail
        dic_node[nodes].append(relation)
    
    df=pd.DataFrame.from_dict(bigdata)
    df.to_csv('/home/user1/deskdata/JS/gossip/coreference/'+filename,index=False)

filelist = os.listdir(r'/home/user1/deskdata/JS/gossip/reverb/')
for j in range(len(filelist)):
    tmpfn=str(filelist[j])
    tmpfn = 'file_'+str(j)+'.csv'
    print(tmpfn)
    coreference(tmpfn)
