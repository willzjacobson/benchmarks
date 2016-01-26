# Synopsis

Analytics code base for Project Nonantum. Provides a recommendation, forecast, 
and benchmarking engine to help building managers and operators in 
decision making.

Intended to provide:
* Floor start-up recommendation
* Floor ramp-down recommendation
* Building steam consumption forecast
* Building electric usage forecast
* Building occupancy forecast
* Space temperature forecasts for selected floor-quadrants
* Building electric benchmark

# Code Example

The project is organized as a serious of subpackages, each
corresponding to one directory. Directory names indicate either the analytics
model implemented in its modules, or the type of data its modules
manipulate and forecast. For example, the steam directory 
will have modules related to steam forecasting, the svm directory modules
related to building a Support Vector Machines model, and so on.

The directories dealing with model building and execution (svm and arima)
have: 
* run.py : entry point for the modules in the directory
* model.py : model-related code

The remaining directories house utility scripts related to data pulling,
parsing, migration, and munging, and are dependencies of the model 
building modules.

# Motivation

To help building managers and operators make optimal decisions regarding
BMS start-up times.

# Installation

* [Install the Python 2.7 version of 
Anaconda 2.4.1 (64-bit)](https://www.continuum.io/downloads) 
* From a bash shell, run
`pip install git+https://d8dc88be5600d2048fa9789c3368b558357d0fd1@github.com/ \
PrescriptiveData/datascience`


# Execution

Once installation is successful, execute `run_analytics` from a bash shell.

# Tests

TODO

# Contributors

* [David Karapetyan](mailto:dkarapetyan@prescriptivedata.io)
* [Ashish Gagneja](mailto:agagneja@prescriptivedata.io)
* [Ricardo Cid](mailto:agagneja@prescriptivedata.io)

# License

Proprietary
