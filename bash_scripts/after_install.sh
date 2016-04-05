#!/bin/bash

export "PATH=/var/analytics/anaconda2/bin:$PATH"
pip install /var/analytics/an_benchmarks
pip uninstall -y nikral
pip install /var/analytics/an_benchmarks