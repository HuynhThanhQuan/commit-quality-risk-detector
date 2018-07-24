# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 16:24:12 2018

@author: sogi
"""

from keras.models import Sequential
from keras.layers import Dense
from keras import metrics
from sklearn.metrics import precision_recall_fscore_support
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)

# load pima indians dataset
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]

# create model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', metrics.categorical_accuracy])

# Fit the model
model.fit(X, Y, epochs=50, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
Y_pred = model.predict_classes(X)

print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

precision, recall, fbeta_score, support = precision_recall_fscore_support(Y, Y_pred, average='macro')
print('precision=',precision)
print('recall=',recall)
print('fbeta_score=',fbeta_score)