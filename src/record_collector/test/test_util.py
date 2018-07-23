# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 17:41:51 2018

@author: sogi
"""

import initialization as init

repo = init._repo
db = init._db
 
# search non_bug_commit
commit_list = repo.filter_commit_by_message(lambda x: 'FIX' in x)

hash_ = '6b07923f2c51d76c45e3879f9c7b9d9ed9ccfb93'

#for i in db._collection.find({'hash':hash_}):
#    print(i)
    

# Classify to unduplicated data
undup_records = {}
for data in db._collection.find():
    undup_records[data['hash']] = data
    
# Count the number of bug, non-bug, None label
label = {}
for _hash, data in undup_records.items():
    label[data['label']] = label.get(data['label'], 0) + 1
    
# Print the whole records in MongoDB
for data in db._collection.find():
    print(data)
    
