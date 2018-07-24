# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 10:46:42 2018

@author: sogi
"""

import initialization as init
import json
import string

ALLOWED_PUNCTUATION = '!#$%&()*+-./;<=>?@[\]^_`{|}~'
VALID_CHARACTER = string.ascii_letters + string.digits + string.whitespace + ALLOWED_PUNCTUATION

JSON_FILE_PATH = init.format_file_name('JSON_Records','csv')
DF_FILE_PATH = init.format_file_name('DF_Records','csv')

def clean_message(message):
    rm_sls = ''
    for i in message:
        if i in VALID_CHARACTER:
            rm_sls += i
    rm_sls = rm_sls.strip()
    mes_pos = rm_sls.find('message')
    files_pos = rm_sls.find('num_of_files')
    mes_cxt = rm_sls[mes_pos:files_pos]
    rm_sls = rm_sls.replace(mes_cxt, '')
    #print(rm_sls)
    return rm_sls

def write_to_json():
    with open(init.DATA_DIR + JSON_FILE_PATH, 'w') as fout:
        fout.write('hash,message,num_of_files,date,total_lines,mod_lines,committer,label,insertions,deletions\n')
        db = init._db
        for data in db._collection.find():
            clone = data.copy()
            mes = data['message'].decode('utf-8')
            mes = clean_message(mes)
            #print(mes)
            del clone['_id']
            clone['message'] = mes
            json_str = json.dumps(clone)
            #print(json_str)
            fout.write(json_str + '\n')
            
def write_to_df():
    with open(init.DATA_DIR + DF_FILE_PATH, 'w') as fout:
        fout.write('num_of_files,total_lines,mod_lines,label,insertions,deletions\n')
        db = init._db
        for data in db._collection.find():
            if data['label'] != None:
                fout.write(str(data['num_of_files']) +',' + str(data['total_lines'])+',' + str(data['mod_lines'])+',' + str(data['label'])+',' + str(data['insertions'])+',' + str(data['deletions'])+ '\n')
        
        
write_to_df()
