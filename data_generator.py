import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import datetime
import math
from time import time as T


class Time:
    def __init__(self, initial_time=None):
        if initial_time:
            self.initial_time = initial_time
        else:
            self.initial_time = datetime.datetime(2019, 1, 1)

        self.seconds_passed = 0

    @property
    def time(self):
        return self.initial_time + datetime.timedelta(seconds=self.seconds_passed)

    def incr(self, seconds=1):
        self.seconds_passed += seconds

    @property
    def weekday(self):
        return self.time.weekday()

    @property
    def day_of_month(self):
        return self.time.day

    @property
    def month(self):
        return self.time.month

    @property
    def second(self):
        return self.time.second

    @property
    def minute(self):
        return self.time.minute

    @property
    def hour(self):
        return self.time.hour

    @property
    def season(self):
        if self.month <= 3:
            return 'spring'
        elif 3 < self.month <= 6:
            return 'summer'
        elif 6 < self.month <= 9:
            return 'fall'
        elif 9 < self.month <= 12:
            return 'winter'

    @property
    def year(self):
        return self.time.year

    # ... others like day of month or minutes


class DataGenerator:
    def __init__(self):
        self.data = list()
        self.attributes = ['second', 'minute', 'hour', 'day_of_week', 'day_of_month', 'month', 'season', 'year',
                           'VM_load', 'requests_per_second', 'disk_usage']

        self.time = Time(datetime.datetime(2019, 1, 1))
        # self.time = datetime.datetime(2019, 1, 1)

    def day_of_month_usage_score(self):
        # mock
        weekday = self.time.weekday
        if weekday < 4:
            return 2
        else:
            return 3

    def minute_usage_score(self):
        pass

    def weekday_usage_score(self):
        # weekday = '{0:%a}'.format(self.time.weekday)  -> i.e. Tue
        weekday = self.time.weekday
        if weekday in (5, 6):  # if in weekends, Sat and Sun
            return 0.3
        elif weekday in (0, 1, 2):  # if in the middle of the week, Mon and Tue and Wed
            return 0.7
        elif weekday in (3, 4):  # if Thu and Fri
            return 0.5

    def hour_usage_score(self):
        hour = self.time.hour
        if 0 <= hour < 8:  # if night until morning
            return .8 + 0.6 * math.sin(math.pi / 16 * (hour + 24))
        elif 8 <= hour < 16:  # if the middle of the day
            return 0.8 + 0.2 * math.sin(math.pi / 8 * (hour - 8))
        elif 16 <= hour < 24:  # if after work time until night
            return .8 + 0.6 * math.sin(math.pi / 16 * hour)

    def month_usage_score(self):
        pass

    def season_usage_score(self):
        pass

    def year_usage_score(self):
        pass

    def psodo_random_score(self):
        # mock
        # something like Ali's algorithm
        return random.randint(-3, 3)

    def service_growth_score(self):
        pass


    # calculates a score for each measurement in each second
    # then aggregates them for each second to make a rational workload for database
    # maybe even calculate a query per second
    # the "score" needs to be rational,  no idea how :/

    def query_per_second_based_on_score(self, score):
        random_score = (random.random() - 0.5) * 2
        return score * (1 + random_score) * 1000


class Utils:
    @staticmethod
    def draw_function(func, domain_from=-20, domain_to=20):
        domain = np.arange(domain_from, domain_to, 0.05)
        result = np.arange(domain_from, domain_to, 0.05)
        for i in range(len(domain)):
            result[i] = func(domain[i])
        fig = plt.figure(1)
        plt.plot(domain, result)
        fig.show()


if __name__ == "__main__":
    pass

