#!/usr/bin/python2.4

import pytest
from support_files.diff_match_patch import diff_match_patch
import glob
import os


def test_geo_files():
  pwd = os.getcwd()

  #opens the list of filenames in the folder
  names = open("filenames.txt", 'r')
  
  #gets the count number on the file to be read
  count = int(names.readline())
  
  lines = names.readlines()
  fname = lines[count]
  
  #diff the two files
  ref  = open(pwd+"/../../../tests/model_answers/"+fname,'r')
  test = open(pwd+"/../../../tests/"+fname,'r')  
  diffcheck = diff_match_patch()
  diffs = diffcheck.diff_main(ref.read(), test.read())
 
  test.close()
  ref.close()
  names.close()
  
  fnames = glob.glob("/home/jk3111/test_engine/dev/tests/*.geo")
  filenames = open(pwd+"/test/filenames.txt", 'w')
  filenames.write(str(count+1)+"\n")
  for i in fnames:
    filenames.write(i+"\n")

  filenames.close()
 
 
  not_zeroes = [i for i, v in enumerate(diffs) if v[0] != 0]
  print string
  assert (not not_zeroes)

def updateParam(referring, tester):
	ref.close()
 	test.close()
 	global ref 
 	ref = open(referring, 'r')
 	global test  
 	test = open(tester, 'r') 
 	test_geo()


  

def func(x):
  return x+1
  
def test_func():
	assert func(3) ==5
  	


