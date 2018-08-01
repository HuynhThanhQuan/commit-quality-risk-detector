# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:21:15 2018

@author: sogi
"""
import initialization as init
from keras.models import load_model
import record_statistic as stats
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
import os

stat = stats.RecordStatistic(init._db)
stat.convert_to_log10()
X, y = stat.get_selected_features()


TYPE = 'neural_network_model_'
DATE = '20180731095919'
EXT = '.h5'
ABSOLUTE_PATH = os.getcwd() + '\\model\\' + TYPE + DATE + EXT
#ABSOLUTE_PATH = 'test_model.h5'

MODEL_PATH = ABSOLUTE_PATH

loaded_model = load_model(MODEL_PATH)

y_pred = loaded_model.predict_classes(X)
accuracy = loaded_model.evaluate(X, y)

precision, recall, fbeta_score, support = precision_recall_fscore_support(y, y_pred, average='binary')
print('precision=',precision)
print('recall=',recall)
print('fbeta_score=',fbeta_score)
print('accuracy=', accuracy[1])
print(confusion_matrix(y, y_pred))