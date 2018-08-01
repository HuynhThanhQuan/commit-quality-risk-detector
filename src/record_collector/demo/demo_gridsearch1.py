# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 10:42:39 2018

@author: sogi
"""

# Use scikit-learn to grid search the batch size and epochs
import numpy as np
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import pandas as pd

# Function to create model, required for KerasClassifier
def create_model():
	# create model
	model = Sequential()
	model.add(Dense(12, input_dim=8, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)
# load dataset
dataset = np.loadtxt("pima-indians-diabetes_reduced.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
print('Loaded model',len(Y))



# create model
model = KerasClassifier(build_fn=create_model, verbose=0)
# define the grid search parameters
batch_size = [10, 20]
epochs = [20, 50]
param_grid = dict(batch_size=batch_size, epochs=epochs)
scoring = {'accuracy': make_scorer(accuracy_score), 
           'precision': make_scorer(precision_score),
           'recall': make_scorer(recall_score),
           'f1': make_scorer(f1_score) }

grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=1, scoring=scoring,refit='f1')
#print('Grid model', grid)
grid_result = grid.fit(X, Y)
#print('Fit model', grid_result)
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
df = pd.DataFrame.from_dict(grid_result.cv_results_)
y_pred = y_pred = grid_result.best_estimator_.predict(X)
print(confusion_matrix(Y, y_pred))

with open('demo_excel.csv', 'w') as f:
    f.write("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_) +'\n')
    f.write(np.array2string(confusion_matrix(Y, y_pred), separator=', ')+'\n')
    f.write(df.to_string())