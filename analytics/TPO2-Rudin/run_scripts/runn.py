
from optparse import OptionParser
# ag2818: removing hardcoded base dir references
import cfgparse
from common_rudin.common import setup

import sys
import os



def main(argv):

	building = None
	mode = None
	
	# ag2818: removing hardcoded base dir references
	oparser = OptionParser(usage='usage: %prog [options]',
		version='%prog 1.0', description=__doc__)
	cparser = cfgparse.ConfigParser()
	setup(oparser, cparser, 'run')
	options, args = cparser.parse(oparser, argv)
	
	configFile = os.path.join(options.base_dir, 'data_tools\config.ini')

	try:
		building = argv[1]
		mode = argv[2]
		configFile = argv[3]
		
	except:
		building == None
		mode == None

	# ag2818: removing hardcoded base dir references
	mainScript = options.base_dir
	usage = "usage:\n run.py {345_Park | 560_Lex} {startup | rampdown | trajectory} [Configuration File]"
	
	
	if mode == 'startup' or mode == 'rampdown':
		mainScript += '\\startup_rampdown'
	elif mode == 'trajectory':
		mainScript += '\\spaceTemperature_trajectory'
	else:
		print usage
		return
	
	if building == '345_Park':
		mainScript += '\\345Park\\runPark'
	elif building == '560_Lex':
		mainScript += '\\560Lex\\runLex'
	else:
		print usage
		return

	if mode == 'startup':
		mainScript += 'SU.py'
	elif mode == 'rampdown':
		mainScript += 'RD.py'
	elif mode == 'trajectory gridSearch':
		mainScript += '.py'
	else:
		print usage
		return
	
	commandLine = mainScript + ' ' + configFile + ' ' + building
	os.system(commandLine)
		
	
if __name__ == '__main__':
	main(sys.argv)