from threading import Thread
from queue import Queue
from GlobalConstants import GlobalConstants
from DataStorage import DataStorage
from Data import Data
from Calculator import Calculator


class DataProcessingThread(Thread):
    def __init__(self, queue: Queue):
        Thread.__init__(self)
        self.q = queue
        self.data_storage = DataStorage()
        self.curr_data_str = ""

    def run(self):
        while True:
            # If there is data to be analysed from the previous data str,
            # do not take the new data off the queue
            curr_data_item = self.data_storage.curr_data
            if len(self.curr_data_str) < GlobalConstants.AVERAGE_DATA_LEN:
                self.curr_data_str += self.q.get()

            # try to find end code if there is data that has not been finished
            if curr_data_item.data_payload:
                self.findEndIndex()
                continue

            # NEW DATA PIECE
            start_index = self.curr_data_str.find(GlobalConstants.START_CODE)
            # if start index was not found
            if start_index < -1:
                raise Exception("MISSING START CODE")

            # remove all data preceding the start code
            self.curr_data_str = self.curr_data_str[start_index:]

            # extract errors
            err = Calculator.extract(self.curr_data_str, GlobalConstants.ERR_CNT_START_INDEX,
                                     GlobalConstants.ERR_CNT_END_INDEX)
            err = Calculator.getInt(err)
            # break if there is errors on sender side
            if err > 0:
                raise Exception("ERRORS ON SENDER SIDE", err)

            # extract buffer length
            curr_data_item.buff_len = Calculator.extract(self.curr_data_str, GlobalConstants.BUF_LEN_START_INDEX,
                                                         GlobalConstants.BUF_LEN_END_INDEX)
            int_len = Calculator.getInt(curr_data_item.buff_len)
            # number of hex digits
            curr_data_item.len_of_hex = int_len * 2

            # remove all all data that has been analysed and saved already
            self.curr_data_str = self.curr_data_str[GlobalConstants.DATA_PAYLOAD_START_INDEX:]

            self.findEndIndex()

    def findEndIndex(self):
        curr_data_item = self.data_storage.curr_data
        data_length = len(self.curr_data_str)
        payload_length = len(curr_data_item.data_payload)
        curr_data_length = len(curr_data_item.data_payload) + GlobalConstants.DATA_PAYLOAD_START_INDEX
        end_code_index = curr_data_item.len_of_hex - GlobalConstants.DATA_PAYLOAD_START_INDEX - GlobalConstants.START_END_CODE_LENGTH - payload_length

        if data_length < end_code_index:
            # add currDataPayload if end index not found
            self.addDataPayload(data_length)
            return False
        else:
            expected_end_code = self.curr_data_str[
                                end_code_index: end_code_index + GlobalConstants.START_END_CODE_LENGTH]
            if expected_end_code == GlobalConstants.END_CODE:
                self.addDataPayload(end_code_index)
                self.data_storage.saveCurrData()
            # if can't find the end code within data
            else:
                raise Exception("MISSING END_CODE, expected_end_code: ", expected_end_code, "end_code index: ", end_code_index, " data_str: ", self.curr_data_str)

            return True

    def addDataPayload(self, end_index):
        curr_data_item = self.data_storage.curr_data

        curr_data_item.data_payload += self.curr_data_str[:end_index]
        curr_data_item.data_pieces_num += 1

        # remove the analysed data from curr_data_str
        self.curr_data_str = self.curr_data_str[end_index + GlobalConstants.START_END_CODE_LENGTH:]
