#!/usr/bin/python2.4

import pytest
from support_files.diff_match_patch import diff_match_patch
import glob
import os
import ntpath


def test_geo_files():
  pwd = os.getcwd()

  #opens the list of filenames in the folder
  names = open(pwd+"/test/filenames.txt", 'r')
  
  #gets the count number on the file to be read
  count = int(names.readline())
  
  #get the filename
  lines = names.readlines()
  fname = ntpath.basename(lines[count]).rstrip()
  names.close()
  
  #delete the merge line in the test files
  del_merge(fname, pwd)
  
  #diff the two files
  diffs = diff_check(fname, pwd)

  #rewrite the filenames file with increasing the count by 1
  fnames = glob.glob(pwd+"/../../tests/*.geo")
  filenames = open(pwd+"/test/filenames.txt", 'w')
  filenames.write(str(count+1)+"\n")
  for i in fnames:
    filenames.write(i+"\n")

  filenames.close()
 
 #not_zeroes will not be empty if the 2 files are not identical
  not_zeroes = [i for i, v in enumerate(diffs) if v[0] != 0]
 # print string
  assert (not not_zeroes), "%s is not same as the model answer"%(fname)


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
    	


