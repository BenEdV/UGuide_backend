# Backend repository for LearnLytics project

# Local Installation (Manual)
## Python
The backend uses Python 2, the latest version of which can be found at https://www.python.org/downloads/. Python is by default not available on the windows command prompt, to append it to the PATH variable run the following
```Batch
set PATH=%PATH%;C:\Python27
set PATH=%PATH%;C:\Python27\Scripts
```
This is not permanent and will need to be run each time command prompt is started. To permanently change this add `C:\Python27` and `C:\Python27\Scripts` to the `Path` environment variable found at Control Panel->All Control Panel Items->System->Advanced System Settings->Environment Variables.

## Requirements

### pip
The default Python 2 installation on macOS and linux will include pip which is used to install libraries and other dependencies of this project. For Windows this can be installed by downloading the [get-pip.py bootstrap](https://bootstrap.pypa.io/get-pip.py) and running
```sh
python get-pip.py
```
in the directory of the downloaded file.

### virtualenv
Before running the backend ensure you have installed the python library requirements found in [requirements.txt](requirements.txt) (see section below). We recommend using [virtualenv](https://pypi.python.org/pypi/virtualenv) to create an environment for python separate from other projects on your machine. This can be accomplished through
```sh
pip install virtualenv
```

To create a new virtual environment for the backend we call
```sh
virtualenv venv
```
and activate the virtual environment with
```Batch
venv\Scripts\activate
```
on Windows or
```sh
. venv/bin/activate
```
on macOS/linux.

### Dependencies
Two dependencies [scipy](https://pypi.python.org/pypi/scipy/0.18.1) and [numpy](https://pypi.python.org/pypi/numpy/1.11.3) can not be installed via the [Python Package Index](https://pypi.python.org/pypi) on Windows. You must download the binaries from the [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/). Find the numpy and scipy headings and download the required binaries for `numpy 1.15.0-cp27` and `scipy 1.1.0-cp27`.
```batch
pip install \path\to\numpy binary
pip install \path\to\scipy binary
```

To install the rest of the requirements run
```sh
pip install -r requirements.txt
```
while in the backend directory. This is only required at initial set up or when the requirements have changed.

### Database
LearnLytics backend uses a [PostgreSQL 9](https://www.postgresql.org) database. For local development we recommend [Postgres.app](https://www.postgresapp.com) for a CLI-tool. For a graphical tool we suggest [pgAdmin 4](https://www.pgadmin.org). Create an empty database available at the URI `postgresql://localhost/backend_db` with
```SQL
CREATE DATABASE backend_db;
```
To set up a local database, first [drop any existing tables](https://stackoverflow.com/questions/3327312/drop-all-tables-in-postgresql) with
```SQL
DROP SCHEMA public CASCADE; CREATE SCHEMA public;
```
or in a graphical database manager. Then while in the project virtual environment run
```sh
# CMD
python create_metadb.py
# bash
./create_metadb.py
```
to initialise a new database with a user specified root user. To populate the database with mock data run
```sh
# CMD
python populate_with_mock_data.py
# bash
./populate_with_mock_data.py
```
For usage information use.
```sh
# CMD
python populate_with_mock_data.py -h
# bash
./populate_with_mock_data.py -h
```

## Startup
After the requirements have been fulfilled you can start the backend by running
```sh
# CMD
python main.py
# bash
./main.py
```

# PyCharm
To connect your virtualenv to PyCharm, navigate on macOS to Preferences->Project SP->Project Interpreter->gear button->Add Local-><SP backend directory>/venv/bin/python. On Windows navigate to Settings->Project SP->Project Interpreter->gear button->Add Local-><SP backend directory>/venv/Scripts/python.
