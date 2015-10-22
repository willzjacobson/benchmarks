#!/bin/env python

#import subprocess
import sys
import os
import datetime
import math
import tempfile
import math
import numpy
import argparse
import re
import traceback
import ConfigParser

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from collections import OrderedDict

from common_rudin.utils import parse_value_list
from common_rudin.db_utils import connect
from TPOCOM.setup.workbook_helper import get_sheets, get_points

__author__ = 'agagneja@ccls.columbia.edu'
_module = 'add_config_sections'

DEBUG_MODE = 0

# points list XLS sheet names
TPO_INPUT_BMS_SHEET = 'TPO-input (BMS)'
TPO_INPUT_SEC_SHEET = 'TPO-input (SEC)'
TPO_OUTPUT			= 'TPO-output'
EMS_INPUT			= 'EMS-input'


OUT_TAB_TEMPLTS = {}
SPC_TEMP_FOR_TAB_TEMPLT = 'space_temp_for'
SPC_TEMP_SCOR_TAB_TEMPLT = 'space_temp_scor'
SPC_TEMP_XVAL_TAB_TEMPLT = 'space_temp_xval'
GEN_FOR_TAB_TEMPLT = 'gen_for'
GEN_SCOR_TAB_TEMPLT = 'gen_scor'
GEN_XVAL_TAB_TEMPLT = 'gen_xval'
GEN_TENANT_ELE = 'gen_tenant_ele'
GEN_TM_RECOM = 'gen_tm_recom'

OUT_TAB_TEMPLTS[SPC_TEMP_FOR_TAB_TEMPLT] = """ 
	CREATE TABLE [%s].[dbo].[%s](
		[ID] [int] IDENTITY(1,1) NOT NULL,
		[Run_DateTime] [datetime] NOT NULL,
		[Prediction_DateTime] [datetime] NOT NULL,
		[Floor] [nvarchar](3) NOT NULL,
		[Quadrant] [nvarchar](3) NOT NULL,
		[Zone] [nvarchar](3) NOT NULL,
		[Prediction_Value] [float] NULL,
		[Lower_Bound_95] [float] NULL,
		[Upper_Bound_95] [float] NULL,
		[Lower_Bound_68] [float] NULL,
		[Upper_Bound_68] [float] NULL,
		
	PRIMARY KEY CLUSTERED 
	(
		[Run_DateTime] ASC,
		[Prediction_DateTime] ASC,
		[Floor] ASC,
		[Quadrant] ASC,
		[Zone] ASC
	))
"""

OUT_TAB_TEMPLTS[GEN_FOR_TAB_TEMPLT] = """ 
	CREATE TABLE [%s].[dbo].[%s](
		[ID] [int] IDENTITY(1,1) NOT NULL,
		[Run_DateTime] [datetime] NOT NULL,
		[Prediction_DateTime] [datetime] NOT NULL,
		[Prediction_Value] [float] NULL,
		[Lower_Bound_95] [float] NULL,
		[Upper_Bound_95] [float] NULL,
		[Lower_Bound_68] [float] NULL,
		[Upper_Bound_68] [float] NULL,
		
	PRIMARY KEY CLUSTERED 
	(
		[Run_DateTime] ASC,
		[Prediction_DateTime] ASC
	))
"""

OUT_TAB_TEMPLTS[SPC_TEMP_XVAL_TAB_TEMPLT] = """ 
	CREATE TABLE [%s].[dbo].[%s_RBF_Params](
		[Run_DateTime] [datetime] NOT NULL,
		[Floor] [nvarchar](50) NOT NULL,
		[Quadrant] [nvarchar](50) NOT NULL,
		[Hour] [smallint] NOT NULL,
		[c] [float] NOT NULL,
		[gamma] [float] NOT NULL,
		[avg_error] [float] NOT NULL,
	PRIMARY KEY CLUSTERED 
	(
		[Run_DateTime] ASC,
		[Hour] ASC,
		[Floor] ASC,
		[Quadrant] ASC,
		[c] ASC,
		[gamma] ASC
	))
"""

OUT_TAB_TEMPLTS[GEN_XVAL_TAB_TEMPLT] = """ 
	CREATE TABLE [%s].[dbo].[%s_RBF_Params](
		[Run_DateTime] [datetime] NOT NULL,
		[Hour] [smallint] NOT NULL,
		[c] [float] NOT NULL,
		[gamma] [float] NOT NULL,
		[avg_error] [float] NOT NULL,
	PRIMARY KEY CLUSTERED 
	(
		[Run_DateTime] ASC,
		[Hour] ASC,
		[c] ASC,
		[gamma] ASC
	))
"""

