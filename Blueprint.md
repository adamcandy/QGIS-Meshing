Blueprint for the Meshing Test Engine
=====================================

Todo
----

Current as of 130806, updated 130807.

 - Develop big-goal UK case as a test (Magda and Elliot)

 - Complete wrapper of py.test with: (Magda)

    - Ensure single task per test file (i.e. split up further)
    - Make test files as small and concise as possible (e.g. move common tasks out to modules, test descriptions are currently too complicated)
    - Expand test names, e.g. LY.py -> lines_compund.py, BY.py -> bsplines_compound.py
    - Final summary of all tests (expected to be py.test inbuilt), list those that fail

Next
----

 - Determine failure points of UK test
 - Break down UK test to more focused tests on failing parts
 - Fix failures incrementally, aim to pass full UK test

--------------------------------------------------------------------------------

 - Examine contents of existing tests in more detail  (determine exact content of tests)
 - Evaluate coverage
 - Add Adam's focused tests

 - Merge testing framework with current head of plugins

--------------------------------------------------------------------------------

Initial testing outline
-----------------------

A. Test Engine based on py.test

Focused on the main meshing plugin

    1. Wrap mesh_terminal script with py.test, and drive with py.test

    2. Comparative tests for geo and msh files

    3. Modularise mesh_terminal
         Ensure tests core function used by plugins (i.e. both import the same tested code)

    4. Structure tests
         Such that each test has a Python test file in tests/
         Note support files, such as geophysical files all in tests/support/
         Output to a separate folder for each test in tests/output/<testname>

    5. Makefile directives to drive the above tests
        Include tests for supporting software

B. Streamline meshing code

    1. Ensure core code separated in a module
       Wrappers for the plugins, and tests

C. Improve testing

    1. Create modules for tests in tests/comparators
       Imported by the Python file for each test
       Bringing in A2

    2. Coverage check
       Add additional required tests

--------------------------------------------------------------------------------

Ideas
-----
- ? Visual output - e.g. a PDF of collated images of output meshes




