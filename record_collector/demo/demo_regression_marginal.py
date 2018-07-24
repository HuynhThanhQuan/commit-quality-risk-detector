# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 10:19:29 2018

@author: sogi
"""

import seaborn as sns
import pandas as pd

sns.set(style="darkgrid")

PATH = 'C:\\Users\\sogi\\seaborn-data\\'

RECORDS = 'C:\\Users\\sogi\\workspace\\quality_risk_manager\\src\\record_collector\\data\\DF_Records_20180723112057.csv'

'''
tips = pd.read_csv(PATH + 'tips.csv')
g = sns.jointplot("total_bill", "tip", data=tips, kind="reg",
                  xlim=(0, 60), ylim=(0, 12), color="m")
'''

sns.set(style="ticks")

df = pd.read_csv(RECORDS)
#df = pd.read_csv(RECORDS)
#sns.pairplot(df, hue="label")
ax = sns.jointplot("num_of_files", "insertions", data=df, kind="kde", space=0, color="g")
