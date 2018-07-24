# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 16:24:12 2018

@author: sogi
"""

from keras.models import Sequential
from keras.layers import Dense
import record_statistic as stats
import initialization as init
from sklearn.metrics import precision_recall_fscore_support


stat = stats.RecordStatistic(init._db)
stat.convert_to_log10()
X, Y = stat.get_selected_features()
# fix random seed for reproducibility

# load pima indians dataset
#dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# split into input (X) and output (Y) variables
#X = dataset[:,0:8]
#Y = dataset[:,8]

# create model
model = Sequential()
model.add(Dense(12, input_dim=5, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, Y, epochs=50, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
Y_pred = model.predict_classes(X)

precision, recall, fbeta_score, support = precision_recall_fscore_support(Y, Y_pred, average='macro')
print('precision=',precision)
print('recall=',recall)
print('fbeta_score=',fbeta_score)