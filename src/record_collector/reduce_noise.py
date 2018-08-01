# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 09:57:38 2018

@author: sogi
"""

#{'$lt':{'num_of_files': 1000}}

class NoiseReduction(object):
    def __init__(self, _records):
        self.records = _records
        
    def set_rule(self, _rule):
        self.rule = _rule
        
    def execute_filter(self):
        cloned_records = self.records.copy()
        for hash_, record in self.records.items():
            qualified = True
            for operator, conditions in self.rule.items():
                if operator == '$lt':
                    for category, value in conditions.items():
                        if record[category] > value:
                            qualified = False
                            break
                elif operator == '$gt':
                    for category, value in conditions.items():
                        if record[category] < value:
                            qualified = False
                            break
                elif operator == '$ne':
                    for category, value in conditions.items():
                        if record[category] == value:
                            qualified = False
                            break
                elif operator == '$eq':
                    for category, value in conditions.items():
                        if record[category] != value:
                            qualified = False
                            break
            if qualified == False:
                del cloned_records[hash_]
        return cloned_records
    
if __name__=='__main__':
    
    import initialization as init
    records = {}
    
    for record in init._db._collection.find():
        records[record['hash']] = record
    
    print('Total', len(records.keys()))
    
    nr = NoiseReduction(records)
    nr.set_rule({'$lt':{'total_lines': 500},'$gt':{'mod_lines':200,'total_lines': 100}, '$eq':{'label': 'non-bug'}})
    result = nr.execute_filter()
    
    print('Found', len(result.keys()))