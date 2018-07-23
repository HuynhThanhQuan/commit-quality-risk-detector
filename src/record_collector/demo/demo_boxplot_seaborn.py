# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 11:26:28 2018

@author: sogi
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

PATH = 'C:\\Users\\sogi\\seaborn-data\\'
RECORDS = 'C:\\Users\\sogi\\workspace\\quality_risk_manager\\src\\record_collector\\data\\DF_Records_20180723112057.csv'

sns.set(style="ticks")

# Initialize the figure with a logarithmic x axis
f, ax = plt.subplots(figsize=(7, 6))
ax.set_xscale("log")

# Load the example planets dataset
planets = pd.read_csv(RECORDS)
#planets = sns.load_dataset("planets")

# Plot the orbital period with horizontal boxes
category = "num_of_files"
sns.boxplot(x=category, y="label", data=planets,
            whis="range", palette="vlag")

# Add in points to show each observation
#sns.swarmplot(x=category, y="label", data=planets,
#              size=2, color=".3", linewidth=0)

# Tweak the visual presentation
ax.xaxis.grid(True)
ax.set(ylabel="")
sns.despine(trim=True, left=True)