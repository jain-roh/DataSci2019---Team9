# A4_MusicMoodPrediction

App hosted on Heroku (Link) : https://mood-prediction.herokuapp.com/

Documentation Link: https://codelabs-preview.appspot.com/?file_id=1guBB6MdRZQEfGpmeTlHPv2Z4a1uChJaGpvSrs7uUKU4#6

Youtube Video Link: https://youtu.be/jPBI4o8b-Gc

The Model Development Phase:

  The Code Folder contains two notebooks:
  1. Main notebook (MusicMood_SongClassification) that has been used to implement the model (MLP) for the web app
  2. Secondary notebook (Implementing Multiple Classifiers) that contains implementation of other models such as SVM, RF, Bagging, Boosting   etc.

  The Data folder contains the following contents:
  1. train_lyrics_1000 which is the training data
  2. valid_lyrics_200 which is the validation data
  3. stopwords_eng which is a corpus of stopwords used by the model to remove stopwords from the training data

  The Model folder contains the pickled version of all the necessary components of the model used by the webapp

The Model Deployment Phase:
    
  1. In the app.py code we have loaded the pickled model and all the other components, and the app.py will recieve the lyrics in   Hindi(Nagri) format which will then be passed to the Google Translater and converted into English
  2. This converted text will then be passed to the model to predict if the song is sad or happy.
  3. Based on the output that we recieve in step 2, we will create a JSON object and return it.
  4. Once the index.html page is loaded, the user needs to enter the lyrics in the text area component and submit it.
  5. Once submitted, an AJAX call will be made to the API that we developed in Step 1 and will recieve the output as described in step 3
  6. This AJAX will then return the image output based on the condition if the song is happy or sad
