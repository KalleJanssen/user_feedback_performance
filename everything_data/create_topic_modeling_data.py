import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import pickle

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

df_instagram = pd.read_sql("SELECT no_stop_words FROM sentiment_data WHERE app = 'Instagra'", database)
df_facebook = pd.read_sql("SELECT no_stop_words FROM sentiment_data WHERE app = 'Facebook'", database)
df_whatsapp = pd.read_sql("SELECT no_stop_words FROM sentiment_data WHERE app = 'Whatsapp'", database)
df_all = pd.read_sql("SELECT no_stop_words FROM sentiment_data", database)
df_all_orig = pd.read_sql("SELECT original_text FROM sentiment_data", database)

df_instagram1 = pd.read_sql("SELECT no_stop_words FROM classification_data WHERE app = 'Instagra'", database)
df_facebook1 = pd.read_sql("SELECT no_stop_words FROM classification_data WHERE app = 'Facebook'", database)
df_whatsapp1 = pd.read_sql("SELECT no_stop_words FROM classification_data WHERE app = 'Whatsapp'", database)
df_all1 = pd.read_sql("SELECT no_stop_words FROM classification_data", database)
df_all1_orig = pd.read_sql("SELECT original_text FROM classification_data", database)

df_instagram = df_instagram.append(df_instagram1)
df_facebook = df_facebook.append(df_facebook1)
df_whatsapp = df_whatsapp.append(df_whatsapp1)
df_all = df_all.append(df_all1)
df_all_orig = df_all_orig.append(df_all1_orig)

for n_dataframe, app_df in enumerate([df_instagram, df_facebook, df_whatsapp, df_all]):
    frequency_dict = {}
    for index, row in app_df.iterrows():
        row[0] = row[0].replace("facebook", ' ')
        row[0] = row[0].replace("instagram", ' ')
        row[0] = row[0].replace("whatsapp", ' ')
        row[0] = row[0].replace("dropbox", ' ')
        row[0] = row[0].replace("dropboxsupport", ' ')
        row[0] = row[0].replace("spotify", ' ')
        row[0] = row[0].replace("spotifycares", ' ')
        row[0] = row[0].replace("slack", ' ')
        row[0] = row[0].replace("slackhq", ' ')
        row[0] = row[0].replace("waze", ' ')
        row[0] = row[0].replace("pinterest", ' ')
        row[0] = row[0].replace("fitbit", ' ')
        row[0] = row[0].replace("app", ' ')
        text_list = [i for i in row[0].split(" ") if len(i) > 3]
        for word in text_list:
            if word in frequency_dict:
                frequency_dict[word] += 1
            else:
                frequency_dict[word] = 1

    filename = "../topic_modeling/STTM-master.nosync/dataset/pre_topic_modeling_" + ["instagram", "facebook", "whatsapp", "all"][n_dataframe] + ".txt"
    file = open(filename,"w")
    orig_list = []
    for index, row in app_df.iterrows():
        row[0] = row[0].replace("facebook", ' ')
        row[0] = row[0].replace("instagram", ' ')
        row[0] = row[0].replace("whatsapp", ' ')
        row[0] = row[0].replace("dropbox", ' ')
        row[0] = row[0].replace("dropboxsupport", ' ')
        row[0] = row[0].replace("spotify", ' ')
        row[0] = row[0].replace("spotifycares", ' ')
        row[0] = row[0].replace("slack", ' ')
        row[0] = row[0].replace("slackhq", ' ')
        row[0] = row[0].replace("waze", ' ')
        row[0] = row[0].replace("pinterest", ' ')
        row[0] = row[0].replace("fitbit", ' ')
        row[0] = row[0].replace("app", ' ')
        text = " ".join([word for word in row[0].split(" ") if len(word) > 3 and frequency_dict[word] > 20])
        if len(text.split(" ")) > 5:
            file.write(text + " \n")
            orig_list.append('"' + str(df_all_orig.loc[[index]]['original_text'].values[0]) + '"')
    
    # For some reason the only thing that works is saving the text as a pickle
    with open(filename[:-4], "wb") as fp:
        pickle.dump(orig_list, fp)
# close the database connection
DBcursor.close()
database.close()