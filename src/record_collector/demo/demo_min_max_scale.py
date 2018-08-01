# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:08:20 2018

@author: sogi
"""

from sklearn.preprocessing import MinMaxScaler

data = [[1, 2, 0],[2, 3, 8],[3, 4, 10]]
scaler = MinMaxScaler()
print(scaler.fit(data))
print(data)
#print(scaler.data_min_)
#print(scaler.data_range_)
#print(scaler.data_max_)
#print(scaler.feature_range)

print(scaler.transform([data[1]]))



#print(scaler.transform([[1]]))
