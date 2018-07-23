# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 13:25:30 2018

@author: sogi
"""

import initialization as init
from sklearn import svm
import record_statistic as stats
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
import pickle

stat = stats.RecordStatistic(init._db)
stat.convert_to_log10()
X, y = stat.get_selected_features()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

clf = svm.SVC()
clf.fit(X_train, y_train)  

y_pred = clf.predict(X_test)

precision, recall, fbeta_score, support = precision_recall_fscore_support(y_test, y_pred, average='macro')
print('precision=',precision)
print('recall=',recall)
print('fbeta_score=',fbeta_score)

pickle.dump(clf, open('svm_model.sav', 'wb'))

loaded_model = pickle.load(open('svm_model.sav', 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)
