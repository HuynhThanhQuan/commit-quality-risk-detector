# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:21:15 2018

@author: sogi
"""
import initialization as init
from keras.models import load_model
import record_statistic as stats
from sklearn.metrics import precision_recall_fscore_support

stat = stats.RecordStatistic(init._db)
stat.convert_to_log10()
X, y = stat.get_selected_features()


MODEL_PATH = 'neural_network_model.sav'

loaded_model = load_model(MODEL_PATH)

y_pred = loaded_model.predict_classes(X)
accuracy = loaded_model.evaluate(X, y)

precision, recall, fbeta_score, support = precision_recall_fscore_support(y, y_pred, average='macro')
print('precision=',precision)
print('recall=',recall)
print('fbeta_score=',fbeta_score)
print('accuracy=', accuracy[1]*100)