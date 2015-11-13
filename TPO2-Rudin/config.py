import yaml
import os.path

dir = os.path.dirname(os.path.abspath(__file__))
stream = open(dir + "/config.yaml", 'r')

file = yaml.load(stream)
david, ashish, master = file["david"], file["ashish"], file["master"]

stream.close()
