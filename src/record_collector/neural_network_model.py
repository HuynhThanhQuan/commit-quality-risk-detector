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
from sklearn.model_selection import train_test_split
from keras.models import load_model

stat = stats.RecordStatistic(init._db)
stat.convert_to_log10()
X, y = stat.get_selected_features()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# create model
model = Sequential()
model.add(Dense(12, input_dim=5, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X_train, y_train, epochs=100, batch_size=10)

# evaluate the model
scores = model.evaluate(X_test, y_test)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
y_pred = model.predict_classes(X_test)

precision, recall, fbeta_score, support = precision_recall_fscore_support(y_test, y_pred, average='binary')
print('precision=',precision)
print('recall=',recall)
print('fbeta_score=',fbeta_score)

OFFICIAL_MODEL = init.MODEL_DIR + init.format_file_name('neural_network_model', 'h5')
TEST_MODEL = 'test_model.h5'

MODEL_PATH = OFFICIAL_MODEL

model.save(MODEL_PATH)

#loaded_model = load_model(MODEL_PATH)
