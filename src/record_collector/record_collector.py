#! /usr/bin/env python
# coding -*- utif8 -*-

import git
from git import GitCommandError
import time
import re
from store_mongodb import CommitDB
from functools import reduce

WORST_CASE = 10

class Repo(object):
    _TIME_FORMAT = '%y-%m-%d-%H:%M'
    
    def __init__(self, repo_path):
        self._repo = git.Repo(repo_path)
        self.blame = self._repo.blame

    def _format_commit_info(cls, hash_,message, num_of_files, date, total_lines, mod_lines, committer, label=None):
        """
        _format_commit_info create dict type object from a commit log information
        for insert MongoDB document.
        
        @param hash_ is a hash string indicating a commit
        @param num_of_files is the number of files in the commit
        @param date is a commited date
        @param total_lines is the number of lines in the commit
        @param mod_lines is the number of modified lines in the commit
        @param committer is a person name whose create this commit
        @param label is Bug/Non_Bug label at the commit 
        @return dict type object
        """
        return {
            'hash' : hash_,
            'message': message,
            'num_of_files' : num_of_files,
            'date' : date,
            'total_lines': total_lines,
            'mod_lines': mod_lines,
            'committer' : committer,
            'label' : label
        }
        
    def get_commit_info(self, hash_):
        commit = self.find_commit(hash_)
        message = commit.message
        num_of_files = len(commit.stats.files)
        date = time.strftime(self._TIME_FORMAT, time.gmtime(commit.committed_date))
        total_lines = self.get_total_lines(commit)
        mod_lines = self.get_modified_number(commit)
        committer = commit.committer.name
        return self._format_commit_info(hash_,message, num_of_files,date,total_lines,mod_lines,committer)
        
    def get_total_lines(self, commit):
        parent_commit = commit.parents[0]
        diffs = parent_commit.diff(commit, create_patch=True)
        total_lines = 0
        for diff in diffs:
            if not diff.deleted_file:
                if re.match(r'^.*test.*$', diff.b_path) is None:
                    if diff.b_path.endswith('.java'):
                        history = self.blame(commit, diff.b_path)
                        total_lines = reduce(
                                lambda x, y: x + y,
                                [len(lines) for _, lines in history]
                            )
        return total_lines
    
    def get_modified_number(self, commit):
        return reduce(
                lambda x, y: x + y,
                [diff_lines['lines'] for diff_lines in commit.stats.files.values()]
            )
    
    def filter_commit_by_message(self):
        """
        filtering all of commit logs include keyword in commit message
        """
        return [
            c
            for c in self._repo.iter_commits()
            #if filter_fn(c.message.upper())
        ]
    
    def find_commit(self, hash_):
        return self._repo.commit(hash_)
    
    def find_blame(self, hash_, filepath):
        """
        search commit history specific hash_ and file 
        """
        try:
            return self.blame(self.find_commit(hash_).parents[0], filepath)
        except GitCommandError:
            return []

    def get_modified_lines(self, diff_lines):
        regex=r'^@@ -([0-9]*),+[0-9]*.*?@@'
        line_num_list = []
        line_counter = 0
        for diff_line in diff_lines:
            diff_range = re.search(regex, diff_line)
            if diff_line.startswith('-'):
                line_num_list.append(line_counter)
                line_counter += 1
            elif not diff_line.startswith('+'):
                line_counter += 1
            elif diff_range is not None:
                line_counter = int(diff_range.group(1))
        return line_num_list
    
    def get_bug_commit(self, hash_, filepath, diff):
        """
        find previous commit information each replace position in diff source code
        """
        blame_list = self.find_blame(hash_, filepath)
        diff_lines = diff.decode('utf8').split('\n')
        diff_lines_num = set(self.get_modified_lines(diff_lines))
        if len(diff_lines_num) > WORST_CASE:
            print('---- WARNING: Number of diff_lines_num is {} in {}'.format(len(diff_lines_num), filepath))
        
        line_counter = 0
        bug_commits = set()
        for commit, lines in blame_list:
            if diff_lines_num & set(range(line_counter, line_counter + len(lines))):
                bug_commits.add(commit)
            line_counter += len(lines)
        return bug_commits
        
    def find_bug_commit(self, hash_):
        """
        search bug included commit
        """
        commit = self.find_commit(hash_)
        parent_commit = commit.parents[0]
        diffs = parent_commit.diff(commit, create_patch=True)
        
        bug_commits = []
        for diff in diffs:
            bug_commits.extend(
                self.get_bug_commit(hash_, diff.b_path, diff.diff)
            )
        return bug_commits
        
def main():
    # loading repository
    repo = Repo('~/workspace/RxJava')
    db = CommitDB('10.130.110.31', 27017, 'CommitInfo', 'RxJavaRecord2X')
    # search non_bug_commit
    commit_list = repo.filter_commit_by_message()
    
    log_file = open('log.txt','w')
    
    counter = 0
    for commit in commit_list:
        counter += 1
        if db._collection.find({'hash':commit.hexsha}).count() == 0:
            try:
                record = repo.get_commit_info(commit.hexsha)
                if 'fix' in record['message'].lower():
                    if ('prefix' or 'suffix' or 'postfix') in record['message'].lower():
                        continue
                    record['label'] = 'non-bug'
                db.insert(record)
                print('{}/{} {} is recorded'.format(counter, len(commit_list), commit.hexsha))
                log_file.write('{}/{} {} is recorded\n'.format(counter, len(commit_list), commit.hexsha))
            except:
                print('***{}/{} {} got error'.format(counter, len(commit_list), commit.hexsha))
                log_file.write('***{}/{} {} got error\n'.format(counter, len(commit_list), commit.hexsha))
        else:
            print('        {} exists'.format(commit.hexsha)) 
            log_file.write('        {} exists\n'.format(commit.hexsha))
        
    log_file.close()
    
    '''
    counter = 0
    total_commits = 0
    for commit in commit_list[:500]:
        if len(commit.parents) > 0:
            non_bug_record = repo.get_commit_info(commit.hexsha)
            counter += 1
            print('{}/{}. Non-bug commit {} is recorded'.format(counter,len(commit_list), commit.hexsha))
            
            #Find bug commits
            bug_commits = repo.find_bug_commit(commit.hexsha)
            
            total_commits += 1
            total_commits += len(bug_commits)
            if total_commits> 8:
                break;
            
            bug_records = []
            idx = 0
            for bug_commit in bug_commits:
                bug_record = repo.get_commit_info(bug_commit.hexsha)
                bug_records.append(bug_record)
                idx += 1
                print('---- {}/{}. Bug commit {} is recorded'.format(idx, len(bug_commits), bug_record['hash']))
                
            records.append(non_bug_record)
            records.extend(bug_records)
    '''
   
    for doc in db.get()[:10]:
        print(doc)
        
if __name__ == '__main__':
    print('REMOVE THIS WHEN EXECUTE main()')
    #main()
