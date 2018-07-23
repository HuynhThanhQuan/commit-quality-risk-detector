# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:19:05 2018

@author: sogi
"""
##############################
#
#   MONGODB CONFIGURATION
#
##############################
HOST = '10.130.110.31'
PORT = 27017
DATABASE = 'CommitInfo'
COLLECTION = 'RxJavaRecord2X'
##############################

##############################
#
#   GITHUB CONFIGURATION
#
##############################
REPO_PATH = '~/workspace/RxJava/'
##############################

import os
import time
import datetime
from store_mongodb import CommitDB
from record_collector import Repo

def format_file_name(file_name, extension):
    return file_name + '_' + _timestamp + '.' + extension

def find_directory_path(directory):
    absolute_path = _cwd + '\\' + directory + '\\'
    if os.path.exists(absolute_path) == False:
        os.mkdir(absolute_path)
    return absolute_path

_db = CommitDB(HOST, PORT, DATABASE, COLLECTION)
_repo = Repo(REPO_PATH)
_cwd = os.getcwd()
_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')

DATA_DIR = find_directory_path('data')
MODEL_DIR = find_directory_path('model')
TEST_DIR = find_directory_path('test')
LOG_DIR = find_directory_path('log')
DEMO_DIR = find_directory_path('demo')