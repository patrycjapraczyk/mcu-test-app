from model.GlobalConstants import GlobalConstants
from model.Time import Time


class ComError:
    def __init__(self, type, packet: str):
        if type in GlobalConstants.COM_ERROR_TYPES:
            self.type = type

        self.time = Time.get_curr_time_ns()
        self.packet = packet
