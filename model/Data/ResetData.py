from model.StaticClasses.GlobalConstants import GlobalConstants
from model.StaticClasses.Time import Time


class ResetData:
    def __init__(self, type: str):
        reset_purposes = list(GlobalConstants.RESET_PURPOSES.values())
        if type in reset_purposes:
            self.type = type

        self.time_hour = Time.get_curr_time()
