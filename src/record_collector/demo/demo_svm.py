# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:45:49 2018

@author: sogi
"""

from sklearn.datasets import load_digits
from sklearn import svm

digits = load_digits()
X = digits.data
y = digits.target

classifier = svm.SVC()
classifier.fit(X[:1000], y[:1000])
predictions = classifier.predict(X[1000:])