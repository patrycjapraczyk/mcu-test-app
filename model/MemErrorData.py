from model.Data import Data
from model.StrManipulator import StrManipulator
from model.GlobalConstants import GlobalConstants
from model.Calculator import Calculator
from model.StrManipulator import StrManipulator
from model.Time import Time


class MemErrorData:
    def __init__(self, data: str, index: int):
        self.data = data
        self.faulty_addresses = []
        self.time = Time.get_curr_time()
        self.mem_error_id = 0
        self.error_num = 0
        self.overflow = False
        self.index = index

        self.clean_data_indices()
        self.extract_mem_error_id()
        self.extract_err_cnt()
        self.check_overflow()
        self.extract_addresses()

    def clean_data_indices(self):
        data = StrManipulator.split_string(self.data, GlobalConstants.PAYLOAD_INDICES_LEN)
        data = StrManipulator.remove_every_other(data, True)
        data = StrManipulator.list_into_str(data)
        self.data = data

    def extract_mem_error_id(self):
        id = StrManipulator.substring(self.data, GlobalConstants.MEM_ERROR_INDEX_START, GlobalConstants.MEM_ERROR_INDEX_END)
        self.mem_error_id = id

    def extract_err_cnt(self):
        cnt = StrManipulator.substring(self.data, GlobalConstants.ERROR_CNT_START, GlobalConstants.ERROR_CNT_END)
        cnt = Calculator.get_int(cnt)
        self.error_num = cnt

    def check_overflow(self):
        overflow = StrManipulator.substring(self.data, GlobalConstants.OVERFLOW_START, GlobalConstants.OVERFLOW_END)
        if overflow != '00':
            self.overflow = True

    def extract_addresses(self):
        self.faulty_addresses = self.data[GlobalConstants.MEM_ADDRESSES_START::]
        self.faulty_addresses = StrManipulator.split_string(self.faulty_addresses, GlobalConstants.MEM_ADDRESSES_LEN)





