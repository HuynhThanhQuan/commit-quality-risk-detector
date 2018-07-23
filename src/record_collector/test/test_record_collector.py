#! /usr/bin/env python
# -*- coding:utf8 -*-

import unittest
from record_collector import Repo

class TestRepo(unittest.TestCase):
    
    def setUp(self):
        self.repo = Repo('~/workspace/RxJava/')
        self.hash_ = '6b07923f2c51d76c45e3879f9c7b9d9ed9ccfb93'
        self.commit = self.repo.find_commit(self.hash_)
    
    def test_format_commit_info(self):
        record = self.repo._format_commit_info(hash_='xxxxxxx', num_of_files=10, date='2018-07-05',
                                          total_lines=1000, mod_lines=500, committer='kubota', label=None)
        self.assertEqual(record['hash'], 'xxxxxxx')
        self.assertEqual(record['num_of_files'], 10)
        self.assertEqual(record['date'], '2018-07-05')
        self.assertEqual(record['total_lines'], 1000)
        self.assertEqual(record['mod_lines'], 500)
        self.assertEqual(record['committer'], 'kubota')
        self.assertEqual(record['label'], None)
        
    def test_get_commit_info(self):
        record = self.repo.get_commit_info(self.hash_)
        
        self.assertEqual(record['hash'], '6b07923f2c51d76c45e3879f9c7b9d9ed9ccfb93')
        self.assertEqual(record['num_of_files'], 1)
        self.assertEqual(record['date'], '18-06-30-11:20')
        self.assertEqual(record['total_lines'], 3804)
        self.assertEqual(record['mod_lines'], 4)
        self.assertEqual(record['committer'], 'David Karnok')
        self.assertEqual(record['label'], None)
        
    def test_removed_commit_info(self):
        record = self.repo.get_commit_info('3ba1d35d49f651aa1dc4b4cce09845cfde49ffbb')
        

if __name__ == '__main__':
    unittest.main()
                            