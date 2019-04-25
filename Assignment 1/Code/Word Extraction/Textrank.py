from __future__ import print_function
import io
import nltk
import os
import math
import re
import csv
import editdistance
import itertools
import networkx as nx
import numpy as np
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from pdfminer.layout import LAParams
from summa import keywords
import scipy
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    converter = TextConverter(resource_manager, fake_file_handle,codec=codec, laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
        stop_words = set(stopwords.words("english"))
		#remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
		# remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
		##Convert to list from string
        text = text.split()
		#Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word,pos="v") for word in text if not word in stop_words]
        text = " ".join(text)
    if text:
        return text

filePath=[]
for file in os.listdir("C:/ADS/A1_HiringTrends/Data/To_Parse"):
    if file.lower().endswith(".pdf"):
        filePath.append(os.path.join("C:/ADS/A1_HiringTrends/Data/To_Parse", file))
datatext=''
for path in filePath:
    datatext+='\n'+extract_text_from_pdf(path).lower()

import codecs
from textrank4zh import TextRank4Keyword

text = datatext


tr4w = TextRank4Keyword()
tr4w.analyze(text=text,lower=True, window=3, pagerank_config={'alpha':0.85})

#for item in tr4w.get_keywords(200, word_min_len=2):
#    print(item.word, item.weight)

wtr = csv.writer(open ('C:/ADS/A1_HiringTrends/Data/Generated/By Algorithms/Textrank.csv', 'w'), delimiter=',', lineterminator='\n')
x = 1
for item in tr4w.get_keywords(500, word_min_len=2):
    wtr.writerow([str(x)] + [item.word] + [item.weight])
    x+=1
