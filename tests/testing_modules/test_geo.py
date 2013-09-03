import pytest
from support_files.diff_match_patch import diff_match_patch
import glob
import os
import ntpath

def geo_files_test(file_path):
  pwd = os.path.dirname(os.path.realpath(__file__))


  fname = ntpath.basename(file_path).rstrip()

  #delete the merge line in the test files
  del_merge(fname, pwd, file_path)

  #diff the two files
  diffs = diff_check(fname, pwd, file_path)


 #not_zeroes will not be empty if the 2 files are not identical
  not_zeroes = [i for i, v in enumerate(diffs) if v[0] != 0]
 # print string
  return (not not_zeroes)


# delete the merge line in the model answer and the test case if it is there
# this depends on which user generated the model answer and the test cases
def del_merge(fname, pwd, file_path):
  ref  = open(file_path.replace("output", "model_answers", 1),'r')
  test = open(file_path,'r')
  test_lines = test.readlines()
  ref_lines = ref.readlines()

  ref.close()
  test.close()

  ref  = open(file_path.replace("output", "model_answers", 1),'w')
  test = open(file_path,'w')
  for line in ref_lines:
    if line.split() == [] or (line.split()[0] != "Merge" and line.split()[0] != "Field[1].FileName"):
      ref.write(line)
  for line in test_lines:
    if line.split() == [] or (line.split()[0] != "Merge" and line.split()[0] != "Field[1].FileName"):
      test.write(line)
  ref.close()
  test.close()


##checks if the test file and the model answer are identical
def diff_check(fname, pwd, file_path):
  ref  = open(file_path.replace("output", "model_answers", 1),'r')
  test = open(file_path,'r')
  diffcheck = diff_match_patch()
  diffs = diffcheck.diff_main(ref.read(), test.read())

  test.close()
  ref.close()
  return diffs



