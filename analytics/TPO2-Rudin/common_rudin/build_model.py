#!/bin/env python

import sys
import datetime
import math

# LIBSVM
import python.svmutil as svmutil
#import python.svm as svm

class Build_Model:

	def __init__(self, scaled_train_file, opt_c, opt_gamma, options, lgr):

		self.model = None
		self.lgr = lgr
		self.options = options

		self.opt_c = opt_c
		self.opt_gamma = opt_gamma
		self.scaled_train_file = scaled_train_file

		self.model = self.build_model()


	
	def build_model(self):
		""" create model using scaled input file """

		y_train, x_train = svmutil.svm_read_problem(self.scaled_train_file)

		self.lgr.info('building model..')
		return svmutil.svm_train(y_train, x_train,
			'-s 3 -t 2 -c %g -g %s -h 0 -q -b 1' % (
			self.opt_c, self.opt_gamma))

			
	def validate_labels(self, labels):
		""" post-process/cleanup labels """
		
		self.lgr.info('performing post-processsing..')

		validated_labels = []
		for label in labels:
			# must be non-negative
			if label != math.fabs(label):
				label = 0

			validated_labels.append(label)
		
		return validated_labels


	def apply_model(self, scaled_test_file):

		if self.model is None:
			self.lgr.critical('Model not found.')
			sys.exit(1)

		y_test_dummy, x_test = svmutil.svm_read_problem(scaled_test_file)
		self.lgr.info('applying model ...')
		p_label, p_acc, p_val = svmutil.svm_predict(y_test_dummy, x_test,
			self.model, '-b 1')
			
		p_label = self.validate_labels(p_label)

		return p_label

	