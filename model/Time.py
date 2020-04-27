import time
import datetime


class Time:
    @staticmethod
    def get_curr_time_ns():
        # TODO: define which freq units suit the current usecase
        return time.time_ns()  # return the current time in nano_seconds since the Epoch

    @staticmethod
    def get_curr_time():
        return datetime.datetime.now().time()