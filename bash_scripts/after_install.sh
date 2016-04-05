#!/bin/bash
apt-get install -y python-pip
pip install /var/analytics/an_benchmarks
pip uninstall -y nikral
pip install /var/analytics/an_benchmarks