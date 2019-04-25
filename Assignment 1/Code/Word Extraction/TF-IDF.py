# libraries
from __future__ import division
import string
import collections
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
from tika import parser
import glob
import os
import codecs
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from rake_nltk import Metric, Rake

# set nlp variables
default_stopwords = stopwords.words('english')
lemmatizer = nltk.stem.WordNetLemmatizer()

# We're adding some on our own stopwords
#stopwords_filepath = 'C:\\Users\\kesha\\Documents\\Data Science\\Assignment1\\fintech pdfs\\custom_stopwords.txt'
#stopwords_file = codecs.open(stopwords_filepath, 'r', 'utf-8')
#custom_stopwords = list(stopwords_file.read().splitlines())
#stopwords_file.close()
#all_stopwords = default_stopwords + custom_stopwords

# create nlp functions
def clean_tokens(tokens):
    """ Lowercases, takes out punct and stopwords and short strings """
    return [token.lower() for token in tokens if (token not in string.punctuation) and
                   (token.lower() not in default_stopwords) and len(token) > 2]

def lemmatize(tokens):
    """ Removes plurals """
    return [lemmatizer.lemmatize(token) for token in tokens]

def count_ngrams(tokens,n):
    n_grams = ngrams(tokens, n)
    ngram_freq = collections.Counter(n_grams)
    ngram_freq = ngram_freq.most_common()
    return ngram_freq

def ngram_to_dict(ngram_freq):
    l = []
    for t in ngram_freq:
        l.append((' '.join(t[0]),t[1]))
    return dict(l)

word_dict = {}
bigram_dict = {}
trigram_dict = {}
ngram_dict = {}
tokenized_doc = []

if os.path.exists("C:/ADS/A1_HiringTrends/Data/To_Parse/MergedFile.txt"):
  os.remove("C:/ADS/A1_HiringTrends/Data/To_Parse/MergedFile.txt")

#Merge data into single file
pdf_files = sorted(glob.glob('C:/ADS/A1_HiringTrends/Data/To_Parse/*.pdf'))
for f in pdf_files:
    raw = parser.from_file(f)
    tokens = nltk.word_tokenize(raw['content'])
    clean = clean_tokens(tokens)
    lem = lemmatize(clean)
    lemdoc = lem
    tokenized_doc.append(lemdoc)
    f = open("C:/ADS/A1_HiringTrends/Data/To_Parse/MergedFile.txt","a+",encoding='utf8')
    f.write(raw['content'])
    f.close()

#Convert text to word tokens
input_file = 'C:/ADS/A1_HiringTrends/Data/To_Parse/MergedFile.txt'
fp = codecs.open(input_file, 'r', 'utf-8')
tokens = nltk.word_tokenize(fp.read())
fp.close()

#Clean data
clean = clean_tokens(tokens)
lem = lemmatize(clean)

# count word and ngram frequency
word_freq = count_ngrams(lem, 1)
bigram_freq = count_ngrams(lem, 2)
trigram_freq = count_ngrams(lem, 3)
ngram_freq = word_freq + bigram_freq + trigram_freq

#WordCount after cleaning [START]
unsorted_dict = ngram_to_dict(word_freq)
sorted_dict = sorted(unsorted_dict.items(),key=lambda x: x[1], reverse=True)  # By Value Backwards
sorted_dict = sorted_dict[0:100]
if os.path.exists("C:/ADS/A1_HiringTrends/Data/Generated/By Algorithms/TF-IDF.csv"):
  os.remove("C:/ADS/A1_HiringTrends/Data/Generated/By Algorithms/TF-IDF.csv")

csvData= [['Word', 'Frequency']]

for word, frequency in sorted_dict:
   csvData.append([word,frequency])

with open('C:/ADS/A1_HiringTrends/Data/Generated/By Algorithms/TF-IDF.csv', 'w', newline='',encoding='utf8') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)

csvFile.close()
#WordCount after cleaning [END]

#TFIDF [START]
def dummy_fun(doc):
    return doc

tfidf = TfidfVectorizer(analyzer='word', stop_words='english', tokenizer=dummy_fun,
    preprocessor=dummy_fun,
    token_pattern=None, use_idf=True)
response = tfidf.fit_transform(tokenized_doc)
weights = np.asarray(response.mean(axis=0)).ravel().tolist()
weights_df = pd.DataFrame({'Term': tfidf.get_feature_names(), 'Weight': weights})
weights_df.sort_values(by='Weight', ascending=False).head(500)
#print(weights_df.sort_values(by='Weight', ascending=False).head(100))
#print(len(tokenized_doc))
if os.path.exists("C:/ADS/A1_HiringTrends/Data/Generated/By Algorithms/TF-IDF.csv"):
  os.remove("C:/ADS/A1_HiringTrends/Data/Generated/By Algorithms/TF-IDF.csv")

export_csv = weights_df.sort_values(by='Weight', ascending=False).head(500).to_csv("C:/ADS/A1_HiringTrends/Data/Generated/By Algorithms/TF-IDF.csv", index = None, header=True)
