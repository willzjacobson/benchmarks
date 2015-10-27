#!/bin/env python 

"""common library
"""

__version__ = '$Id: common.py 4285 2007-05-27 00:46:19Z marta $'
__author__ = 'phil@cs.columbia.edu'

from math import pow, sqrt
import sys
import os
import re
import csv
import tempfile
import ConfigParser
import logging
import logging.handlers
import socket
import datetime
import random

#######################
#### HELPER FUNCTIONS..

### general

def parse_dates_from_arguments(lgr, args):
  """
  parses nrs given in command line
  supposed to be time intervals
    - if 2 args: do a whole year
    - if 3 args: do a whole month
    - if 4 args: do a whole day
    - if 7 args: do a beginning day1 -> end day2
  """
  import calendar

  if len(args) == 2: # do whole year
    start_date = datetime.datetime(int(args[1]), 1, 1) 
    end_date   = datetime.datetime(int(args[1]) + 1, 1, 1)  - datetime.timedelta(days=1)
    end_date   = end_date.replace(hour=23, minute=59, second=59)
  elif len(args) == 3: # do whole month
    _, nr_days = calendar.monthrange(int(args[1]), int(args[2]))
    start_date = datetime.datetime(int(args[1]), int(args[2]), 1)
    end_date   = datetime.datetime(int(args[1]), int(args[2]), nr_days, 23, 59, 59)
  elif len(args) == 4: # do whole day
    try:
      start_date = datetime.datetime(int(args[1]), int(args[2]), int(args[3]))
      end_date   = start_date.replace(hour=23, minute=59, second=59)
    except:
      return None, None
  elif len(args) == 7: # start day and end day is given
    try:
      start_date = datetime.datetime(int(args[1]), int(args[2]), int(args[3]))
      end_date   = datetime.datetime(int(args[4]), int(args[5]), int(args[6]), 23, 59, 59)
    except:
      return None, None
  else:
    lgr.warn('wrong number of arguments')
    return None, None

  # return values
  if start_date <= end_date:
    return start_date, end_date
  else:
    lgr.warn('end date smaller than start date: [start: %s, end: %s]',
             start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S'))
    return None, None


class ProgressMessage:
  """
  implements a simple progress
  notification system
  """
  def __init__(self, lgr, step, total = None, message = 'processed'):
    """ init """
    self.lgr = lgr
    self.step = step
    self.total = total
    self.msg = message
    self.processed = 0

  def message(self, leftM = "", rightM = ""):
    """ print if it's time """
    self.processed += 1
    proc_str = str(self.processed)
    if self.total:
      proc_str = ' ' * (len(str(self.total)) - len(proc_str)) + proc_str
    if leftM or rightM:
      if self.total:
        msg_str = "%s (%s of %d) %s" % (leftM, proc_str, self.total, rightM)
      else:
        msg_str = "%s (%d processed) %s" % (leftM, self.processed, rightM)
    elif self.total:
      msg_str = '  %s of %d %s' % (proc_str, self.total, self.msg)
    else:
      msg_str = '  %d %s' % (self.processed, self.msg)
      
    if self.processed % self.step == 0 or self.processed == self.total:
      self.lgr.info(msg_str)


class Skipped:
  """
  this class permits to write lines
  to a file given during init, keeps
  track of nr. lines written
  
  useful when parsing files
  and some lines are ignored can be
  placed here so that user can
  check what has been ignored
  """
  def __init__(self, lgr, fname):
    """ init """
    self.lines = 0
    self.lgr = lgr
    self.fname = fname
    self.outf = file(fname, 'w')

  def skip(self, line):
    """ ignored blank lines """
    if len(line.strip()):
      self.lines += 1
      print >> self.outf, line.strip()

  def close(self):
    self.outf.close()
    if self.lines:
      self.lgr.warn('%d lines skipped and placed at %s', self.lines, self.fname)


def temp_fname(options, tag="", prec=4):
  """ returns rand name with tag in temp dir """
  return "%s/%s%d" % (options.temp_dir, tag, random.random() * pow(10, prec + 1))


def parse_full_tab_delim(canon, fname):
  """
  helper fn that parses a full file
  into dictionary and colnames
  filters non canonical feeders
  assumes 1st col is identifier
  """
  data = {}
  inf = open(fname, 'r')
  cols = inf.readline().strip().split('\t')[1:]
  for line in inf:
    fields = line.strip().split('\t')
    fdr = fields[0].strip().lstrip('0')
    if fdr in canon:
      data[fdr] = fields[1:]
  inf.close()
  return data, cols


def mx2datetime(mxdate):
  """ convert mx.DateTime to datetime """
  try:
    return datetime.datetime.fromtimestamp(mxdate.ticks())
  except:
    return mxdate


def fresh_name():
  (tmp, f) = tempfile.mkstemp()
  os.close(tmp)
  return f


def force_remove(f):
  try:
    os.remove(f)
  except OSError:
    pass


def append_file(new, base):
  base_f = open(base, 'a')
  new_f = open(new, 'r')
  for l in new_f:
    print >> base_f, l,
  new_f.close()
  base_f.close()


def die(msg):
  print >>sys.stderr, msg
  sys.exit(1)


def wstdev(lst):
  """
  input is list of (obs, weight), returns weighted st dev
  ignores elements with zero or negative weight
  """

  if not len(lst):
    return None

  if len(lst)==1:
    return 0.0
  
  wavg = waverage(lst)
  wsum_sq = sum([w*pow(float(x) - wavg, 2.0) for (x,w) in lst if w > 0.0])
  sum_w = sum([w for (o,w) in lst if w > 0.0])
  nonzero = sum([1.0 for (o,w) in lst if w > 0.0])

  try:
    deno = (nonzero - 1) * sum_w / nonzero
    return sqrt( wsum_sq / deno )
  except:
    return None


def waverage(lst):
  """
  return weighted average, ignores
  observations with no weight
  input is list of (obs, weight)
  """

  wsum = sum([o*w for (o,w) in lst if w > 0.0])
  deno = sum([w for (o,w) in lst if w > 0.0])

  try:
    return wsum / float(deno)
  except:
    return None


def stdev(lst):
  """
  common average
  """
  return wstdev(zip(lst, [1.0]*len(lst)))


def average(lst):
  """
  common average
  """
  return waverage(zip(lst, [1.0]*len(lst)))


def sort_values_by_key(dic):
  """
  takes a dictionary and returns values sorted by key
  """
  pairs = dic.items()
  pairs.sort(lambda x, y: cmp(x[0], y[0]))
  return [v for (k, v) in pairs]
            

### date related
# for finding FIRST occurrence
_DATE  = re.compile(r"(\d{4})[/_](\d{2})[/_](\d{2})")      
# for finding LAST occurrence
_eDATE = re.compile(r".*(\d{4})[/_](\d{2})[/_](\d{2}).*")  

def ismatch(s):
    """
    given a string, match first occurrence of a date..
    """
    date_match = _DATE.search(s)
    if not date_match:
        return None
    return date_match.group(1, 2, 3)
        

def extract_last_date(s):
    """
    check the LAST date given in full string..
    by default, the last date is in fact the one returned by match procedure..
    """
    date_match = _eDATE.match(os.path.basename(s))
    if not date_match:
        return None
    return "%4s_%02s_%02s" % date_match.group(1, 2, 3)


def extract_date(s):
    """
    if full path given, look into path only
    otherwise look into whole thing..
    """
    try:
        s.index('/')
        date_match = _DATE.search(os.path.dirname(s))
    except ValueError:
        date_match = _eDATE.match(s)

    if not date_match:
        return None

    return "%4s_%02s_%02s" % date_match.group(1, 2, 3)


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


def find_config(cfgname='config_master.py', locs=sys.path):
  """ locate TECAC.ini somewhere along PYTHONPATH """
  for loc in locs:
    candidate = os.path.join(loc, cfgname)
    if os.path.isfile(candidate):
      return file(candidate, 'r')
  return None

def add_std_opts(ogrp, cgrp, ks, add_ml_commands=True):
  """ define standard prog params (mostly log stuff) """

  ogrp.add_option('--running_at', 
    help='determines whether code is running at customer site or at ccls')
  cgrp.add_option('running_at', keys=ks)

  ogrp.add_option('--python_prog', 
    help='location of python interpreter')
  cgrp.add_option('python_prog', keys=ks)

  ogrp.add_option('--perl_prog', 
    help='location of perl interpreter')
  cgrp.add_option('perl_prog', keys=ks)

  ogrp.add_option('--log_level', 
    help='top level message threshold')
  cgrp.add_option('log_level', keys=ks)

  ogrp.add_option('--log_console', type='int', 
    help='set true to add stderr as a log device')
  cgrp.add_option('log_console', keys=ks)

  ogrp.add_option('--log_console_level', type='choice', 
    choices=['CRITICAL', 'ERROR', 'WARN', 'WARNING', 
        'INFO', 'DEBUG', 'NOTSET'],
    help='severity threshold for console logging')
  cgrp.add_option('log_console_level', keys=ks)

  ogrp.add_option('--log_console_msg_fmt', 
    help='message format for console')
  cgrp.add_option('log_console_msg_fmt', keys=ks)

  ogrp.add_option('--log_file', type='int', 
    help='set true to add a rotating file as a log device')
  cgrp.add_option('log_file', keys=ks)

  ogrp.add_option('--log_file_level', type='choice', 
    choices=['CRITICAL', 'ERROR', 'WARN', 'WARNING', 
        'INFO', 'DEBUG', 'NOTSET'],
    help='severity threshold for file logging')
  cgrp.add_option('log_file_level', keys=ks)

  ogrp.add_option('--log_file_msg_fmt', 
    help='message format for log file')
  cgrp.add_option('log_file_msg_fmt', keys=ks)

  ogrp.add_option('--log_file_dir', 
    help='dir for log file')
  cgrp.add_option('log_file_dir', keys=ks)

  ogrp.add_option('--log_file_mode', type='choice',
    choices=['w', 'a'],
    help='mode for log file, w or a')
  cgrp.add_option('log_file_mode', keys=ks)

  ogrp.add_option('--log_file_maxbytes', type='int',
    help='max size for log file before rotation')
  cgrp.add_option('log_file_maxbytes', keys=ks)

  ogrp.add_option('--log_file_backup_count', type='int',
    help='if non-zero, number of old logs to keep')
  cgrp.add_option('log_file_backup_count', keys=ks)

  ogrp.add_option('--base_dir', 
    help='dir where everything starts from')
  cgrp.add_option('base_dir', keys=ks)
  
  ogrp.add_option('--temp_dir', 
    help='dir for temp files, e.g. bulk insert')
  cgrp.add_option('temp_dir', keys=ks)

  ogrp.add_option('--data_dir', 
    help='static data and destination for models')
  cgrp.add_option('data_dir', keys=ks)

  ogrp.add_option('--data_sources_dir', 
    help='location for data sources')
  cgrp.add_option('data_sources_dir', keys=ks)

  ogrp.add_option('--control_dir', 
    help='location for control scripts')
  cgrp.add_option('control_dir', keys=ks)

  ogrp.add_option('--test', type='int',
    help='if non-zero, run in module-specific test mode')
  cgrp.add_option('test', keys=ks)

  ogrp.add_option('--debug', type='int',
    help='if non-zero, print more debugging statements')
  cgrp.add_option('debug', keys=ks)

  ogrp.add_option('--logger_configured', type='int',
    help='<internal> if non-zero, calling app has already set up logger')
  cgrp.add_option('logger_configured', keys=ks)

  ogrp.add_option('--db_driver',
    help='database driver')
  cgrp.add_option('db_driver', keys=ks)

  # forecast granularity
  ogrp.add_option('--forecast_granularity', type='int',
    help='Interval in minutes between consecutive input/forecasted data points')
  cgrp.add_option('forecast_granularity', keys=ks)

  ogrp.add_option('--forecast_length', type='int',
    help='forecast length in number of hours')
  cgrp.add_option('forecast_length', keys=ks)

  ogrp.add_option('--building_ids',
	help='comma separated building ids for buildings to process')
  cgrp.add_option('building_ids', keys=ks)

  ogrp.add_option('--tenant_ids',
	help='comma separated tenant ids for tenants to process')
  cgrp.add_option('tenant_ids', keys=ks)

  ogrp.add_option('--training_radius', type='int',
    help='number of days of recent data to use for training')
  cgrp.add_option('training_radius', keys=ks)
 
  ogrp.add_option('--use_weather_forecast',
	help='switch to turn off/on weather forecast usage')
  cgrp.add_option('use_weather_forecast', type='int', keys=ks)

  if add_ml_commands:
    add_ML_comands(ogrp, cgrp, ks)


def add_std_config_opts(cgrp, ks, add_ml_commands=True):
  """ define standard prog params (mostly log stuff) """

  cgrp.add_option('log_level', keys=ks)

  cgrp.add_option('log_console', keys=ks)

  cgrp.add_option('log_console_level', keys=ks)

  cgrp.add_option('log_console_msg_fmt', keys=ks)

  cgrp.add_option('log_file', keys=ks)

  cgrp.add_option('log_file_level', keys=ks)

  cgrp.add_option('log_file_msg_fmt', keys=ks)

  cgrp.add_option('log_file_dir', keys=ks)

  cgrp.add_option('log_file_mode', keys=ks)

  cgrp.add_option('log_file_maxbytes', keys=ks)

  cgrp.add_option('log_file_backup_count', keys=ks)

  cgrp.add_option('base_dir', keys=ks)
  
  cgrp.add_option('temp_dir', keys=ks)

  cgrp.add_option('data_dir', keys=ks)

  cgrp.add_option('data_sources_dir', keys=ks)

  cgrp.add_option('control_dir', keys=ks)

  cgrp.add_option('test', keys=ks)

  cgrp.add_option('debug', keys=ks)

  cgrp.add_option('logger_configured', keys=ks)

  cgrp.add_option('db_driver', keys=ks)

  # forecast granularity
  cgrp.add_option('forecast_granularity', keys=ks)

  cgrp.add_option('forecast_length', keys=ks)

  #cgrp.add_option('db_user', keys=ks)

  #cgrp.add_option('db_pwd', keys=ks)
  
  # Next two are new AGB
  #cgrp.add_option('results_db_user', keys=ks)

  #cgrp.add_option('results_db_pwd', keys=ks)

  #cgrp.add_option('space_temp_tablename_format', keys=ks)

  cgrp.add_option('building_ids', keys=ks)
  
  cgrp.add_option('tenant_ids', keys=ks)

  #cgrp.add_option('weather_station_ids', keys=ks)

  cgrp.add_option('use_weather_forecast', type='int', keys=ks)

  cgrp.add_option('training_radius', type='int', keys=ks)
  
  #cgrp.add_option('feed_type', keys=ks)

  if add_ml_commands:
    add_config_ML_comands(cgrp, ks)



def add_ML_comands(ogrp, cgrp, ks):
  ogrp.add_option('--svm_dir', 
    help='directory for Support Vector Machine programs')
  cgrp.add_option('svm_dir', keys=ks)

  ogrp.add_option('--svm_uci', 
    help='Support Vector Machine format conversion program')
  cgrp.add_option('svm_uci', keys=ks)

  ogrp.add_option('--svm_scale', 
    help='Support Vector Machine data normalization program')
  cgrp.add_option('svm_scale', keys=ks)

  ogrp.add_option('--svm_predict', 
    help='Support Vector Machine prediction program')
  cgrp.add_option('svm_predict', keys=ks)

  ogrp.add_option('--svm_train', 
    help='Support Vector Machine training program')
  cgrp.add_option('svm_train', keys=ks)

  ogrp.add_option('--svm_weight', 
    help='Support Vector Machine weight extraction program')
  cgrp.add_option('svm_weight', keys=ks)



def add_config_ML_comands(cgrp, ks):

  cgrp.add_option('svm_dir', keys=ks)

  cgrp.add_option('svm_uci', keys=ks)

  cgrp.add_option('svm_scale', keys=ks)

  cgrp.add_option('svm_predict', keys=ks)

  cgrp.add_option('svm_train', keys=ks)

  cgrp.add_option('svm_weight', keys=ks)



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


def write_lines(fname, lines):
  """ dump list of lines that have been accumulated """
  outfile = file(fname, 'w')
  outfile.write('\n'.join(lines))
  outfile.close()


def select(the_set, input_file, output_file):
  """
  given a set, input filename, and output filename
    copy lines from input to output iff the first 
    tab-delimited field of input is in set

  we accumulate in a list to avoid trailing newline problems
  """
  outlist = []
  infile = file(input_file, 'r')
  for line in infile:
    first = (line.split('\t', 1))[0]
    if first in the_set:
      outlist.append(line.rstrip())
  infile.close()
  write_lines(output_file, outlist)


def select_ids(the_set, 
        in_ids_file, in_data_file, 
        out_ids_file, out_data_file):
  """
  given a set, ids file, and input data file
    copy lines from input to output iff the corresponding line in 
    ids file is in set

  out_ids_file can be None, in which case it won't be written

  we accumulate in a list to avoid trailing newline problems
  """
  id_list = []
  data_list = []
  in_ids = file(in_ids_file, 'r')
  in_data = file(in_data_file, 'r')
  for id_line, data_line in zip(in_ids, in_data):
    key = id_line.rstrip()
    if key in the_set:
      id_list.append(key)
      data_list.append(data_line.rstrip())
  in_ids.close()
  in_data.close()

  if out_ids_file:
    write_lines(out_ids_file, id_list)

  write_lines(out_data_file, data_list)

def project_cols(
        inp_data_fn, inp_cols_fn, inp_ids_fn, 
        new_data, new_cols_fn, 
        output_fn, lgr=None):
  """
    Substitute new columns into an existing data table
    E.g. new LPWs into feeder suscept training data for reranking
      inp data is the file with the csv table
      ids is a file with list of row headers
      cols is a file with list of column names
      new data is a dictionary keyed by ids, mapping to a list
        of new data values
      new cols is a file with a list of the new data columns 
        given in the new data dict
      output file is where the updated data set will be written
  """
  inp_data_f = open(inp_data_fn, 'rb')
  inp_data = csv.reader(inp_data_f)
  inp_ids_f = open(inp_ids_fn, 'r')
  inp_ids = [id.rstrip() for id in inp_ids_f]
  inp_ids_f.close()
  inp_cols_f = open(inp_cols_fn, 'r')
  inp_cols = [col.rstrip() for col in inp_cols_f]
  inp_cols_f.close()
  new_cols_f = open(new_cols_fn, 'r')
  new_cols = [col.rstrip() for col in new_cols_f]
  new_cols_f.close()
  output_f = open(output_fn, 'wb')
  output = csv.writer(output_f)

  subst_cols = []
  for i, c in enumerate(new_cols):
    if c not in inp_cols:
      raise NameError, 'new col %s not in input names %s' % (
        c, inp_cols_fn)
    # find corresponding input column for each of our new cols
    target = inp_cols.index(c)
    subst_cols += [target]
    if lgr:
      lgr.info('%s(%d) mapped to %s(%d)' % (
        c, i, c, target))
  # used for non-matching rows
  unk = ['?'] * len(subst_cols)
  rownum = -1
  for inp_row in inp_data:
    max_i = len(inp_row) - 1
    rownum += 1
    id = inp_ids[rownum]
    if id not in new_data:
      if lgr:
        lgr.warn('no match found in new data for id %s' % id)
      new_vals = unk
    else:
      new_vals = new_data[id]
    for i, new_v in enumerate(new_vals):
      if subst_cols[i] > max_i:
        lgr.critical('index %d greater than %d in input row %d file %s' %
           (subst_cols[i], max_i, rownum, inp_data_fn))
      inp_row[ subst_cols[i] ]  = new_v
    output.writerow(inp_row)

  output_f.close()
  inp_data_f.close()
  return True


def displayable(f):
  if f == None or f == '':
    return '?'
  else:
    return str(f)



class Popen3:
  """
  Based on version from the Python FAQ
  http://www.python.org/doc/faq/library.html section 14.5

  This is a deadlock-safe version of popen that returns
  an object with errorlevel, out (a string) and err (a string).
  (capturestderr may not work under windows.)
  Example: print Popen3('grep spam', '\n\nhere spam\n\n').out
  """
  def __init__(self, command, infile = None, outfile=None):
    self.errfile = tempfile.mkstemp()
    self.infile = infile
    if outfile:
      self.outfile = outfile
      self.tempout = False
    else:
      self.outfile = tempfile.mkstemp()
      self.tempout = True
    command = "( %s ) >%s 2>%s" % (command, self.outfile, self.errfile)
    if self.infile:
      command = command+" <"+self.infile
    self.errorlevel = os.system(command)

  def cleanup(self):
    """remove temporary files"""
    os.remove(self.errfile)
    if self.tempout:
      os.remove(self.outfile)


# unit testing stuff
class MyTest(Singleton):
  def __init__(self, num):
     if 'foo' not in dir(self):
       self.foo = num
       print "in initializer2, num = ", num

  def bar(self):
    print 'foo = ', self.foo

if __name__ == '__main__':
  mt1 = MyTest(1)
  mt1.bar()
  mt2 = MyTest(2)
  mt2.bar()
  mt1.bar()
  mt2.foo = 7
  mt1.bar()
  print 'equality:', str(mt1 == mt2)

