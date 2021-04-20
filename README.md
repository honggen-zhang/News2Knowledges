# News2Knowledges
The project is tring to transfrom the news articles to Knowledge graphs. The following steps are the procesures of building knowledge graphs from download dataset.
## Step1 samples
Becasue of large dataset, it will be spend a lot on data clearence and graph computation. We random sampled around 2k articles for each data sample. The 2k articles slelcted based on the URL. Firstly, we obtain a dictionary whose key is the source and vlaue is the corresponding count. We selected the news source randomly untill the sum of count reach to 2k. Secondly, we filter out the data sample based on such sources. 

Step1 refers to two scripts, the **random sources sampling.py** used to generate sources list, and the  **samples_based_web.py** used to generate the raw data.

## Step2 Coreference





