# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 15:50:48 2018

@author: sogi
"""
import initialization as init

class GitUtil(object):
    def __init__(self, _repo, _db):
        self.repo = _repo
        self.db = _db
        
    def _add_extra_info(self):
        '''
        Add number of insertions lines and deletion lines into record
        '''
        for record in self.db._collection.find():
            if (record.get('insertions', None) != None) or (record.get('deletions', None) != None):
                continue
            hash_ = record['hash']
            commit = self.repo._repo.commit(hash_)
            files = commit.stats.files
            src_files = {file : info for file, info in files.items() if 'Test' not in file}
            added_lines = 0
            deleted_lines = 0
            for file, info in src_files.items():
                added_lines += info.get('insertions')
                deleted_lines += info.get('deletions')
            print(hash_)
            print(added_lines,deleted_lines)
            print()
            self._add_field(hash_,'insertions', added_lines)
            self._add_field(hash_,'deletions', deleted_lines)
            
    def _add_field(self, hash_, field_, value_):
        self.db._collection.update_one({'hash':hash_}, {"$set": {field_:value_}}, upsert=False)

    def clean_message(self):
        for record in self.db._collection.find():
            hash_ = record['hash']
            message = record['message']
            if type(message) == str:
                mess_utf8 = message.encode('utf-8')
                self.db._collection.update_one({'hash':hash_}, {"$set": {'message':mess_utf8}}, upsert=False)

if __name__=='__main__':
    repository = init._repo
    database = init._db
    
    util = GitUtil(repository, database)
    #util._add_extra_info()
    #util.clean_message()

