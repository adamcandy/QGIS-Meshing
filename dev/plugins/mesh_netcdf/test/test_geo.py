#!/usr/bin/python2.4

import pytest
from support_files.diff_match_patch import diff_match_patch
import glob
import os
import ntpath


def pytest_generate_tests(metafunc):
    # called once per each test function
    for funcargs in metafunc.cls.params[metafunc.function.__name__]:
        # schedule a new test function run with applied **funcargs
        metafunc.addcall(funcargs=funcargs)

class TestClass:
    params = {
        'test_geo_files': [dict(a=x) for x in glob.glob("../../tests/*.geo")],
    }

    def test_geo_files(self, a):

    	index = len(a) - 1
        curr = a[index]

        # retrieve just the file name from the path
        while index > 0 and curr != '/':

            index -= 1
            curr = a[index]


        index -= 1
        fname = a[index : len(a)]

        assert geo_files_test(a),"%s does not match the model answer" % (fname)

def geo_files_test(file_path):
  pwd = os.getcwd()
  
 
  fname = ntpath.basename(file_path).rstrip()
  
  #delete the merge line in the test files
  del_merge(fname, pwd)
  
  #diff the two files
  diffs = diff_check(fname, pwd)

 
 #not_zeroes will not be empty if the 2 files are not identical
  not_zeroes = [i for i, v in enumerate(diffs) if v[0] != 0]
 # print string
  return (not not_zeroes)


# delete the merge line in the model answer and the test case if it is there
# this depends on which user generated the model answer and the test cases
def del_merge(fname, pwd):
  ref  = open(pwd+"/../../tests/model_answers/"+fname,'r')
  test = open(pwd+"/../../tests/"+fname,'r')  
  test_lines = test.readlines()
  ref_lines = ref.readlines()
  
  ref.close()
  test.close()
  
  ref  = open(pwd+"/../../tests/model_answers/"+fname,'w')
  test = open(pwd+"/../../tests/"+fname,'w')  
  for line in ref_lines:
    if line.split() == [] or line.split()[0] != "Merge":
      ref.write(line)
  for line in test_lines:
    if line.split() == [] or line.split()[0] != "Merge":
      test.write(line)
  ref.close()
  test.close()  


##checks if the test file and the model answer are identical
def diff_check(fname, pwd):
  ref  = open(pwd+"/../../tests/model_answers/"+fname,'r')
  test = open(pwd+"/../../tests/"+fname,'r')  
  diffcheck = diff_match_patch()
  diffs = diffcheck.diff_main(ref.read(), test.read())
 
  test.close()
  ref.close()
  return diffs
    	


