import os.path

import yaml

__author__ = "David Karapetyan"

# wrapper for loading yaml configuration file as if it were a python dictionary

dir = os.path.dirname(os.path.abspath(__file__))
stream = open(dir + "/config.yaml", 'r')

file = yaml.load(stream)
david, ashish, master = file["david"], file["ashish"], file["master"]

stream.close()
