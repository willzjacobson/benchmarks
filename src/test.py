import subprocess

import pandas as pd

import os

# for wide terminal display of pandas dataframes
pd.options.display.width = 120

# set project working directory
os.chdir( '/Users/davidkarapetyan/Documents/workspace/data_analysis/' )

# convert dynamodb table to csv
subprocess.call( 'cd /Users/davidkarapetyan/node_modules/DynamoDBtoCSV; \
node dynamoDBtoCSV.js -t WeMo > \
/Users/davidkarapetyan/Documents/workspace/data_analysis/data/WeMo.csv',
shell = True,
executable = '/bin/zsh' )


data_today = pd.read_csv( 'data/WeMo.csv' )
data_today = data_today.sort( 'name' )
average_power = data_today.current_power.mean()

data_today = data_today.loc[:, ['today_on_time', 'today_kwh', 'name']]

# convert units to hours
data_today['today_on_time'] = data_today['today_on_time'] / 3600

# rename columns
data_today.columns = ['today_total_time_on(hrs)',
                'today_energy_used (kilowatt_hrs)', 'power_shift_timestamp']

# reset index--mislabeled due to previous sort
data_today = data_today.reset_index( drop = True )

# set timestamps as index
data_today.set_index( ['power_shift_timestamp'], drop = True )

# export to json
data_today.to_json( 'data/wemo_munged.json' )
