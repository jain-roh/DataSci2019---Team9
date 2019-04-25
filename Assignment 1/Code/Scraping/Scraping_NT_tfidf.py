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

#from lxml import etree

#import urllib
from urllib.request import urlopen
pages = []
abcd = {}
qq=[]
count=0
testDict = defaultdict(int)
for i in range(1, 26):
    url = 'https://careers.northerntrust.com/jobs/search/8420211/page' + str(i) + '.htm'
    #print(url)
    pages.append(url)
dataset=[]
counter = 1
link=[]
#print(pages)
count = 0
for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

#print(soup)

    hash_links = soup.find(class_='job_filters_toggle jJobFiltersToggle')
    hash_links.decompose()

    job_name_list = soup.find(class_='info_listings jJobResultsListHldr')
    job_name_list_items = job_name_list.find_all('a')

    for job_name in job_name_list_items:
        #print(job_name.prettify())
        links = job_name.get('href')
        link.append(links)
        page1 = requests.get(links)
        soup1 = BeautifulSoup(page1.text, 'html.parser')
        ignore = soup.find("div",["flg_hldr","info_box","jFooter compact"])
        ignore.decompose()
        #ignore1 = soup.find(class_='info_box')
        #ignore1.decompose()
        #ignore2 = soup.find(class_='jFooter compact')
        #ignore2.decompose()
        content = soup1.find(class_='jBlock')
        data = content.get_text()
        delete = soup1.find("span","field_value font_header_light")
        delete.decompose()
        idjob = soup1.find("span","field_value")
        job_id=idjob.get_text()
        qq.append(job_id)
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
        count+=1

print(count)
#dataset = ['hi my name is financial customer financial', 'hii hii hii nmy name is customer customer customer']
#print(dataset)
x = 1
abc=[]
df = pd.read_csv("../Assignment 1/Data/Generated/By Algorithms/TF-IDF_top100.csv",header=None,names=["0","words","rate"])
#df = pd.read_csv("Z:/ADS/a/textrank_final.csv")
with open('../Assignment 1/Data/Generated/By Algorithms/TF-IDF_top100.csv', newline='') as myFile:
    reader = csv.reader(myFile)
    for row in reader:
        abc.append(row[1])
    #for row in reader:
        #print(row[1])
#print(abc)
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
    #print(abcd)
    #x = 0
    #df = pd.read_csv("Z:/ADS/a/textrank_final.csv",header=None,names=["ranking","words","rate"])
    df[x]= df['words'].map(abcd)
    x +=1
    abcd.clear()
#df
#df2 = df.drop(df.column2)
df2_transposed = df.transpose() # or df2.transpose()
df2_transposed1 = df2_transposed.drop(df2_transposed.index[1])
df2_transposed2 = df2_transposed1.drop(df2_transposed1.index[1])
#df2_transposed2.to_csv("Z:/ADS/Assignment1/file1.csv",index=False, encoding='utf8')
df2_transposed2.insert(loc=0, column='Job No',value='')
df2_transposed2.insert(loc=1, column='Institutation',value='')
df2_transposed2.insert(loc=2, column='URL(url of job posting)',value='')
df2_transposed2.insert(loc=3, column='List Id',value='')
#df2_transposed2
q=1
m=1
o=1
for a in qq:
    df2_transposed2.iloc[m,0] = a
    m+=1
for l in link:
    df2_transposed2.iloc[q,2] = l
    q+=1
inst = 'northern trust'
for o in range(o,count+1):
    df2_transposed2.iloc[o,3] = '2'
    df2_transposed2.iloc[o,1] = inst
    o+=1
df2_transposed2 = df2_transposed2.replace(np.nan, 0)
df2_transposed2.to_csv("../Assignment 1/Data/Generated/By Algorithms/final_files/TF-IDF_final_file.csv",index=False, encoding='utf8')
