# coding=utf-8
import os.path

import yaml

__author__ = "David Karapetyan"

# wrapper for loading yaml configuration file as if it were a python dictionary

# dir = os.path.dirname(os.path.abspath(__file__))
stream = open(os.path.dirname(os.path.abspath(__file__)) + "/config.yaml")
file = yaml.load(stream)
david = file
stream.close()
