import io
import nltk
import os
import math
import re
import csv
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from pdfminer.layout import LAParams

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
        text = fake_file_handle.getvalue().lower()
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
    # close open handles
    converter.close()
    fake_file_handle.close()
    if text:
        return text
filePath=[]
bloblist = []
for file in os.listdir("C:/ADS/A1_HiringTrends/Data/To_Parse"):
    if file.lower().endswith(".pdf"):
        filePath.append(os.path.join("C:/ADS/A1_HiringTrends/Data/To_Parse", file))
datatext=''
lem = WordNetLemmatizer()
stem = PorterStemmer()
for path in filePath:
    datatext+='\n'+extract_text_from_pdf(path).lower()
stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(datatext)
filtered_sentence = []
for w in word_tokens:
    if w not in stop_words:
        #w=stem.stem(w)
        filtered_sentence.append(w)
fdist1 = nltk.FreqDist(filtered_sentence)
wtr = csv.writer(open ('C:/ADS/A1_HiringTrends/Data/Generated/By Algorithms/WordCount.csv', 'w'), delimiter=',', lineterminator='\n')
    #writer = csv.writer(f)
x=1
for row in fdist1.most_common(500):
    wtr.writerow([str(x)] + [row[0]])
    x+=1
#f.close()
