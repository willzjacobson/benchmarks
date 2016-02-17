# coding=utf-8

import sys

from crontab import CronTab

my_cron = CronTab(user='davidkarapetyan')
my_cron.remove_all()  # start afresh every time we reinstall

# set environment variables
my_cron.env['LANG'] = 'en_US.UTF-8'
my_cron.env['LC_CTYPE'] = 'en_US.UTF-8'
my_cron.env['USER'] = 'davidkarapetyan'
my_cron.env['LOGNAME'] = 'davidkarapetyan'
my_cron.env['HOME'] = '/home/davidkarapetyan'
my_cron.env['PATH'] = '/home/davidkarapetyan/anaconda3/bin:/usr/local/bin:' \
                      '/usr/bin:/bin:/usr/local/games:/usr/games'
my_cron.env['MAILTO'] = 'dkarapetyan@prescriptivedata.io'
my_cron.env['SSH_CLIENT'] = '192.168.98.146 54013 22'
my_cron.env['SSH_CONNECTION'] = '192.168.98.146 54013 192.168.98.20 22'
my_cron.env['PYTHONPATH'] = sys.prefix

weather_job = my_cron.new(
        command='python -c "import larkin; larkin.weather.run()')

master_job = my_cron.new(command='python -c "import larkin; larkin.main()')

# set time slice
master_job.setall('0 6 * * *')

my_cron.write_to_user(user='davidkarapetyan')
