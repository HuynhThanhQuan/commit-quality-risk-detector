# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 13:57:55 2018

@author: sogi
"""

import initialization as init
import pandas as pd
import string
import collections as cl

db = init._db
repo = init._db

SUB_FOLDER = 'Snapshot\\'
SUFFIX = '_Records_20180723'
EXTENSION = '.csv'
JSON = '_JSON'

def clean_message(message):
    rm_sls = ''
    for i in message:
        if i in string.ascii_letters or i in string.digits or i in ' -_':
            rm_sls += i
    rm_sls = rm_sls.strip()
    mes_pos = rm_sls.find('message')
    files_pos = rm_sls.find('num_of_files')
    mes_cxt = rm_sls[mes_pos:files_pos]
    rm_sls = rm_sls.replace(mes_cxt, '')
    #print(rm_sls)
    return rm_sls

# Clean the file format
def read_and_export_csv():
    file = open(init.DATA_DIR + SUB_FOLDER + OWNER + SUFFIX + EXTENSION, errors='ignore')
    lines = file.readlines()
    dicts = {}
    for idx, line in enumerate(lines):
        cleaned_ms = clean_message(line)
        elements = cleaned_ms.split(' ')
        for idx,e in enumerate(elements):
            if e == 'label':
                break
        dicts[elements[3].strip()] = elements[idx+1].strip()
    file.close()
    
    # Export to csv format
    fout = open(init.DATA_DIR + SUB_FOLDER + OWNER + SUFFIX + JSON + EXTENSION, 'w')
    fout.write('hash' + ',' + 'label' + '\n')
    for k, v in dicts.items():
        fout.write(k + ',' + v + '\n')
    fout.close()
    
def check_aggregation():
    df = pd.read_csv(init.DATA_DIR + SUB_FOLDER + OWNER + SUFFIX + JSON + EXTENSION)
    print('Count element frequency of label of {}'.format(OWNER))
    print(cl.Counter(df['label']))
    return df

def update_dabase():
    db = init._db
    df = pd.read_csv(init.DATA_DIR + SUB_FOLDER + OWNER + SUFFIX + JSON + EXTENSION)
    for idx, row in df.iterrows():
        #print(idx, row['hash'], row['label'])
        label = row['label']
        if label == 'bug':
            db._collection.update_many({'hash':row['hash']}, {"$set": {'label':label}}, upsert=False)
    
if __name__ == '__main__':
    print('*********************************************')
    print('REMOVE WHEN YOU ARE READY TO UPDATE DATABASE')
    print('Warning: Database will be changed')
    print('*********************************************')
    print()
    OWNER = 'Quan'
    read_and_export_csv()
    check_aggregation()
    update_dabase()
