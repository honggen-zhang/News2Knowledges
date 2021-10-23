import pandas as pd 
import os
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize, word_tokenize 
import warnings 
import string
from operator import itemgetter
from nltk.corpus import stopwords 
from gensim.models.phrases import Phrases, Phraser
warnings.filterwarnings(action = 'ignore') 
from nltk.stem.wordnet import WordNetLemmatizer
import gensim 
from gensim.models import Word2Vec 
from nltk.corpus import stopwords
stop_words = list(stopwords.words('english'))
stop_words.remove('s')

import glob
os.chdir('/home/user1/deskdata/JS/gossip/TXT/')
read_files = glob.glob("*.txt")
i = 0
with open("/home/user1/deskdata/JS/gossip/newfile.txt", "wb") as outfile:
    for f in read_files:
        f = 'file_'+str(i)+'.txt'
        print(f)
        i =i+1
        with open(f, "rb") as infile:
            outfile.write(infile.read())


# Reads ‘alice.txt’ file 
sample = open("/home/user1/deskdata/JS/gossip/newfile.txt", "r") 
s = sample.read() 

# Replaces escape character with space 
f = s.replace("\n", " ") 

data = [] 

# iterate through each sentence in the file 
#sent = [row.split() for row in sent_tokenize(f)]

for i in sent_tokenize(f):
    temp = []
    for j in i.split(): 
        if j.lower() not in stop_words:
            
            try:
                w1 = WordNetLemmatizer().lemmatize(j.lower(),'v')
            except:
                w1 = j.lower()
            temp.append(w1)
    data.append(temp) 
# =============================================================================
# phrases = Phrases(data, min_count=5, progress_per=10000)
# bigram = Phraser(phrases)
# sentences = bigram[data]
# =============================================================================
#print(data)
# Create CBOW model 
model1 = gensim.models.Word2Vec(data, min_count = 5, 
							size = 50, window = 6) 
model1.save('/home/user1/deskdata/JS/gossip/model_bignews11')
#model = gensim.models.Word2Vec.load('/home/user1/deskdata/JS/gossip/model_bignews')