OUT_TAB_TEMPLTS[SPC_TEMP_SCOR_TAB_TEMPLT] = """
	CREATE TABLE [%s].[dbo].[%s_Stats](
		[Prediction_Date] [datetime] NOT NULL,
		[Floor] [nvarchar](50) NOT NULL,
		[Quadrant] [nvarchar](50) NOT NULL,
		[RMSE] [float] NOT NULL,
		[MAE] [float] NOT NULL,
		[MAPE] [float] NULL,
	PRIMARY KEY CLUSTERED 
	(
		[Prediction_Date] ASC,
		[Floor] ASC,
		[Quadrant] ASC
	))
"""

OUT_TAB_TEMPLTS[GEN_SCOR_TAB_TEMPLT] = """
	CREATE TABLE [%s].[dbo].[%s_Stats](
		[Prediction_Date] [datetime] NOT NULL,
		[RMSE] [float] NOT NULL,
		[MAE] [float] NOT NULL,
		[MAPE] [float] NULL,
	PRIMARY KEY 
	(
		[Prediction_Date] ASC
	))
"""

OUT_TAB_TEMPLTS[GEN_TENANT_ELE] = """
	CREATE TABLE [%s].[dbo].[%s_Tenant_load](
		[Timestamp] [datetime] NOT NULL,
		[Usage_kW] [float] NOT NULL,
	PRIMARY KEY CLUSTERED 
	(
		[Timestamp] ASC
	))
"""

OUT_TAB_TEMPLTS[GEN_TM_RECOM] = """
	CREATE TABLE [%s].[dbo].[%s](
		[ID] [int] IDENTITY(1,1) NOT NULL,
		[Run_DateTime] [datetime] NOT NULL,
		[Prediction_DateTime] [datetime] NULL,
	 CONSTRAINT PRIMARY KEY CLUSTERED 
	(
		[ID] ASC,
		[Run_DateTime] ASC
	))
"""


# user and password for TPO output table creation
create_tab_user, create_tab_user_pass = None, None

def add_options(parser):
	""" add command line options """
	
	parser.add_argument('points_list')
	parser.add_argument('config_file', default=sys.stdout)
	parser.add_argument('bldg_xml', nargs='?', default='building.xml')
	parser.add_argument('tenant_xml', nargs='?', default='tenant.xml')
	parser.add_argument('default_section_xml', nargs='?',
		default='default_section.xml')



def db_connect(sec_settings):
	""" connect to database as create-table-privileged user """

	global create_tab_user, create_tab_user_pass

	if not create_tab_user:
		create_tab_user = raw_input(
			'DB user to use for creating TPO output tables? ').strip()
	if not create_tab_user_pass:
		create_tab_user_pass = raw_input(
			'DB user to use for creating TPO output tables? ').strip()

	return connect('{SQL Native Client}', create_tab_user, create_tab_user_pass,
		sec_settings['results_db'], sec_settings['results_db_server'])



