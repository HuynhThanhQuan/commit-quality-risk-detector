# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 15:46:01 2018

@author: sogi
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

RECORDS = 'C:\\Users\\sogi\\workspace\\quality_risk_manager\\src\\record_collector\\data\\DF_Records_20180723112057.csv'
CATEGORIES = ['num_of_files', 'total_lines', 'mod_lines', 'insertions', 'deletions']


class DataVisualization(object):
    def __init__(self, path):
        self.df = pd.read_csv(path, dtype={'num_of_files': np.float64, 'total_lines': np.float64, 'mod_lines': np.float64, 'insertions': np.float64, 'deletions': np.float64})

    def box_plot(self, category):
        sns.set(style="ticks")
        
        # Initialize the figure with a logarithmic x axis
        f, ax = plt.subplots(figsize=(7, 6))
        ax.set_xscale("log")
        
        planets = pd.read_csv(RECORDS)
        
        # Plot the orbital period with horizontal boxes
        sns.boxplot(x=category, y="label", data=planets,
                    whis="range", palette="vlag")
        
        # Add in points to show each observation
        #sns.swarmplot(x=category, y="label", data=planets,
        #              size=2, color=".3", linewidth=0)
        
        # Tweak the visual presentation
        ax.xaxis.grid(True)
        ax.set(ylabel="")
        sns.despine(trim=True, left=True)
        
    def convert_to_log10(self):
        for index, row in self.df.iterrows():
            for category in CATEGORIES:
                if row[category] != 0:
                    self.df.at[index, category] = np.log10(row[category])
                else:
                    self.df.at[index, category] = 0.0
        
    def joint_plot(self, x, y):
        self.convert_to_log10()
        sns.jointplot(x, y, data=self.df, kind="kde", space=0, color="g")
    
if __name__ == '__main__':
    dv = DataVisualization(RECORDS)
    #dv.box_plot(CATEGORIES[0])
    dv.joint_plot(CATEGORIES[0], CATEGORIES[1])