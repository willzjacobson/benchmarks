# coding=utf-8
# import time

# import schedule

import nikral.benchmarks.electric.run_benchmark as erb
import nikral.benchmarks.steam.run_benchmark as srb
import nikral.benchmarks.water.run_benchmark
import nikral.weather.run as wr


def weather_update_job():
    print("Updating weather DB")
    wr.main()
    print("Done")


def benchmark_run_job():

    print("Running electricity benchmark")
    erb.main()

    print("Now running steam benchmark")
    srb.main()

    print("running water benchmark")
    nikral.benchmarks.water.run_benchmark.main()

    print("Done")
    # print("Going to sleep now for an hour")


def main():
    # for debugging. Delete later
    # weather_update_job()
    benchmark_run_job()
    # print("Scheduling the new jobs")
    # schedule.every().hour.do(weather_update_job)
    # schedule.every().hour.do(benchmark_run_job)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == '__main__':
    main()
