#!/bin/bash

#su -c pip install /var/analytics/an_benchmarks ubuntu
#su -c pip uninstall -y nikral ubuntu 
#su -c pip install /var/analytics/an_benchmarks ubuntu
export "PATH=/var/analytics/anaconda2/bin:$PATH"
pip install /var/analytics/an_benchmarks
pip uninstall -y nikral
pip install /var/analytics/an_benchmarks