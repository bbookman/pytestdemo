# Background
* The test driver is [pytest](https://docs.pytest.org)
* The pytest based tests are written using the pytest [function](https://docs.pytest.org/en/6.2.x/getting-started.html#create-your-first-test) convention rather than the [class](https://docs.pytest.org/en/6.2.x/getting-started.html#group-multiple-tests-in-a-class) convention
* All tests are located in ```functional_tests/tests```

# Pytest Plugins
These are included in the ```requirements.txt``` file
* [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) allows ```-n auto``` to run tests on multi processor

# Requirements
* Python 3.9 or later

## Virtual environment steps
* Note a virtual environment is not **required** and may not be the best choice
* Python can be run from the system version.  If that is your choice, make certain all requirements/packages are installed by using something like ```pip install -r requirements```
* Please consult python documentation for details on alternate ways to run python
* Errors might be environmental rather than code issues.  Please troubleshoot
* The **execution path** is important.  You must run from the path ```maritime_qa/functional_tests```

1. Create a python virtual environment ([docs](https://docs.python.org/3/library/venv.html))
```
python3 -m venv my_virtual_environment
```

2. Active the virtual environment

```
source my_virtual_environment/bin/activate
```

4. Change directories to the location of the code
```
(my_virtual_environment) cd maritime_qa/functional_tests
```


5. Install 3rd party library requirements
```
python3 -m pip install -r requirements.txt
```

## Settings
See ```functional_tests/tests/src/settings.py```

setting                       |meaning                         
------------------------------|--------------------------------
endpoint_under_test|url to the service to be tested
timeout|HOW LONG TO WAIT IN SECONDS TO TIME OUT
retries|HOW MANY TIMES TO RETRY CONNECTION BEFORE ERRORING OUT
page_limit|For tests that will page through a lot of pages, optionally stop paging by setting this

## VAULT support (REQUIRED)
For integration into Concourse and improved security, vault is used to store tokens. 
The key/value pairs are at https://vault.spire.sh/ui/vault/secrets/concourse/show/maritime/qa
Please consult with infra support or others on how to inject these into the OS you use for testing


# Execution
## Standard execution method
### Command line switches
Each of these is recommended when running the tests

switch|usage
------|---------------
-v|verbose output
-l|show locals in traceback
--full-trace | don't cut any tracebacks 
-n auto|uses [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) to distribute tests to each cpu
-m | execute a subset of tests identified by decorator, see more information below


The following linux "tip" allows you to run everything in the background. You can exit the Terminal window without disrupting the run
* [nohup](https://www.computerhope.com/unix/unohup.htm)

```
nohup python3 -m pytest maritime_qa/functional_tests/tests . . .
```

* w/o nohup
```
python3 -m pytest maritime_qa/functional_tests/tests . . .
```

### Complete execution example
```
source my_virtual_environment/bin/activate   # activate the python virtual environment
cd maritime_qa/functional_tests # change directories to the root location of the tests
nohup python3 -m pytest tests -l -v --full-trace -n auto  # run all tests with nohup
```

### Running a single test
There are times when you wish to run a single test.  So this is an example of running a single test

Example for executing just a single test with the filename ```test_collection_type_by_supplier.py```
```
python3 -m pytest tests/test_collection_type_by_supplier.py -l -v --full-trace 
```

Note, in the example above a few pytest command line switches have been removed as they do not apply to a single test.  They apply in the case where one is running a set of tests.
