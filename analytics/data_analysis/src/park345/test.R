# TODO: Add comment
# 
# Author: davidkarapetyan
###############################################################################


library("forecast")
library("plyr")
library("zoo")
setwd("/Users/davidkarapetyan/Documents/workspace/data_analysis")
data = read.csv('data/wemo.csv', stringsAsFactors = FALSE)


#ditch some entries
data = data[c('name', 'today_kwh')]

#rename columns

colnames(data) = c('timestamp', 'energy_used_kw_hrs')
data = arrange(data, timestamp)
data_zoo = zoo(data$energy_used_kw_hrs,
		order.by=data$timestamp
)