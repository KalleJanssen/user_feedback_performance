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

df.to_csv('ClassificationTask/data/inputCorpus.csv', columns = ["preprocessed_text"], header=None, index=None)

# for i in range(10):
#     df.to_csv('ClassificationTask/data/inputCorpus.csv', mode='a', columns = ["preprocessed_text"], header=None, index=None)

start = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")

for i in range(25):
    os.system("sh ClassificationTask/classificationTask.sh ClassificationTask/data/inputCorpus.csv data/outputPredictions.csv")

end = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
file.write("sentiment, senti4SD, " + start[:-3] + ", " + end[:-3] + "\n")

predictions = pd.read_csv("ClassificationTask/data/outputPredictions.csv")
predicted_list_labels = list(predictions["Predicted"])
label_to_value = {'negative': -1, 'neutral': 0, 'positive': 1}
predicted_list = [label_to_value[i] for i in predicted_list_labels]
correct_list = [round_sentiment(i) for i in list(df["sentiment"])]

correct = 0
incorrect = 0
MAE = 0
for i in range(len(predicted_list)):
    if predicted_list[i] == correct_list[i]:
        correct += 1
    else:
        incorrect += 1
    MAE += abs(predicted_list[i] - list(df["sentiment"])[i])

(precision, recall, F1, ignore) = precision_recall_fscore_support(correct_list, predicted_list, average='macro')

# write accuracy to file
filename = "accuracy.txt"
if not os.path.exists(filename):
    file = open(filename, 'w')
    file.write("approach, method, accuracy, precision, recall, F1, MAE\n")
    file.write("sentiment, senti4SD, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")
else:
    file = open(filename,"a")
    file.write("sentiment, senti4SD, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")

# close the database connection
DBcursor.close()
database.close()