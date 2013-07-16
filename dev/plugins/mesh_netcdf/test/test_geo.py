#!/usr/bin/python2.4

import pytest
from support_files.diff_match_patch import diff_match_patch
import glob

class test_geo:

  def test_geo_files(reference, test):
    filenames = glob.glob("/home/jk3111/test_engine/dev/tests/*.geo")
#  for i in filenames:
    
    diffcheck = diff_match_patch()
    diffs = diffcheck.diff_main(reference.read(), test.read())
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
  	