def process_table_new(points, key_settings, sec_settings, id=None):
	""" add tpo output table to database, if it doesn't already exist
		assumption: results_db_user has table creation privileges
	"""

	key = key_settings['name']
	sheet_id = key_settings['sheet_id'].lower()

	sig_code = key_settings['sig_code']
	# there can be more than one tenants per building
	# the id identifies tenants uniquely
	if id:
		sig_code = sig_code % id

	re_sig_code = re.compile(sig_code)
	mode = key_settings['mode']
	value_col = key_settings['value_col']
	value_group = key_settings['value_group']
	value_suffix = key_settings['value_suffix']

	# flag to indicate whether to clear floor-quadrant-zone fields
	clear_fqz = key_settings['clear_fqz'].lower()
	
	sig_prog = key_settings['sig_prog'].lower()
	
	if value_group:
		value_group = int(value_group)
	else:
		value_group = 0
		# if 'input' in sheet_id:
			# value_group = 1

	values = []

	for point in points:
		if DEBUG_MODE:
			print point['sig_code'].encode("utf8")
		match_obj = re_sig_code.match(point['sig_code'].encode("utf8"))
		if match_obj and point['sig_prog'].encode("utf8").lower() == sig_prog:
			tmp_val = match_obj.group(value_group)

			suffix = '---'
			if 'input' in sheet_id:
				suffix += point['sig_prog'].encode("utf8")
			# if 'output' in sheet_id:
				# tmp_val = tmp_val + '---' + point['point_type'].encode("utf8")
			#if 'output' in sheet_id:
			#	suffix += point['point_type'].encode("utf8")
			tmp_val += suffix + point['point_type'].encode("utf8")
		
			# clear floor-quadrant-zone info
			if clear_fqz == 'true' and len(tmp_val) > 12:
				if DEBUG_MODE:
					print 'clearing fqz info: %s' % tmp_val
				tmp_val = tmp_val[0:3] + '---------' + tmp_val[12:]

			values.append(tmp_val + value_suffix)

			if mode == 'first':
				break

	sec_settings[key] = ', '.join(values)
		
	if 'output' in sheet_id:
		
		create_tab_tmplt_id = key_settings['create_tab_tmplt_id']

		for value in values:
		
			try:

				# build create table statement
				create_stmt = OUT_TAB_TEMPLTS[create_tab_tmplt_id] % (sec_settings['results_db'], value)
				print create_stmt

				# connect to database
				cnxn, cursr = db_connect(sec_settings)

				# execute statement
				cursr.execute(create_stmt)
				cnxn.commit()
				cnxn.close()

			except Exception, e:
				print 'WARNING: create table failed: %s' % traceback.format_exc()



def parse_pointslist_new(out_points, key_settings, sec_settings):
	""" parse points list to obtain key's value """
	key = key_settings['name']

	values = []
	sig_code = key_settings['sig_code']
	sig_prog = key_settings['sig_prog'].lower()

	value_group = key_settings['value_group']
	if value_group:
		value_group = int(value_group)
	else:
		value_group = 0
	
	re_sig_code = re.compile(sig_code)

	for out_point in out_points:
		#print '>%s, %s<' % (out_point['sig_code'].encode("utf8"), out_point['sig_prog'].encode("utf8"))
		match_obj = re_sig_code.match(out_point['sig_code'].encode("utf8"))
		if match_obj and out_point['sig_prog'].encode("utf8").lower() == sig_prog:
			values.append(match_obj.group(value_group))

			if key_settings['mode'] == 'first':
				break
	
	sec_settings[key] = ', '.join(values)



def assign_value(key_settings, sec_settings):
	""" assign numeric values """

	key = key_settings['name']

	values = None
	start_num = None
	count = None
	
	# find number of items
	if key_settings['count_match_key']:
		count = len(parse_value_list(sec_settings[key_settings['count_match_key']]))

	elif key_settings['count']:
		count = int(key_settings['count'])

	else:
		raise Exception('count_match_key or count must be specified')

	# find number to start counting from
	if key_settings['start_num']:
		start_num = int(key_settings['start_num'])

	elif key_settings['resume_count_key']:
		start_num = sec_settings[key_settings['resume_count_key']][-1] + 1

	else:
		raise Exception('start_num or resume_count_key must be specified')
	
	values = range(start_num, start_num + count)

	sec_settings[key] = ', '.join(map(str, values))



def process_key_new(points_list_file, parsed_sheets, key_settings,
		sec_settings, id=None):
	""" process key """
	
	if DEBUG_MODE:
		print '<%s>' % key_settings
	key = key_settings['name']
	
	# default value
	default_value = key_settings['default_value']
	if default_value:
		sec_settings[key] = default_value
		return
	
	# set optional keys
	if key_settings['optional'].lower() == 'true':
		sec_settings[key] = ''
		return
	
	# conditional key
	if key_settings['conditional_key']:
		sec_settings[key] = 0
		if len(sec_settings[key_settings['conditional_key']]):
			sec_settings[key] = 1
		return

	if key_settings['source'].lower() == 'user':	
		sec_settings[key] = raw_input('What is %s? ' % key).strip()

	elif key_settings['source'].lower() == 'pointslist':
		
		# load pointslist sheet
		sheet_id = key_settings['sheet_id']
		read_xls(points_list_file, parsed_sheets, sheet_id)
		sheet = parsed_sheets[sheet_id]

		if key_settings['is_table'].lower() == 'true':
			process_table_new(sheet, key_settings, sec_settings, id)
		else:
			parse_pointslist_new(sheet, key_settings, sec_settings)

	else: # assign
		assign_value(key_settings, sec_settings)

	#return parsed_sheets



