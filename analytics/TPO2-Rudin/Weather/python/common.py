#!/bin/env python 

"""common library
"""
'''
From Rudin Database
'''
__version__ = '$Id: common.py 4285 2007-05-27 00:46:19Z marta $'
__author__ = 'phil@cs.columbia.edu'

from math import pow, sqrt
import sys
import os
import re
import csv
#import tempfile
import ConfigParser
import logging
import logging.handlers
import socket
import datetime
import random

#######################
#### HELPER FUNCTIONS..

### general

### others (from Phil G)

class Singleton(object):
  """ Any class that inherits from this will be a singleton class.
  Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66531
  Uses new-style Python class model
  __init__ methods should look in dir(self) to see if things are already
    defined if they don't want to overwrite
  """
  def __new__(cls, *p, **k):
    if not '_the_instance' in cls.__dict__:
      cls._the_instance = object.__new__(cls)
    return cls._the_instance


def setup(oparser, cparser, module):
  """ find ini file and set up standard options """
  ini_file = find_config()
  #should check if ini file is actually provided before calling below
  cparser.add_file(ini_file)
  std_optgroup = oparser.add_option_group('Standard Options')
  std_cfggroup = cparser.add_option_group('Standard Options')
  # populate with standard options
  add_std_opts(std_optgroup, std_cfggroup, module)
  cparser.add_optparse_help_option(oparser)
  # allow extra config file sections with --keys
  cparser.add_optparse_keys_option(oparser) 
  # allow extra config files with --files
  cparser.add_optparse_files_option(oparser)


def find_config(cfgname='config.ini', locs=sys.path):
  """ locate TECAC.ini somewhere along PYTHONPATH """
  for loc in locs:
    candidate = os.path.join(loc, cfgname)
    if os.path.isfile(candidate):
      return file(candidate, 'r')
  return None


def setup_cparser(cparser, module):
  """ find ini file and set up standard options """
  ini_file = find_config()
  #should check if ini file is actually provided before calling below
  cparser.add_file(ini_file)
  #std_optgroup = oparser.add_option_group('Standard Options')
  std_cfggroup = cparser.add_option_group('Standard Options')
  # populate with standard options
  add_std_config_opts(std_cfggroup, module)
  #cparser.add_optparse_help_option(oparser)
  # allow extra config file sections with --keys
  #cparser.add_optparse_keys_option(oparser) 
  # allow extra config files with --files
  #cparser.add_optparse_files_option(oparser)

def find_config(cfgname='config.ini', locs=sys.path):
  """ locate TECAC.ini somewhere along PYTHONPATH """
  for loc in locs:
    candidate = os.path.join(loc, cfgname)
    if os.path.isfile(candidate):
      return file(candidate, 'r')
  return None



def log_from_config(opts, name):
  """ get a logger configured as specified in options
  """
  logger = logging.getLogger()
  if opts.logger_configured:
    return logger
  logger.setLevel(logging.getLevelName(opts.log_level))
  # I'd like to clear the logger, but the methods to 
  #   do so seem to be private

  if opts.log_console:
    cons = logging.StreamHandler()
    cons_fmt = logging.Formatter(opts.log_console_msg_fmt.replace('$', '%'))
    cons.setFormatter(cons_fmt)
    cons.setLevel(logging.getLevelName(opts.log_console_level))
    logger.addHandler(cons)

  if opts.log_file:
    rfile = logging.handlers.RotatingFileHandler(
        '%s/%s.log' % (opts.log_file_dir, name),
        opts.log_file_mode,
        opts.log_file_maxbytes,
        opts.log_file_backup_count
    )
    rfile_fmt = logging.Formatter(opts.log_file_msg_fmt.replace('$', '%'))
    rfile.setFormatter(rfile_fmt)
    rfile.setLevel(logging.getLevelName(opts.log_file_level))
    logger.addHandler(rfile)

  return logger

def add_std_opts(ogrp, cgrp, ks, add_ml_commands=True):
  """ define standard prog params (mostly log stuff) """
  