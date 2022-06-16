# -*- coding: utf-8 -*-
# This code finds duplicate tweets
import nltk
import sys
import mysql.connector
from mysql.connector import errorcode
from nltk.metrics import *
from datetime import datetime
import sys
import warnings
import pandas as pd
import os
from scipy import spatial
from sentence_transformers import SentenceTransformer
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

def round_similarity(similarity):
    if similarity <= 0.5:
        return 0
    elif similarity > 0.5:
        return 1

df = pd.read_sql("SELECT * FROM combined_similarity_english", database)

start = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")

sentences = list(df['preprocessed_text1'])
length = len(sentences)
sentences.extend(list(df['preprocessed_text2']))

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
embeddings = model.encode(sentences)

for i in range(35):
    predicted_list = []
    correct_list = []
    for index, row in df.iterrows():
        predicted_list.append(1 - spatial.distance.cosine(embeddings[index], embeddings[index+length]))
        correct_list.append(row[6]/4)

end = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
file.write("similarity, MPNet, " + start[:-3] + ", " + end[:-3] + "\n")

correct = 0
incorrect = 0
MAE = 0
round_predicted = [round_similarity(i) for i in predicted_list]
round_correct = [round_similarity(i) for i in correct_list]
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
    file.write("similarity, MPNet, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")
else:
    file = open(filename,"a")
    file.write("similarity, MPNet, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")

# close the database connection
DBcursor.close()
database.close()