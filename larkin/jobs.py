# coding=utf-8
import time

import schedule

import larkin.benchmarks.electric.run_benchmark as erb
import larkin.benchmarks.steam.run_benchmark as srb
import larkin.weather.run as wr


def weather_update_job():
    wr.main()


def benchmark_run_job():
    erb.main()
    srb.main()


schedule.every().hour.do(weather_update_job)
schedule.every().hour.do(benchmark_run_job)

while True:
    schedule.run_pending()
    time.sleep(1)
