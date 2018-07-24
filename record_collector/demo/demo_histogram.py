# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 11:17:56 2018

@author: sogi
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

scalar = MinMaxScaler()

X = np.random.randn(1000)

hist = np.histogram(X, bins=1)

nb = stats.hist['None']

nb_list = [ record['num_of_files'] for hash_, record in stats.records.items()]
print(nb_list)

X = [[x] for x in nb.keys()]

scalar.fit(X)
X_norm = scalar.transform(X)
print(list(nb.keys()))
print(X_norm)
#plt.hist(X_norm[:20])
plt.bar(list(stats.hist['non-bug_norm'].keys())[:10], list(stats.hist['non-bug_norm'].values())[:10])
plt.xlim(0,1)
#plt.bar(nb.keys(),nb.values())
#plt.hist(np.array(nb_list[:100]))