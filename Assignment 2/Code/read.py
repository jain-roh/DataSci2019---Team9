import requests
import csv
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import lxml
import csv
from collections import defaultdict
import pandas as pd
import numpy as np
import os

#from lxml import etree

#import urllib
from urllib.request import urlopen
abcd = {}
dataset=[]
link=[]
institution = []
position =[]
df1 = pd.read_csv(os.getcwd()+"\\final_file.csv",header=None,names=["0","words"])
#df = pd.read_csv("Z:/ADS/a/textrank_final.csv")
with open(os.getcwd()+"\\final_file.csv",encoding="utf8", newline='') as myFile:
    reader1 = csv.reader(myFile)
    for row1 in reader1:
        data = row1[2]
        data = data.lower()
        stop_words = set(stopwords.words("english"))
		#remove tags
        data=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",data)
		# remove special characters and digits
        data=re.sub("(\\d|\\W)+"," ",data)
		##Convert to list from string
        data = data.split()
		#Lemmatisation
        lem = WordNetLemmatizer()
        data = [lem.lemmatize(word) for word in data if not word in stop_words]
        data = " ".join(data)
        dataset.append(data)
        #dataset.append(row1[2])
        link.append(row1[0])
        institution.append(row1[3])
        position.append(row1[1])
#print(abc)
x = 1
abc=[]
df = pd.read_csv(os.getcwd()+"\\keywords.csv",header=None,names=["0","words"])
#df = pd.read_csv("Z:/ADS/a/textrank_final.csv")
with open(os.getcwd()+"\\keywords.csv", newline='') as myFile:
    reader = csv.reader(myFile)
    for row in reader:
        abc.append(row[1])

for text in dataset:
        #print(text)
    thisline = text.split(" ");
    #print(thisline)
    for q in abc:
        #print(row)
        for wd in thisline:
            #print(wd)
            if q == wd:
                if wd in abcd:
                    abcd[wd] +=1

                else:
                    abcd.update({wd:1})
                        #abcd[wd] = 1

    df[x]= df['words'].map(abcd)
    x +=1
    abcd.clear()
#df
#df2 = df.drop(df.column2)
df2_transposed = df.transpose() # or df2.transpose()
df2_transposed2 = df2_transposed.drop(df2_transposed.index[1])

#df2_transposed2.insert(loc=0, column='Job No',value='')
df2_transposed2.insert(loc=0, column='Institutation',value='')
df2_transposed2.insert(loc=1, column='URL(url of job posting)',value='')
df2_transposed2.insert(loc=2, column='Position',value='')
#df2_transposed2.insert(loc=4, column='Location',value='')
df2_transposed2.insert(loc=3, column='Description',value='')
#df2_transposed2
q=1
m=1
o=1
d=1
for dd in dataset:
    df2_transposed2.iloc[q,3] = dd
    q+=1
for p in position:
    df2_transposed2.iloc[m,2] = p
    m+=1
for l in link:
    df2_transposed2.iloc[o,1] = l
    o+=1
for inst in institution:
    df2_transposed2.iloc[d,0] = inst
    d+=1
#df2_transposed2['Location'] = df2_transposed2['Location'].map(lambda x: str(x)[23:])
df2_transposed2 = df2_transposed2.replace(np.nan, 0)
df2_transposed2 = df2_transposed2.replace('\n','', regex=True)
df2_transposed2 = df2_transposed2.replace('\t','', regex=True)
df2_transposed2.to_csv(os.getcwd()+"\\data_final.csv",index=False, encoding='utf8')
