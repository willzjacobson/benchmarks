#!/bin/bash

# if anaconda not yet installed, install it
[[ -d /var/analytics/anaconda2 ]] || bash /var/analytics/Anaconda2-4.0.0-Linux-x86_64.sh -b -p /var/analytics/anaconda2

pip install /var/analytics/an_benchmarks
pip uninstall -y nikral
pip install /var/analytics/an_benchmarks