# -*- coding: utf-8 -*-
# Removes links, mentions, and hashtags themselves.
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import sys
import warnings
import pandas as pd
import os
warnings.filterwarnings("ignore")
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
filename = "times.txt"
from sklearn.metrics import precision_recall_fscore_support

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

def round_sentiment(sentiment):
    if sentiment < (-1/3):
        return -1
    elif sentiment > (1/3):
        return 1
    return 0

start = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")

# https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

for i in range(25):

    predicted_list = []
    correct_list = []
    for index, row in df.iterrows():
        text = row[3]
        encoded_input = tokenizer(text, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        score = scores[0] * -1 + scores[2] * 1
        correct_list.append(row[1])
        predicted_list.append(score)


end = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
file.write("sentiment, RoBERTa, " + start[:-3] + ", " + end[:-3] + "\n")

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
    file.write("sentiment, RoBERTa, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")
else:
    file = open(filename,"a")
    file.write("sentiment, RoBERTa, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")

# close the database connection
DBcursor.close()
database.close()