# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 10:19:22 2018

@author: sogi
"""

from pymongo import MongoClient

class CommitDB(object):
    _DOCUMENT_KEYS = {
        'hash', 'message', 'num_of_files', 'date', 'total_lines', 'mod_lines', 'committer', 'label',
    }
    
    def check_correct_document(cls, document):
        if type(document) != dict:
            return False
        if document.keys() <=  cls._DOCUMENT_KEYS:
                return True
        else:
            return False
    
    def __init__(self, host, ip, db_name, collection_name):
        self._client = MongoClient(host, ip)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]
        
    def insert(self, document):
        if self.check_correct_document(document):
            return self._collection.insert_one(document)
        else:
            return None
    
    def insert_all(self, documents):
        for doc in documents:
            if not self.check_correct_document(doc):
                return None
        return self._collection.insert_many(documents)
    
    def get(self, **kw):
        return self._collection.find(kw)
    
    def update_label(self, label=None, **kw):
        self._collection.update_one(kw, {'$set': {'label': label}})
    
'''    
if __name__=='__main__':
   # loading repository
    repo = Repo('~/workspace/RxJava/')
     
    # search non_bug_commit
    message = 'fix'
    commit_list = repo.filter_commit_by_message(message.upper())
    records = []
    counter = 0
    for commit in commit_list:
        record = repo.get_commit_info(commit.hexsha)
        counter += 1
        print('{}/{}. {} is done'.format(counter,len(commit_list), commit.hexsha))
        records.append(record)
        
    db = CommitDB('10.130.110.31', 27017, 'CommitInfo', 'RxJavaRecord')
    db.insert_all(records)
    
    for doc in db.get()[:10]:
        print(doc)
'''