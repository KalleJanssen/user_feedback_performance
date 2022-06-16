# -*- coding: utf-8 -*-
# This application use Twitter Search API to query tweets that contain a particular app name and store the retrieved
# tweets in DB
import nltk
import sys
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import re
from nltk.stem import PorterStemmer 
ps = PorterStemmer()
import numpy as np 

# connect to the database
# Add your DB connection information
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

REMOVE_URL = re.compile(
    "([^0-9A-Za-z# \t" +
    "[!\"#$%&'()*+,\-./:;<=>?@[\]^_`{|}~]\"" + # UNTESTED PLS TEST 
    "\U0001F300-\U0001F5FF" + # symbols & pictographs
    "\U0001F600-\U0001F64F" + # emoticons
    "\U0001F900-\U0001F9FF" +  # Supplemental Symbols and Pictographs
    "])|(\w+:\/\/\S+)" + 
    "|(@[A-Za-z0-9_]+)" + # removes mentions
    # remove more emojis
    "|["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251" 
    "]+")

#Removes url from a tweet
def remove_url(txt):
    return " ".join(re.sub(REMOVE_URL, "", txt).split())

#Splits multi word hashtags into seperate words
def split_hashtag(hashtag):
    if hashtag.isupper() or hashtag.islower():
        return hashtag
    return ' '.join(word for word in re.findall('[A-Z][^A-Z]*', hashtag))

#Splits a tweet up in sentences
def preprocess(tweet):
    final = ''
    tweet = tweet.replace('!', ' ')
    tweet = tweet.replace('.', ' ')
    tweet = tweet.replace(',', ' ')
    tweet = tweet.replace('-', ' ')
    tweet = tweet.replace('_', ' ')
    tweet = tweet.replace('?', ' ')
    tweet = tweet.replace('/', ' ')
    tweet = tweet.replace('"', ' ')
    tweet = tweet.replace('@', ' ')
    for sentence in nltk.sent_tokenize(tweet):
        new_tweet = remove_url(sentence)
        new_tweet = new_tweet.split()
        final_tweet = []
        for i in new_tweet:
            if i[0] == "#":
                final_tweet.append(split_hashtag(i[1:]))
            else:
                final_tweet.append(i)
        # if the tweet consists of 2 or less words, it is removed
        if len(final_tweet) > 2:
            final += ' '.join(word.lower() for word in final_tweet)
    return final

# https://github.com/stopwords-iso/stopwords-en
my_file = open("labeled_data/stopwords-en.txt", "r")
data = my_file.read()
stop_words = data.split("\n")

DBcursor = database.cursor()

# reads oliviera data and transforms sentiments score from [-2, 2] to [-1, 1]
df_Oliviera = pd.read_csv('labeled_data/Oliveira_data.csv')
df_Oliviera['sentimentScore'] = df_Oliviera['sentimentScore']/2

DBcursor.execute("DROP TABLE IF EXISTS sentiment_data")
DBcursor.execute("CREATE TABLE sentiment_data (app VARCHAR(50), sentiment REAL, original_text TEXT, preprocessed_text TEXT, no_stop_words TEXT, stem_words TEXT, no_stop_stem_words TEXT)")

# store imported tweets into the database
for index, row in df_Oliviera.iterrows():
    try:
        preprocessed_text = preprocess(row[9])

        # stem and remove stop words from text
        no_stop_words = [word for word in nltk.word_tokenize(preprocessed_text) if word not in stop_words]
        stem_words = [ps.stem(word) for word in nltk.word_tokenize(preprocessed_text)]
        no_stop_stem_words = [ps.stem(word) for word in nltk.word_tokenize(preprocessed_text) if word not in stop_words]
        # removes tweets with short length
        if preprocessed_text:
            # save tweet in new table in DB
            add_tweet = ("INSERT INTO sentiment_data(app, sentiment, original_text, preprocessed_text, no_stop_words, stem_words, no_stop_stem_words)"
                                "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            tweet_data = (row[1], row[15], row[9], preprocessed_text, ' '.join(word for word in no_stop_words), ' '.join(word for word in stem_words), ' '.join(word for word in no_stop_stem_words))
            DBcursor.execute('SET NAMES utf8mb4')
            DBcursor.execute("SET CHARACTER SET utf8mb4")
            DBcursor.execute("SET character_set_connection=utf8mb4")
            DBcursor.execute(add_tweet, tweet_data)
            database.commit()
    except mysql.connector.DatabaseError as err:
        print(err)
        break

# close the database connection
DBcursor.close()
database.close()