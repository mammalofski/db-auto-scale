import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import datetime
import math
import logging
from time import time as T
from constants import *


class Time:
    def __init__(self, initial_time=datetime.datetime(2019, 1, 1)):
        self.initial_time = initial_time
        self.seconds_passed = 0

    @property
    def time(self):
        return self.initial_time + datetime.timedelta(seconds=self.seconds_passed)

    def live(self, seconds=1):
        # pass the time: live
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
            return Seasons.SPRING
        elif 3 < self.month <= 6:
            return Seasons.SUMMER
        elif 6 < self.month <= 9:
            return Seasons.FALL
        elif 9 < self.month <= 12:
            return Seasons.WINTER

    @property
    def year(self):
        return self.time.year

    @property
    def day_of_year(self):
        first_day_of_year = datetime.datetime(self.year, 1, 1)
        timedelta = self.time - first_day_of_year
        return timedelta.days

    # ... others like day of month or minutes


class DataGenerator:
    GENERATE_CHUNK_NO = 24 * 3600  # every 24 hours

    def __init__(self, duration, export=False, initial_time=None):
        self._temp_data = list()
        self.export = export
        self.attributes = [
            'seconds_passed', 'second', 'minute', 'hour', 'day_of_week', 'day_of_month', 'month', 'season', 'year', 'VM_load',
            'requests_per_second', 'disk_usage',
        ]
        self.score_calculator_methods = [
            'day_of_month_usage_score', 'weekday_usage_score', 'hour_usage_score', 'season_usage_score',
            'pseudo_random_score', 'service_growth_score'
        ]
        self.score_method_impact_factor = {
            'day_of_month_usage_score': 1,
            'weekday_usage_score': 1.3,
            'hour_usage_score': 3,
            'season_usage_score': .7,
            'pseudo_random_score': 1,
            'service_growth_score': 2.5
        }
        # create an empty dataframe
        self._data_frame = pd.DataFrame(columns=self.attributes)
        if not initial_time:
            self.time = Time(datetime.datetime(2019, 1, 1))
        else:
            self.time = Time(initial_time)
        # self.time = datetime.datetime(2019, 1, 1)
        self.duration = duration
        self.whole_period = self.duration * 24 * 3600  # in seconds

        self.total_queries = 0

    @property
    def data(self):
        return self._temp_data

    @property
    def data_frame(self):
        self._update_data_frame()
        return self._data_frame

    def _update_data_frame(self):
        if not len(self._temp_data):
            return
        print('flushing data into dataframe')
        new_df = pd.DataFrame(self._temp_data, columns=self.attributes)
        self._data_frame = self._data_frame.append(new_df)
        # flush the data
        del self._temp_data
        self._temp_data = list()

    def day_of_month_usage_score(self):
        day = self.time.day_of_month
        if day < 7:
            return -0.4 / 7 * day + 0.7
        elif 7 <= day < 20:
            return 0.2 / 13 * (day - 7) + 0.3
        elif 20 <= day:
            return 0.3 / 10 * (day - 20) + 0.5

    def weekday_usage_score(self):
        # weekday = '{0:%a}'.format(self.time.weekday)  -> i.e. Tue
        weekday = self.time.weekday
        if weekday in (5, 6):  # if in weekends, Sat and Sun
            return 0.3
        elif weekday in (0, 1, 2):  # if in the middle of the week, Mon and Tue and Wed
            return 0.7
        elif weekday in (3, 4):  # if Thu and Fri
            return 0.5
        else:
            return 0

    def hour_usage_score(self):
        """
        usage increases between 0 and 8,
        reaches its peek between 8 and 16,
        and decreases between 16 and 24
        """
        hour = self.time.hour
        minute_percentage = self.time.minute / 60.0
        x = hour + minute_percentage
        if 0 <= hour < 8:  # if night until morning
            return .8 + .6 * math.sin(math.pi / 16 * (x + 24))
        elif 8 <= hour < 16:  # if the middle of the day
            return .8 + .2 * math.sin(math.pi / 8 * (x - 8))
        elif 16 <= hour < 24:  # if after work time until night
            return .8 + .6 * math.sin(math.pi / 16 * x)
        else:
            return 0

    def month_usage_score(self):
        pass

    def season_usage_score(self):
        if self.time.season == Seasons.SPRING:
            return 0.5
        elif self.time.season == Seasons.SUMMER:
            return 0.3
        elif self.time.season == Seasons.FALL:
            return 0.3
        elif self.time.season == Seasons.WINTER:
            return 0.4
        else:
            return 0

    def year_usage_score(self):
        pass

    def pseudo_random_score(self):
        # throttle_top = 0.7
        # throttle_bottom = 0.2
        # growth_dir = 'up'
        # current_value = 0.2
        # TODO: generate something meaningful, like going up and down based on a period of time
        return random.random()

    def service_growth_score(self):
        """
        a linear growth from 0 to 1 through the year
        """
        day_of_year = self.time.day_of_year
        return day_of_year / 365.0


    # calculates a score for each measurement in each second
    # then aggregates them for each second to make a rational workload for database
    # maybe even calculate a query per second
    # the "score" needs to be rational,  no idea how :/

    def query_per_second_based_on_score(self, score):
        random_score = random.triangular(-1, 1, 2)
        return score * (1 + random_score) * 1000

    def add_row(self, row):
        # TODO: validate the row  # not that much needed
        self._temp_data.append(row)

    def new_row(self, score):
        t = self.time  # making it shorter :D
        return [
            t.seconds_passed, t.second, t.minute, t.hour, t.weekday, t.day_of_month, t.month, t.season, t.year,
            self.score_to_VMLoad(score), self.query_per_second_based_on_score(score), self.total_queries_to_db_size()
        ]

    def score_to_VMLoad(self, score):
        # TODO: convert score to vm load
        return score

    def total_queries_to_db_size(self):
        """
        half of the queries are db write, and each occupy 10 KB of space
        :return total_queries / 2 * 10 (KB):
        """
        return self.total_queries * 5

    def get_score(self):
        score = 0
        for method_name in self.score_calculator_methods:
            method = getattr(self, method_name)
            score += method() * self.score_method_impact_factor.get(method_name, 1)
        self.total_queries += self.query_per_second_based_on_score(score)
        return score

    def export_csv(self):
        # TODO: also include the headers
        t = T()
        self.data_frame.to_csv('data.csv')
        print('export time', T() - t)

    def generate_data(self):

        t = T()
        current_chunk = 0
        try:  # a try block, to export the data generated so far, in case of emergency exit
            while self.GENERATE_CHUNK_NO * (current_chunk + 1) <= self.whole_period:
                self.generate_chunk_of_data()
                self._update_data_frame()  # this method flushes temp data and imports it into the dataframe
                current_chunk += 1
        finally:
            if self.export:
                self.export_csv()

    def generate_chunk_of_data(self):
        for second in range(self.GENERATE_CHUNK_NO):
            score = self.get_score()  # calculate score based on current time
            row = self.new_row(score)  # generate a new row of data
            self.add_row(row)
            # just some logs, every 10 hours
            if second % 36000 == 0:
                print('progress', self.time.seconds_passed / float(self.whole_period) * 100)
                x = T() - t
                print('time passed', int(x / 60), 'minutes and', int(x % 60), 'seconds')
            self.time.live()  # pass the time (go ahead for one second)


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
    t = T()
    logging.basicConfig(filename='log.log')
    die = DataGenerator(365, export=True)
    die.generate_data()
    x = T() - t
    print('Finished in', int(x / 60), 'minutes and', x % 60, 'seconds')


