# PASTE THIS INTO alginer.py FROM SIMBA AT THE BOTTOM OF THE PAGE

from sklearn.metrics import precision_recall_fscore_support
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import warnings
import pandas as pd
import os
warnings.filterwarnings("ignore")
filename = "./times.txt"

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

df = pd.read_sql("SELECT * FROM combined_similarity_english", database)
# df = pd.read_sql("SELECT * FROM ss_all_final_en_reconciled", database)

start = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
import time
for i in xrange(1):
    print(i)
    accuracy = 0.0
    predicted_list = []
    correct_list = []
    for index, row in df.iterrows():
        predicted_list.append(getAlignScore(row[1][:400], row[4][:400]))
        correct_list.append(row[6])


end = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
file.write("similarity, simba, " + start[:-3] + ", " + end[:-3] + "\n")

correct = 0
incorrect = 0
MAE = 0
print("Correct: {}".format(correct_list))
print("predicted SIMBA: {}".format(predicted_list))
for i in xrange(len(predicted_list)):
    if predicted_list[i] == correct_list[i]:
        correct += 1
    else:
        incorrect += 1
    MAE += abs(predicted_list[i] - correct_list[i])

(precision, recall, F1, ignore) = precision_recall_fscore_support(correct_list, predicted_list, average='macro')

# write accuracy to file
filename = "accuracy.txt"
if not os.path.exists(filename):
    file = open(filename, 'w')
    file.write("approach, method, accuracy, precision, recall, F1, MAE\n")
    file.write("similarity, simba, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")
else:
    file = open(filename,"a")
    file.write("similarity, simba, " + str(correct/(correct+incorrect)) + ", " + str(precision) + ", " + str(recall) + ", " + str(F1) + ", " + str(MAE/len(predicted_list)) + "\n")

file.close()
# close the database connection
DBcursor.close()
database.close()