import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from textblob import TextBlob, Word
import pickle
import flask
from flask import render_template
import json
from flask import request, make_response
import nltk
import tweepy
import smtplib
from flask import Flask
from flask_mail import Mail, Message

def lemmatize_with_postag(sentence):
    sent = TextBlob(sentence)
    tag_dict = {"J": 'a', 
                "N": 'n', 
                "V": 'v', 
                "R": 'r'}
    words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
    lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
    return " ".join(lemmatized_list)
def remove_stopwords(review_words):
    all_texts=[]
    with open('vectorizer/stopwords_eng.txt') as stopfile:
        stopwords = stopfile.read()
        list = stopwords.split()
        for item in review_words.split():
            if not item in list:
                all_texts.append(item)
    return all_texts

# Lemmatize
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(60)
def send_mail(gmail_user,gmail_password,send_from, send_to, subject, text,filename):

    app = Flask(__name__)

    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": gmail_user,
        "MAIL_PASSWORD": gmail_password
    }
    app.config.update(mail_settings)
    mail = Mail(app)
    msg = Message(subject=filename+" Twitter sentiment Report",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=send_to, # replace with your email for testing
                      body="PFA "+filename)
    with app.open_resource(filename) as fil:
        msg.attach(filename,"text/csv",fil.read())
        # After the file is closed
    mail.send(msg)
    

file=open('vectorizer/tfidfvectorizer.pkl', 'rb')

loaded_vec = pickle.load(file)

model_path="model/"
loaded_model = mlflow.sklearn.load_model(model_path)

model_path2="model2/"
loaded_model2 = mlflow.sklearn.load_model(model_path2)

# Use pickle to load in the pre-trained model.
app = flask.Flask(__name__, template_folder='templates')

# load weights into new model
@app.route('/', methods=['GET','POST'])
def loadmain():
    return render_template('index.html')
@app.route('/sentiment-report', methods=['GET','POST'])
def loadSentiment():
    return render_template('sentiment.html')
@app.route('/predict-sentiment', methods=['GET','POST'])
def main():
    if flask.request.method == 'GET':
        dataError = {}
        dataError['prediction']="Method Provided is GET. Please Try Using Post Method"
        json_data = json.dumps(dataError)
        resp = make_response(json_data)
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        #prediction = 1
        return resp
    if flask.request.method == 'POST':
        text = flask.request.form['text']
        text=lemmatize_with_postag(text)
        all_texts=remove_stopwords(text)    

        data = pd.Series(str(items) for items in [all_texts])


        x_input = loaded_vec.transform(data)
        yTPred=loaded_model.predict(x_input)
        rounded = [np.round(x) for x in yTPred]
        value={}
        if(rounded[0]==1):
            value['Prediction'] = 'Neutral'
        elif(rounded[0]==0):
            value['Prediction'] = 'Negative'
        else:
            value['Prediction'] = 'Positive'

        json_data = json.dumps(value)
        resp = make_response(json_data)
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        #prediction = 1
        return resp
        #return render_template('main.html', result = data)
@app.route('/recommend-sent', methods=['GET','POST'])
def mainRecommend():
    if flask.request.method == 'POST':
        val=[]
        ads = flask.request.form['ads']
        cost=flask.request.form['cost']
        recommendation=flask.request.form['recommendation']
        stability=flask.request.form['stability']
        if(cost=='NoPref'):
            val.append(0)
            val.append(0)
        elif(cost=='Low'):
            val.append(1)
            val.append(0)
        else:
            val.append(0)
            val.append(1)
        if(recommendation=='NoPref'):
            val.append(0)
            val.append(0)
        elif(recommendation=='Low'):
            val.append(0)
            val.append(1)
        else:
            val.append(1)
            val.append(0)
        if(stability=='NoPref'):
            val.append(0)
            val.append(0)
        elif(stability=='Low'):
            val.append(0)
            val.append(1)
        else:
            val.append(1)
            val.append(0)
        if(ads=='NoPref'):
            val.append(0)
            val.append(0)
        elif(ads=='Low'):
            val.append(1)
            val.append(0)
        else:
            val.append(0)
            val.append(1)
        val_arr=[]
        val_arr.append(val)
        ypred=loaded_model2.predict(val_arr)
        value={}

        if(ypred[0]==1):
            value['Result'] = 'Spotify'
        elif(ypred[0]==2):
            value['Result'] = 'Pandora'
        elif(ypred[0]==3):
            value['Result'] = 'Apple Music'
        else:
            value['Result'] = 'Amazon Music'
        json_data = json.dumps(value)
        resp = make_response(json_data)
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        #prediction = 1
        return resp
@app.route('/report-sent', methods=['GET','POST'])
def mainReport():
    if flask.request.method == 'POST':
        text = flask.request.form['tag']
        auth = tweepy.OAuthHandler('h2Ec61T4KdLdbwfIiugdgSjg5', 'SfS5AGPyN2hovxElLi8SIb0ViIhWtTzZUAAPyG80aIRguAoiIH')
        auth.set_access_token('112085069-uzxDSeJiPUMv0qOCiLi3kVLdIXGu0krjqaOngD3O', 'xGF2kyvNRj5tOQ29eudp7UBkKc9s039zFewlTapgHNTZo')
        pageCount=flask.request.form['pageCount']
        api = tweepy.API(auth,wait_on_rate_limit=True)

        public_tweets = api.home_timeline()
        c=tweepy.Cursor(api.search, q='%23'+text)
        c.pages(int(pageCount))
        Tweet_Text = []
        Tweet_Id=[]
        Tweet_Creator=[]
        Tweet_Date=[]
        Data={}
        j=0
        for tweet in c.items():
            j=j+1
            if tweet.lang == 'en':
                createdAt = str(tweet.created_at)
                Tweet_Text.append(tweet.text)
                Tweet_Date.append(createdAt)
                Tweet_Creator.append(tweet.user._json['screen_name'])
                Tweet_Id.append(j)
        Data["Id"]=Tweet_Id
        Data["Creator"]=Tweet_Creator
        Data["Text"]=Tweet_Text
        Data["Date"]=Tweet_Date
        df = pd.DataFrame(Data)
        all_texts=[]
        for data in df['Text']:
            sentence=lemmatize_with_postag(data)
            all_texts.append(remove_stopwords(sentence))

        data = pd.Series(str(items) for items in all_texts)
        x_input = loaded_vec.transform(data)
        yTPred=loaded_model.predict(x_input)
        rounded = [np.round(x) for x in yTPred]
        new_items = ['Neutral' if x == 1 else 'Negative' if x==0 else 'Positive' for x in rounded]
        df["Sentiment"]=new_items
        df.to_csv(text+'Report.csv')

        gmail_user = flask.request.form['email']  
        gmail_password = flask.request.form['pwd']
        sent_list=flask.request.form['sentlist'].split(',')

        send_mail(gmail_user,gmail_password,gmail_user,sent_list,text+'Twitter sentiment Report','PFA',text+'Report.csv')
        value={}

        value['Result'] = 'Success'
        json_data = json.dumps(value)
        resp = make_response(json_data)
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        #prediction = 1
        return resp
if __name__ == '__main__':
    app.run()
