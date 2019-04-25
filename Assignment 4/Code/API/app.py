import flask
from flask import request, make_response
import tensorflow as tf
from keras.models import load_model
from google.cloud import translate
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from stemming.porter2 import stem
import string
import re
import pickle
from tensorflow import keras
import json
from flask import render_template

file=open('model/vectorizer.pkl', 'rb')

kwargs=pickle.load(open('model/kwargs.pkl', 'rb'))

loaded_vec = pickle.load(file)

def init():
    global load_model,graph,loaded_vec
    # load the pre-trained Keras model
    json_file = open('model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    load_model = tf.keras.models.model_from_json(loaded_model_json)
    load_model.load_weights("model/model_weights.h5")
    graph = tf.get_default_graph()
    #loaded_vec = TfidfVectorizer(vocabulary=vectorizer)

# Use pickle to load in the pre-trained model.
app = flask.Flask(__name__, template_folder='templates')

# load weights into new model
@app.route('/', methods=['GET','POST'])
def loadmain():
    return render_template('index.html')
@app.route('/predict-song', methods=['GET','POST'])
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
        song = flask.request.form['song']

        translate_client = translate.Client.from_service_account_json('key.json')
        song=[song]
        target = 'en'
        translation = translate_client.translate(song[0],target_language=target)
        tsong=format(translation['translatedText'])
        init()
        x_input = loaded_vec.transform([tsong])
        prediction = int(np.round(load_model.predict(x_input))[0])
        data = {}
        if(int(prediction)==1):
            data['Prediction'] = 'Sad'
        else:
            data['Prediction'] = 'Happy'
        json_data = json.dumps(data)
        resp = make_response(json_data)
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        #prediction = 1
        return resp
        #return render_template('main.html', result = data)
if __name__ == '__main__':
    app.run()
