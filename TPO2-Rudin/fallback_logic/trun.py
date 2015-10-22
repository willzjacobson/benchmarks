import fallback_logic.tfailover as failover
import datetime

date_str = str(datetime.datetime.now())[0:19]
date_str = date_str.replace(' ', '_')
date_str = date_str.replace(':', '-')

file = open(date_str+"_log.txt", 'w')

configFile = 'config.ini'
failover.fall_back(configFile, '345_Park', 'startup', file)
failover.fall_back(configFile, '345_Park', 'rampdown', file)

failover.fall_back(configFile, '560_Lex', 'startup', file)
failover.fall_back(configFile, '560_Lex', 'rampdown', file)

failover.fall_back(configFile, '1BP', 'startup', file)
failover.fall_back(configFile, '1BP', 'rampdown', file)

failover.fall_back(configFile, '40E52', 'startup', file)
failover.fall_back(configFile, '40E52', 'rampdown', file)

file.close()