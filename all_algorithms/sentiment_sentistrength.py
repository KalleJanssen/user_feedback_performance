# -*- coding: utf-8 -*-
# Removes links, mentions, and hashtags themselves.
import mysql.connector
from mysql.connector import errorcode
from sentistrength import PySentiStr
from datetime import datetime
import sys
import warnings
import pandas as pd
import os
warnings.filterwarnings("ignore")
filename = "times.txt"
from sklearn.metrics import precision_recall_fscore_support

if not os.path.exists(filename):
	file = open(filename, 'w')
	file.write("approach, method, start_time, end_time\n")
else:
	file = open(filename,"a")

senti = PySentiStr()
senti.setSentiStrengthPath('sentistrength/SentiStrength.jar')
senti.setSentiStrengthLanguageFolderPath('sentistrength/SentiStrength_Data')

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
for i in range(25):
    senti_list = senti.getSentiment(list(df['preprocessed_text']), score='scale')
    predicted_list = []
    correct_list = []
    for index, row in df.iterrows():
        predicted_list.append(senti_list[index]/4)
        correct_list.append(row[1])


end = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
file.write("sentiment, sentistrength, " + start[:-3] + ", " + end[:-3] + "\n")


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
    file.write("sentiment, sentistrength, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")
else:
    file = open(filename,"a")
    file.write("sentiment, sentistrength, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")

# close the database connection
DBcursor.close()
database.close()