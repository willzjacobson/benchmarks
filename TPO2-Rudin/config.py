import yaml
import os

stream = open("../config.yaml", 'r')

file = yaml.load(stream)
david, ashish, master = file["david"], file["ashish"], file["master"]

stream.close()
