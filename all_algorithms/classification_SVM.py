# -*- coding: utf-8 -*-
# Removes links, mentions, and hashtags themselves.
import mysql.connector
from mysql.connector import errorcode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from datetime import datetime
import sys
import warnings
import os
import pandas as pd
import time
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

def create_training(sql):
    df = pd.read_sql(sql, database)
    X_train = df['preprocessed_text']
    y_train = df['category']
    return df, X_train, y_train

df, corpus, Y = create_training("SELECT * FROM classification_data")

start = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")

for i in range(1):
    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
    X = vectorizer.fit_transform(corpus)
    vectorizer.get_feature_names_out()

    X = X.todense()

    clf = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    clf.fit(X[:int(0.7*len(corpus))], Y[:int(0.7*len(corpus))])

    predictions = clf.predict(X[int(0.7*len(Y)):])
end = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
file.write("classification, SVM, " + start[:-3] + ", " + end[:-3] + "\n")
file.close()

predicted_list = [0 if i < 0.5 else 1 for i in predictions]
correct_list = list(Y[int(0.7*len(Y)):])

correct = 0
incorrect = 0
for i in range(len(predicted_list)):
    if predicted_list[i] == correct_list[i]:
        correct += 1
    else:
        incorrect += 1

(precision, recall, F1, ignore) = precision_recall_fscore_support(correct_list, predicted_list, average='macro')

# write accuracy to file
filename = "accuracy.txt"
if not os.path.exists(filename):
    file = open(filename, 'w')
    file.write("approach, method, accuracy, precision, recall, F1\n")
    file.write("classification, SVM, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + "\n")
else:
    file = open(filename,"a")
    file.write("classification, SVM, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + "\n")

# close the database connection
DBcursor.close()
database.close()