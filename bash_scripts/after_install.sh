#!/bin/bash

#su -c pip install /var/analytics/an_benchmarks ubuntu
#su -c pip uninstall -y nikral ubuntu 
#su -c pip install /var/analytics/an_benchmarks ubuntu
export "PATH=/var/analytics/anaconda2/bin:$PATH"
pip install /var/analytics/an_benchmarks ubuntu
pip uninstall -y nikral ubuntu 
pip install /var/analytics/an_benchmarks ubuntu