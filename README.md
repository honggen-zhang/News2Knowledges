# News2Knowledges
The project is tring to transfrom the news articles to Knowledge graphs. The following steps are the procesures of building knowledge graphs from download dataset.
## Step1 samples
Becasue of large dataset, it will be spend a lot on data clearence and graph computation. We random sampled around 2k articles for each data sample. The 2k articles slelcted based on the URL. Firstly, we obtain a dictionary whose key is the source and vlaue is the corresponding count. We selected the news source randomly untill the sum of count reach to 2k. Secondly, we filter out the data sample based on such sources. 

Step1 refers to two scripts, the **random sources sampling.py** used to generate sources list, and the  **samples_based_web.py** used to generate the raw data. When we attempt to generate the samples, we also remove brackets, emoji, and space.

## Step2 ReVerb
Then, the ReVerb API was used to extract triplets from sample name.txt folder.

Download the latest ReVerb jar from http://reverb.cs.washington.edu/reverb-latest.jar

Runing The following commond to deal with batch of files:
```bash
for i in {1..44}; do java -Xmx512m -jar /home/user1/reverb-latest.jar /home/user1/deskdata/IranPlane/JS/Js_gossip_n/file_$i.txt > /home/user1/deskdata/IranPlane/JS/reverb_gossip/file_$i.csv; done^C
```

## Step3 Coreference
Based on the observation on raw triplet data generated by ReVerb, we attempt to relace the pronorn with entites. Note that we not only relpace single pronoun words, but also try to find the phrase with pronoun, such as 'her message'. Here is the pronoun list:
['him','it','this','he','they','his','us','her','she','their','we','my','its','himself','them','that','which','i','you','me','your','herself','themselves']   

However, we cannot replace all pronoun using the NeuralCoref 4.0(https://github.com/huggingface/neuralcoref). 

## Step4 Deep clearence

In this step, we try to clear the duplicate triplets refer to the head, relation and tail. We will call both head and tail as node in the following.

A: Clearing pronorn in a phrase using **node_cler_noise.py**.

B:**node_cler_frequence.py:** When two node phrase have at least 50% common words except the stopwords, we can see them as the same nodes. For relation phrases, we also conser some specific 
words such as ''not''. This operation make it easer for the comparsion of phrase based on embedding in the next operation.

C: **node_cler_embedding.py:** If two phrases have the similarity value larger than 0.8, we can see the two phrases as the same. We define the phrase similarity fucntion 
```def sim(phrase1, phrase2):```
We aslo discard the nodes with apperance less than 3, and the relations with apperance less than 2. 

After the deep clearence procedure, we finally obtain clear Knowledge graphs.


| Samples | #ReVerb (nodes,relations) | #Final (nodes,relations) |
| ------- | --- | --- |
| Sample1 | 29321,20319 | 1298,1422 |
| Sample2 | 24969,17605 | 1339,1419 |