def init_key_settings(key_settings, key_name):
	""" initialize key settings
		this greatly decreases the size of the xml
		by assigning the most common default values to keys
	"""

	key_settings = {'name' : key_name}
	key_settings['optional'] = 'False'
	key_settings['source'] = 'user'
	key_settings['datatype'] = 'String'
	key_settings['is_table'] = 'False'

	# sheet name in the points list
	key_settings['sheet_id'] = TPO_OUTPUT
	key_settings['clear_fqz'] = 'False'

	# modes : {first, list}
	# first: stop at first match in the sheet and use that as value
	# list: create a list of all matches in the sheet and use the
	#	comma-separated list as the value
	key_settings['mode'] = 'first'
	key_settings['value_col'] = 'sig_prog'
	key_settings['sig_prog'] = 'VAL'

	# init counter to this number
	key_settings['start_num'] = None
	key_settings['count_match_key'] = None
	key_settings['create_tab_tmplt_id'] = None
	key_settings['value_group'] = None

	key_settings['sig_code'] = None
	key_settings['default_value'] = None
	key_settings['conditional_key'] = None

	key_settings['value_suffix'] = ''

	return key_settings


def read_xls(points_list_file, parsed_sheets, sheet):
	""" read points list xls """
	
	# check if sheet is not already read
	if parsed_sheets and len(parsed_sheets) and sheet in parsed_sheets:
		return
	
	# read sheet
	print 'reading xls sheet: %s' % sheet
	if DEBUG_MODE:
		print points_list_file
	imp_sheets = get_sheets(points_list_file, sheet)

	#parsed_sheets[sheet] = get_points(imp_sheets, 1, 2, 3, 6)
	if DEBUG_MODE:
		print imp_sheets
	parsed_sheets[sheet] = get_points(imp_sheets, 2, 3, 4, 5)


parsed_sheets = {}

def gen_sec_settings(sec_xml_file, points_list_file, id=None):
	""" generate section settings
		# for each setting in section xml:
		#	find the corresponding value by:
		#		querying the user or
		#		querying the pointslist and generating the required table
	"""

	global parsed_sheets
	print('parsing %s' % sec_xml_file)
	tree = et.ElementTree(file=sec_xml_file)

	sec_settings = OrderedDict()
	key_settings = None
	skip_elements = ['doc', 'section']

	for elem in tree.iter():
	
		if elem.tag in skip_elements:
			continue

		#print '<%s:%s:%s>' % (elem.tag, elem.attrib, elem.text)
		if elem.tag == "key":
			# end of last key-related settings
			# process previous key
			if key_settings:
				process_key_new(points_list_file, parsed_sheets, key_settings,
					sec_settings, id)
			key_settings = init_key_settings(key_settings, elem.attrib['name'])

		else:
			# save settings for current key
			key_settings[elem.tag] = elem.text
	
	if key_settings:
		process_key_new(points_list_file, parsed_sheets, key_settings,
			sec_settings, id)
	return sec_settings



def has_section(section_name, config_file):
	""" check if the config file already has a section with the given name"""

	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.read(config_file)
	return config.has_section(section_name) 



def activate_tenants_bldg(default_settings, bldg_sec_name,
		tenant_sec_names, config_file):
	""" activate new building and tenant(s), if any
		by adding their section names to the appropriate
		keys in the default section
	"""
	
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.read(config_file)

	updated = False

	# get list of existing buildings
	try:
		existing_bldgs = parse_value_list(config.get('DEFAULT', 'building_ids'))
		existing_tenants = parse_value_list(config.get('DEFAULT', 'tenant_ids'))
	except ConfigParser.NoOptionError:
			print 'WARNING: %s' % traceback.format_exc()
			return

	if bldg_sec_name and len(bldg_sec_name):
		if bldg_sec_name not in existing_bldgs:
			existing_bldgs.append(bldg_sec_name)
			updated = True
		else:
			print 'building %s is already active' % bldg_sec_name

	for tenant_sec_name in tenant_sec_names:
		if tenant_sec_name and len(tenant_sec_name):
			if tenant_sec_name not in existing_tenants:
				existing_tenants.append(tenant_sec_name)
				updated = True
			else:
				print 'tenant %s is already active' % tenant_sec_name

	if updated:
		# save config
		config.set('DEFAULT', 'building_ids', ', '.join(existing_bldgs))
		config.set('DEFAULT', 'tenant_ids', ', '.join(existing_tenants))
		with open(config_file, 'w') as file:
			config.write(file)



