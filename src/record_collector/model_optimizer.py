from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
import initialization as init
import record_statistic as stats
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np


stat = stats.RecordStatistic(init._db)
stat.convert_to_log10()
X, y = stat.get_selected_features()

def create_model(optimizer='adam'):
    model = Sequential()
    model.add(Dense(12, input_dim=5, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

# Test differenct configuration
# epoch, batch_size
batch_size = [5, 10, 15, 20]
epochs = [100, 500, 1000, 1500]
# optimizer
# optimizer = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
# learning_rate

# scores
scoring = {'accuracy': make_scorer(accuracy_score), 
           'precision': make_scorer(precision_score),
           'recall': make_scorer(recall_score),
           'f1': make_scorer(f1_score) }

# Model wrapper
TRIAL_MODEL = 'TRIAL_MODELS'
LOG_FILE = init.format_file_name(init.LOG_DIR + TRIAL_MODEL, 'log')
with open(LOG_FILE,'w') as f:
    param_grid = dict(batch_size=batch_size, epochs=epochs)
    model = KerasClassifier(build_fn=create_model, verbose=1)
    try:
        grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=1, scoring=scoring, refit='f1')
        grid_result = grid.fit(X, y)
        
        df = pd.DataFrame.from_dict(grid_result.cv_results_)
        y_pred = grid_result.best_estimator_.predict(X)
        
        f.write("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_) +'\n')
        f.write(np.array2string(confusion_matrix(y, y_pred), separator=', ')+'\n')
        f.write(df.to_string()+'\n')
    except Exception as error:
        f.write(error.__str__())