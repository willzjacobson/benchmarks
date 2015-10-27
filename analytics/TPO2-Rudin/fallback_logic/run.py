import fallback_logic.failover as failover

configFile = 'config_master.py'
failover.fall_back(configFile, '345', 'startup')
failover.fall_back(configFile, '345', 'rampdown')

failover.fall_back(configFile, '560', 'startup')
failover.fall_back(configFile, '560', 'rampdown')

failover.fall_back(configFile, '1BP', 'startup')
failover.fall_back(configFile, '1BP', 'rampdown')

failover.fall_back(configFile, '4E5', 'startup')
failover.fall_back(configFile, '4E5', 'rampdown')