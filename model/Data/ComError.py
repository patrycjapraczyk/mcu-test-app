from model.StaticClasses.GlobalConstants import GlobalConstants
from model.StaticClasses.Time import Time


class ComError:
    def __init__(self, type, packet: str, extra_data=''):
        if type in GlobalConstants.COM_ERROR_TYPES:
            self.type = type

        self.time = Time.get_curr_time_ns()
        self.time_hour = Time.get_curr_time()
        self.packet = packet
        self.extra_data = extra_data
