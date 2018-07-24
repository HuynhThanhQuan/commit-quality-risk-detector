# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:10:43 2018

@author: sogi
"""

from sklearn.model_selection import train_test_split
import initialization as init

db = init._db

X = [ record for record in db._collection.find()]
y = [ record['label'] for record in X]

X_train,  X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)