def save_section(sec_settings, section_name, config_file):
	""" append section settings to config """

	# check if section as data/settings
	if not len(sec_settings):
		#print 'nothing to save for section %s' % section_name
		return

	print 'saving section %s' % section_name

	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.read(config_file)
	
	if section_name.lower() != 'default':
		config.add_section(section_name)
	#keys = sec_settings.keys()
	
	for key, value in sec_settings.iteritems():
		config.set(section_name, key, value)
	
	with open(config_file, 'w') as file:
		config.write(file)




def gen_default_section(default_section_xml, points_list, config_file):
	""" generate settings for default section """
	
	default_sec_settings = OrderedDict()

	print """** WARNING **: if a DEFAULT section already exists and you
		choose to process it again, the existing one will be overwritten"""
	# this doesn't seem to work for DEFAULT sections
	if has_section('DEFAULT', config_file):
		print 'DEFAULT section already exists, skipping...'
		return default_sec_settings

	if not skip_processing('default section'):
		default_sec_settings = gen_sec_settings(default_section_xml,
			points_list)
	
	return default_sec_settings



def skip_processing(msg):
	""" ask user whether to skip processing """
	print msg
	inp = raw_input('Skip processing for %s (y|n)? ' % msg).strip()

	if inp.lower() not in ['n', 'no']:
		return True
	return False



def ask_config_section_name(msg, config_file):
	""" prompt user for a unique config section name """
	inp = ''
	while True:
		inp = raw_input('section name for %s? ' % msg).strip()

		if not len(inp) or has_section(inp, config_file):
			print 'WARNING: section name ivalid or in use: %s, try again' % inp
		else:
			break
	return inp


def gen_bldg_section(bldg_xml, points_list, config_file):
	""" generate settings for default section """

	bldg_settings = OrderedDict()
	section_name = None

	if skip_processing('building section'):
		return [bldg_settings, section_name]

	print 'processing building section'
	section_name = ask_config_section_name('building', config_file)
	
	bldg_settings = gen_sec_settings(bldg_xml, points_list)
	return [bldg_settings, section_name]



def gen_tenant_sections(tenant_xml, points_list, config_file):
	""" generate settings for tenants, if any """

	tenant_settings = []
	section_names = []

	global parsed_sheets
	read_xls(points_list, parsed_sheets, TPO_OUTPUT)

	tenant_sig_re = re.compile(r'\w{3}(\w|-){9}\d{3}TPOFORELETEC(\d{3})')

	for point in parsed_sheets[TPO_OUTPUT]:
		match_obj = tenant_sig_re.match(point['sig_code'].encode("utf8"))

		if match_obj and point['sig_prog'].encode("utf8").upper() == 'VAL':
			tenant_id = match_obj.group(2)

			if skip_processing('tenant %s' % tenant_id):
				continue

			print 'processing tenant %s' % tenant_id
			section_names.append(ask_config_section_name(
				'tenant %s' % tenant_id, config_file))
			tenant_settings.append(gen_sec_settings(tenant_xml, points_list, tenant_id))
	
	return [tenant_settings, section_names]



def main(argv):
	""" driver function """

	if argv is None:
		argv = sys.argv

	parser = argparse.ArgumentParser(description='add new sections to config')
	add_options(parser)
	args = parser.parse_args()
	
	# add default section
	default_sec = gen_default_section(args.default_section_xml,
		args.points_list, args.config_file)
	try:
		save_section(default_sec, 'DEFAULT', args.config_file)
	except ValueError:
		print 'WARNING: %s' % traceback.format_exc()
		

	# generate building settings
	#bldg_settings = gen_sec_settings(args.bldg_xml, args.points_list)
	bldg_settings, bldg_sec_nm = gen_bldg_section(args.bldg_xml,
		args.points_list, args.config_file)
	save_section(bldg_settings, bldg_sec_nm, args.config_file)

	# add tenant section(s)
	tenant_sections, tenant_sec_names = gen_tenant_sections(args.tenant_xml,
		args.points_list, args.config_file)
	for i, section in enumerate(tenant_sections):
		save_section(section, tenant_sec_names[i], args.config_file)

	# activate new bldg/tenant(s)
	if len(bldg_settings) or len(tenant_sections):
		activate_tenants_bldg(default_sec, bldg_sec_nm,
			tenant_sec_names, args.config_file)


if __name__ == '__main__':
	main(sys.argv)
