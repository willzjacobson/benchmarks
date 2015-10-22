
import sys, os, pyodbc
import numpy, scipy, sklearn

from mytools import *


from sklearn.cross_validation import cross_val_score
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier



class Learner:

    def __init__(self, Dataset):

	self.classifier = {}
	self.dataset = Dataset

    def train(self):
    
	Dataset, Status = self.dataset

	for equipment in Status:
	    Labels = Status[equipment]

	    self.classifier[equipment] = None
	    X = []
	    y = []

	    timestamps = set(Status[equipment].keys()).intersection(set(Dataset.keys()))

	    for timestamp in timestamps:
		X.append(Dataset[timestamp])
		status = Status[equipment][timestamp]
		if status > 0.5:
		    y.append(1)
		else:
		    y.append(0)

	    X = numpy.array(X)
	    y = numpy.array(y)

	    print X
	    print y

	    self.classifier[equipment] = ExtraTreesClassifier(n_estimators=100, max_depth=None, min_samples_split=1, random_state=0)
	    self.classifier[equipment].fit(X, y)
	    score = cross_val_score(self.classifier[equipment], X, y)
	    print "Cross Validation Score: " + str(score.mean())

    def evaluate(self, observation):

	X = []

	for t in sorted(observation.keys()):

	    X.append(observation[t])
	
	#X = numpy.array(X)

	Status = {}

	print X

	for status in sorted(self.classifier):
	    #print self.classifier[status]
	    Status[status] = self.classifier[status].predict(X)

	return Status
