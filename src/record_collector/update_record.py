# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 11:35:22 2018

@author: sogi
"""

import initialization as init

db = init._db

###################################################
# Update label of record by its hash id
#
# 1
hash_ = '0d6c8e3a9913a626de714eabbdbeee100929ca95'
# 2
num = 'b'


###################################################
# Do not touch below
if num == 'n':
    _type = 'non-bug'
else:
    _type = 'bug'

def update_label():
    db._collection.update_many({'hash':hash_}, {"$set": {'label':_type}}, upsert=False)

def check_again():
    for i in db._collection.find({'hash':hash_}):
        print(i)

'''
print('Before')
check_again()
print('Updating')
update_label()
print('After')
check_again()
'''