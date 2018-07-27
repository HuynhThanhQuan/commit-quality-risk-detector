# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:21:41 2018

@author: sogi
"""

from pymongo import MongoClient
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from keras.models import load_model

class CommitDB(object):    
    def __init__(self, host, ip, db_name, collection_name):
        self._client = MongoClient(host, ip)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

db = CommitDB('10.130.110.31', 27017, 'CommitInfo', 'RxJavaRecord2X')

records=dict()
for record in db._collection.find():
    records[record['hash']] = record
    
CATEGORIES = ['num_of_files', 'total_lines', 'mod_lines', 'insertions', 'deletions']
def get_input_and_target_data():
    X, y = [], []
    for hash_, record in records.items():
        if record['label'] != None:
            info = []
            for category in CATEGORIES:
                if record[category] == 0:
                    info.append(0)
                else:
                    info.append(np.log10(record[category]))
            X.append(info)
            if record['label'] == 'non-bug':
                y.append(0)
            if record['label'] == 'bug':
                y.append(1)
    return np.array(X), np.array(y)

X, y = get_input_and_target_data()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)


loaded_model = load_model('neural_network_model.sav')

y_pred = loaded_model.predict_classes(X)
accuracy = loaded_model.evaluate(X, y)

precision, recall, fbeta_score, support = precision_recall_fscore_support(y, y_pred, average='macro')
print('precision=',precision)
print('recall=',recall)
print('fbeta_score=',fbeta_score)
print('accuracy=', accuracy[1]*100)