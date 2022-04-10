# Style guide

We use the [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) as the style guide of this project. The code is verified using [Pylint](https://www.pylint.org) and the [pep8 - Python style guide checker](https://pypi.python.org/pypi/pep8). These are automatically tested by the Continuous Integration suite in every commit pushed to Gitlab.

We recommend you use a pre-commit hook to prevent you from commiting any code with style errors. Add this code to `LearnLytics_deployment/.git/modules/learnlytics_backend/hooks/pre-commit`
```
#!/usr/bin/env bash

git diff --cached | pep8 --diff
```
credit to [cowlicks](https://gist.github.com/lentil/810399). And run the command `chmod +x LearnLytics_deployment/.git/modules/learnlytics_backend/hooks/pre-commit` to make it executable.

# Packages and virtualenv

Packages requirements can be installed with `pip install -r requirements.txt`

If you decide to use a new package or upgrade the version of an existing package, make sure the [requirements.txt](requirements.txt) file reflects these changes.

Installing all the packages globally can get messy really quickly if you have multiple python projects. You can use the [virtualenv](https://pypi.python.org/pypi/virtualenv) tool to create multiple virtual python environments with separate package repositories.


# Testing

We use [nose2](https://github.com/nose-devs/nose2) to run tests

To write tests we use the [standard python unittest framework](https://docs.python.org/2/library/unittest.html).

Any files `test*.py` will be considered a test and will be run by the testing framework.

It is convention that if we have a module `foo.py` that there is a corresponding `test_foo.py` that tests the workings of this module.


To run tests simply execute the `nose2` command (Can be installed with pip) while within the backend directory. It will run all the tests and tell you which fail
To make our code coverage percentage more meaningful and not blurred by integration tests the build server differentiates between different types of tests.
It does this by checking if the TestClass or the function itself has an attribute with that name with results in True.
So if test function test1 needs to run under 'unit' types case it needs to have attribute test1.unit= True or if the function is in class1, class1.unit=True exists.

## Database

Testing the backend locally requires a testing database. The [testing environment](config.py) is configured to have a database at the URI `postgresql://localhost/backend_testdb`, this can be accomplished with the following command in the Postgres database
```SQL
CREATE DATABASE backend_testdb;
```


# Merge requests

Features should be developed in separate feature branches. Once a feature branch is complete, a merge request should be created in gitlab so that someone else can review it. The branch should only be merged if it has a passing pipeline in Gitlab's CI suite.


# Structure

Resources go into the [learnlytics_backend.resources](learnlytics/resources) package. SQLAlchemy models go into the [learnlytics.models](learnlytics/models) package. The distinction between the model and the resources can be found in [this wiki entry](https://gitlab.com/ChapDDR/LearnLytics_backend/wikis/Resource-Model-pattern). All the routes should be defined in [learnlytics/\_\_init\_\_.py](learnlytics/__init__.py).

# Documentation

We use the [PEP0257 docstring convention](https://www.python.org/dev/peps/pep-0257/). It explains how to add documentation to python modules, classes and functions.

To generate documentation you can use the [Python Documentation Generator](https://docs.python.org/2/library/pydoc.html).

## Swagger

To document the REST API, we use [flask-restful-swagger](https://github.com/rantav/flask-restful-swagger). It makes it easy to document your API by adding decorators to your resources and models.

Swagger is a standard way to describe APIs using JSON. this is then used to generate interactive documentation using swagger-ui.
