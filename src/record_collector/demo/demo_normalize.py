# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:02:46 2018

@author: sogi
"""

import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import normalize

x = np.random.rand(10)*10
norm1 = x / np.linalg.norm(x)
norm2 = normalize(x[:,np.newaxis], axis=0).ravel()
print(np.all(norm1 == norm2))

from sklearn.preprocessing import MinMaxScaler
scalar = MinMaxScaler()
X = [[i] for i in x]
print('X=', X)
scalar.fit(X)
trans = scalar.transform(X)
print(trans)
'''
print(x)
X_scaled = preprocessing.scale(x)
print(X_scaled)
print(X_scaled.mean(axis=0))
print(X_scaled.std(axis=0))
'''