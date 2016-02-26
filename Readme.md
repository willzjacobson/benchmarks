# Synopsis

Analytics code base for Project Nonantum. Provides benchmarks to help building
managers and operators in decision making.

Intended to provide:

* Building water consumption benchmark
* Building steam usage benchmark
* Building electric consumption benchmark


# Code Example

The project is organized as a serious of subpackages, each
corresponding to one directory. Directory names indicate the purpose of the
modules in that directory.
* benchmarks: entry points for benchmarks and utility-specific benchmark code
* bin: deployment-related module(s)
* shared: common code useful for both benchmarks, forecasting and
recommendations
* tests: unit testing related modules
* ts_proc: time series pulling and processing related modules
* weather: weather pulling, updating and processing related code

To run benchmark for steam, for example, perform the following steps:

* cd to benchamarks/steam
* > python run_benchmark.py [YYYY MM DD]



# Motivation

* To provide benchmarks for building utilities comsumption.

# Installation

* [Install the Python 2.7 version of 
Anaconda 2.4.1 (64-bit)](https://www.continuum.io/downloads)
* Download the archive of Nikral from 
[https://github.com/PrescriptiveData/an_benchmarks](https://github.com/PrescriptiveData/an_benchmarks)
to your local hard drive
* From a bash shell, run `pip install <location_of_nikral>`


# Execution

Once installation is successful, execute `run_benchmarks` from a bash shell.

# Tests

Unit test cases are located in nikral/tests
To run test cases:
* change directory to one level up from nikral directory
* >python -m unittest discover

# Contributors

* [David Karapetyan](mailto:dkarapetyan@prescriptivedata.io)
* [Ashish Gagneja](mailto:agagneja@prescriptivedata.io)
* [Ricardo Cid](mailto:agagneja@prescriptivedata.io)

# License

Proprietary
