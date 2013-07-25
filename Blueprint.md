Blueprint for the Meshing test engine
=====================================

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

