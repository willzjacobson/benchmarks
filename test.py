import subprocess

import pandas as pd

import os

# for wide terminal display of pandas dataframes
pd.options.display.width = 120

#set project working directory
os.chdir( '/Users/davidkarapetyan/Documents/workspace/data_analysis/' )

#convert dynamodb table to csv
subprocess.call( 'cd /Users/davidkarapetyan/node_modules/DynamoDBtoCSV; \
node dynamoDBtoCSV.js -t WeMo > \
/Users/davidkarapetyan/Documents/workspace/data_analysis/data/WeMo.csv',
shell = True,
executable = '/bin/zsh' )


data = pd.read_csv( 'data/WeMo.csv' )