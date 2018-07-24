# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:18:32 2018

@author: sogi
"""
import initialization as init
import pylab as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import statistics as stat
import pandas as pd
from reduce_noise import NoiseReduction

SMALL_DATASET = 30
MEDIUM_DATASET = 300
BIG_DATASET = 500
FULL_DATASET = 1000000

UPPER_LIMIT = 100
DATASET = MEDIUM_DATASET
CATEGORIES = ['num_of_files', 'total_lines', 'mod_lines', 'insertions', 'deletions']

class RecordStatistic(object):
    def __init__(self,_db):
        self.db = _db
        self.total = 0
        self.records = {}
        self.labels = {}
        self.hist = {}
        self.statistic = {}
        self.label_data = {}
        self.read_db()
    
    def read_db(self):
        for record in self.db._collection.find():
            self.records[record['hash']] = record
            self.labels[record['label']] = self.labels.get(record['label'], 0) + 1
        del self.labels[None]
        self.total = self.db._collection.find().count()
        
    def convert_to_log10(self):
        for hash_,record in self.records.items():
            temp = record.copy()
            for category in CATEGORIES:
                if record[category] == 0:
                    temp[category] = 0
                else:
                    temp[category] = np.log10(record[category])
            self.records[hash_] = temp
        return self.records
    
    def histogram_of_type(self, type_, field):
        hist = {}
        for hash_, record in self.records.items():
            if record['label'] == type_:
                if record[field] < UPPER_LIMIT:
                    hist[record[field]] = hist.get(record[field], 0) + 1
        return hist
                
    def normalize_hist(self, hist):
        scalar = MinMaxScaler()
        data = [[d] for d in hist.keys()]
        scalar.fit(data)
        tf_data  = scalar.transform(data)
        itf_data = scalar.inverse_transform(tf_data)
        norm_data = {}
        for c in range(len(itf_data)):
            print(tf_data[c])
            print(itf_data[c])
            norm_data[tf_data[c][0]] = hist[np.around(itf_data[c][0])]
        return norm_data
                    
    def histogram(self, field):
        for type_ in self.labels.keys():
            self.hist[str(type_)] = self.histogram_of_type(type_, field)
            #self.hist[str(type_) + '_norm'] = self.normalize_hist(self.hist[str(type_)])
            
        fig, axes = plt.subplots(2, 2)
        fig.suptitle(field + ' of non-bug and None')
        self.plot_hist(axes[0][0], self.hist['non-bug'], field, 'blue')
        #self.plot_hist(axes[0][1], self.hist['non-bug_norm'], field, 'blue', (0,1))
        self.plot_hist(axes[1][0], self.hist['bug'], field, 'orange')
        #self.plot_hist(axes[1][1], self.hist['None_norm'], field, 'orange', (0,1))
        
    def plot_hist(self, axe, hist, field, c, xlim=None):
        axe.set_ylabel('Frequency')
        axe.bar(list(hist.keys()), list(hist.values()), color=c)
        if xlim != None:
            axe.set_xlim(xlim)
       
    def normalize_list(self, _list):
        scalar = MinMaxScaler()
        tf_list = [[i] for i in _list]
        scalar.fit(tf_list)
        return scalar.transform(tf_list)
        
    def describe(self, _list=[]):
        describe = {}
        data = {'origin': np.array(_list), 'norm': self.normalize_list(_list)}
        describe['min'] = round(min(_list),2)
        describe['max'] = round(max(_list),2)
        describe['ave'] = round(stat.mean(_list),2)
        describe['var'] = round(stat.variance(_list),2)
        describe['std'] = round(stat.stdev(_list),2)
        describe['med'] = round(stat.median(_list),2)
        return describe, data
    
    def statistic_of_type(self, type_):
        categories_stats = { category:[] for category in CATEGORIES }
        categories_data = { category:[] for category in CATEGORIES }
        for hash_, record in self.records.items():
            if record['label'] == type_:
                for category in CATEGORIES:
                    categories_stats[category].append(record[category])
        for category in CATEGORIES:
            categories_stats[category], categories_data[category] = self.describe(categories_stats[category])
        return categories_stats, categories_data
                
    def get_statistic(self):
        self.labels = {}
        for hash_, record in self.records.items():
            self.labels[record['label']] = self.labels.get(record['label'], 0) + 1
        del self.labels[None]
        for type_ in self.labels.keys():
            self.statistic[str(type_)], self.label_data[str(type_)] = self.statistic_of_type(type_)
        return self.statistic, self.label_data
            
    def plot_scatter_of_type(self, type_, xlabel, ylabel):
        x, y = [], []
        counter = 0
        for hash_, record in self.records.items():
            if record['label'] == type_:
                counter += 1
                x.append(record[xlabel])
                y.append(record[ylabel])
                if counter == DATASET:
                    break;
        return x, y
    
    def plot_scatter(self, xlabel, ylabel):
        plt.figure()
        plt.title(str(self.labels))
        for type_ in self.labels.keys():
            x, y = self.plot_scatter_of_type(type_, xlabel, ylabel)
            plt.scatter(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid()
        plt.legend(self.labels.keys())
        
    def plot_scatter_on_axes(self, axes, xlabel, ylabel):
        for type_ in self.labels.keys():
            x, y = self.plot_scatter_of_type(type_, xlabel, ylabel)
            axes.scatter(x, y)
        
    def plot_scatter_3d_of_type(self, ax, type_, xlabel, ylabel, zlabel):
        x, y, z = [], [], []
        counter = 0
        for hash_, record in self.records.items():
            if record['label'] == type_:
                counter += 1
                x.append(record[xlabel])
                y.append(record[ylabel])
                z.append(record[zlabel])
                if counter == DATASET:
                    break;
        return x, y, z
    
    def plot_scatter_3d(self, xlabel, ylabel, zlabel):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for type_ in self.labels.keys():
            x, y, z = self.plot_scatter_3d_of_type(ax, type_, xlabel, ylabel, zlabel)
            ax.scatter(x, y, z)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        plt.grid()
        plt.legend(self.labels.keys())
        
    def get_normalize_database(self):
        database = {hash_: [record[category] for category in CATEGORIES] for hash_, record in self.records.items()}
        scalar = MinMaxScaler()
        scalar.fit(list(database.values()))
        X, y =[], []
        for hash_, record in self.records.items():
            X.append(scalar.transform([database[hash_]])[0])
            if record['label'] == 'non-bug':
                y.append(0)
            elif record['label'] == 'bug':
                y.append(1)
            else:
                y.append(-1)
        return X, y
    
    def plot_aggregation_scatter_graph(self):
        rows, cols = 5, 5
        fig, axes = plt.subplots(rows, cols)
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.text(-4.56,-0.6, 'number_of_files                           total_lines                                 mod_lines                                    insertions                                  deletions')
        plt.text(-5.4,6, 'deletions        insertions        mod_lines         total_lines       number_of_files', rotation=90)
        for i in range(rows):
            for j in range(cols):
                if i!=j:
                    self.plot_scatter_on_axes(axes[j][i], CATEGORIES[i],CATEGORIES[j])
                else:
                    axes[i][j].set_facecolor('black')
    
    def compare_statistic(self):
        for category in CATEGORIES:
            df = pd.DataFrame({label:self.statistic[str(label)][category] for label in self.labels.keys()})
            print('*****************************')
            print(category)
            print(df)
            
    def apply_filter(self):
        noise_filter = NoiseReduction(self.records)
        noise_filter.set_rule({'$lt':{'num_of_files': 25, 'total_lines':5000,'mod_lines':1000},'$ne':{'label':None}, '$gt': {'mod_lines':200}})
        self.records = noise_filter.execute_filter().copy()
            
    def get_origin_database(self):
        X, y =[], []
        for hash_, record in self.records.items():
            if record['label'] != None:
                X.append([record[category] for category in CATEGORIES])
                if record['label'] == 'non-bug':
                    y.append(0)
                if record['label'] == 'bug':
                    y.append(1)
        return X, y
            
    def get_selected_features(self):
        #SELECTED_FEATURES = [CATEGORIES[2], CATEGORIES[3]]
        SELECTED_FEATURES = CATEGORIES
        X, y = [], []
        for hash_, record in self.records.items():
            if record['label'] != None:
                X.append([record[category] for category in SELECTED_FEATURES])
                if record['label'] == 'non-bug':
                    y.append(0)
                if record['label'] == 'bug':
                    y.append(1)
        return np.array(X), np.array(y)
        
if __name__ == '__main__':
    database = init._db
    stats = RecordStatistic(database)
    stats.convert_to_log10()
    #stats.apply_filter()
    #stats.get_normalize_database()
    stats.histogram(CATEGORIES[0])
    #stats.histogram(CATEGORIES[1])
    #stats.histogram(CATEGORIES[2])
    #stats.histogram(CATEGORIES[3])
    #stats.histogram(CATEGORIES[4])
    stats.get_statistic()
    stats.compare_statistic()
    #stats.plot_scatter(CATEGORIES[1], CATEGORIES[4])
    #stats.plot_scatter(CATEGORIES[3], CATEGORIES[2])
    stats.plot_aggregation_scatter_graph()
    #stats.plot_scatter_3d(CATEGORIES[3], CATEGORIES[2], CATEGORIES[1])
    print(stats.labels)
