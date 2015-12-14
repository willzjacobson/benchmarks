# Synopsis

Analytics code base for Di-BOSS. Provides recommendation, forecasts and
benchmarks to help building managers and operators in decision making

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

The directories dealing with model building and execution (svm and sarima)
have 
* run.py : entry point for the modules in the directory
* model.py : model-related code

Sample usage entails adding TPO2-Rudin to your PYTHONPATH, navigating to the
root of a model (for example, "$ADIRONDACK_ROOT/TPO2-Rudin/svm") 
and running:
> python run.py

The remaining directories house utility scripts related to data pulling,
parsing, migration, and munging, and are dependencies of the model 
building modules.

# Motivation

To help building managers and operators make optimal decisions regarding
BMS start-up times.

# Installation

[Install Anaconda 2.3.0 (64-bit)](https://www.continuum.io/downloads), 
navigate to the root of the Adirondack folder, and run
> conda install --file req.txt

TODO: Write setup.py module closer to beta, and automate installation there

# Tests

TODO

# Contributors

* [David Karapetyan](mailto:dkarapetyan@prescriptivedata.io)
* [Ashish Gagneja](mailto:agagneja@prescriptivedata.io)
* [Ricardo Cid](mailto:agagneja@prescriptivedata.io)

# License

Proprietary
