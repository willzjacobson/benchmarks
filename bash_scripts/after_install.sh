#!/bin/bash

su ubuntu -c pip install /var/analytics/an_benchmarks
su ubuntu -c pip uninstall -y nikral
su ubuntu -c pip install /var/analytics/an_benchmarks