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
        self.curr_data_str = self.q.get()
        while True:
            #OLD DATA PIECE
            curr_data_item = self.data_storage.curr_data
            if not self.curr_data_str :
                self.curr_data_str = self.q.get()
            if curr_data_item.data_payload:
                if not self.findEndIndex():
                    continue

            #NEW DATA PIECE
            curr_data_item.start_index = self.curr_data_str.find(GlobalConstants.START_CODE)
            #if start index was not found
            if curr_data_item.start_index < -1: continue
            #extract errors
            err = calculator.extract(data, curr_data_item.start_index + GlobalConstants.ERR_CNT_START_CODE, curr_data_item.start_index + GlobalConstants.ERR_CNT_END_CODE)
            err = calculator.getInt(err)
            #break if there is errors on sender side
            if err > 0:
                raise Exception("ERRORS ON SENDER SIDE", err)
            #extract buffer length
            curr_data_item.buff_len = calculator.extract(data, curr_data_item.start_index + GlobalConstants.BUF_LEN_START_INDEX,  curr_data_item.start_index + GlobalConstants.BUF_LEN_END_INDEX)
            int_len = calculator.getInt(curr_data_item.buff_len)
            curr_data_item.len_of_hex = int_len * 2 - GlobalConstants.START_END_CODE_LENGTH


    def findEndIndex(self):
        curr_data_item = data_storage.curr_data_item
        end_index = self.curr_data_str.find(GlobalConstants.END_CODE)
        if end_index < 0:
            #TODO: add currDataPayload
            return False
        else:
            while curr_data_item.start_end_distance < curr_data_item.len_of_hex:
                old_end_index = end_index
                end_index = self.curr_data_str.find(GlobalConstants.END_CODE)
                curr_data_item.start_end_distance += end_index - old_end_index

            #if can't find the end code within data
            if curr_data_item.start_end_distance > curr_data_item.len_of_hex:
                raise Exception("MISSING END_CODE, curr_data: ", curr_data_item.to_str())

            if curr_data_item.start_index >= 0:
                curr_data_item.end_index = end_index
                #TODO: find the right start index
                #curr_data_item.data_payload += calculator.extract(curr_data_item, start?, end_index + 1)
                dataStorage.saveCurrData()

            return True

