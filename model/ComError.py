from model.GlobalConstants import GlobalConstants
import time

class ComError:
    def __init__(self, type, packet):
        if type in GlobalConstants.COM_ERROR_TYPES:
            self.type = type

        self.time = self.get_curr_time()
        self.packet = packet

    def get_curr_time(self):
        # TODO: define which freq units suit the current usecase
        return time.time_ns()  # return the current time in nano_seconds since the Epoch
