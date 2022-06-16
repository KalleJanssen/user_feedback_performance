# -*- coding: utf-8 -*-
# Removes links, mentions, and hashtags themselves.
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import sys
import warnings
import pandas as pd
import os
from flair.models import TextClassifier
from flair.data import Sentence
from sklearn.metrics import precision_recall_fscore_support
warnings.filterwarnings("ignore")
filename = "times.txt"

if not os.path.exists(filename):
	file = open(filename, 'w')
	file.write("approach, method, start_time, end_time\n")
else:
	file = open(filename,"a")

try:
    database = mysql.connector.connect(user='root', password='Qw3rty!2',
                              host='127.0.0.1',
                              database='analysweet')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

DBcursor = database.cursor()

df = pd.read_sql("SELECT * FROM sentiment_data", database)

def predict(sentence):
    """ Predict the sentiment of a sentence """
    if sentence == "":
        return 0
    text = Sentence(sentence)
    # stacked_embeddings.embed(text)
    classifier.predict(text)
    value = text.labels[0].to_dict()['value'] 
    if value == 'POSITIVE':
        result = text.to_dict()['all labels'][0]['confidence']
    else:
        result = -(text.to_dict()['all labels'][0]['confidence'])
    return round(result, 3)

def round_sentiment(sentiment):
    if sentiment < (-1/3):
        return -1
    elif sentiment > (1/3):
        return 1
    return 0

start = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")

classifier = TextClassifier.load('en-sentiment')

for i in range(25):
    predicted_list = []
    correct_list = []
    for index, row in df.iterrows():
        predicted_list.append(predict(row[3]))
        correct_list.append(row[1])


end = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
file.write("sentiment, flair, " + start[:-3] + ", " + end[:-3] + "\n")

correct = 0
incorrect = 0
MAE = 0
round_predicted = [round_sentiment(i) for i in predicted_list]
round_correct = [round_sentiment(i) for i in correct_list]
for i in range(len(predicted_list)):
    if round_predicted[i] == round_correct[i]:
        correct += 1
    else:
        incorrect += 1
    MAE += abs(predicted_list[i] - correct_list[i])

(precision, recall, F1, ignore) = precision_recall_fscore_support(round_correct, round_predicted, average='macro')

# write accuracy to file
filename = "accuracy.txt"
if not os.path.exists(filename):
    file = open(filename, 'w')
    file.write("approach, method, accuracy, precision, recall, F1, MAE\n")
    file.write("sentiment, flair, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")
else:
    file = open(filename,"a")
    file.write("sentiment, flair, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")
# close the database connection
DBcursor.close()
database.close()