from queue import Queue
from threading import Thread
import threading

from Calculator import Calculator
from DataStorage import DataStorage
from GlobalConstants import GlobalConstants
from StrManipulator import StrManipulator


class DataProcessingThread(Thread):
    def __init__(self, queue: Queue):
        Thread.__init__(self)
        self._stopped = False
        self.q = queue
        self.data_storage = DataStorage()
        self.curr_data_str = ""

    def stop(self):
        self._stopped = True

    def get_start_index(self, data_str):
        return data_str.find(GlobalConstants.START_CODE)

    def run(self):
        #look for start code initially
        start_index = self.get_start_index(self.curr_data_str)
        # take another data packet off the queue if it was not found
        # and continue the search for the start code
        while start_index < 0:
            self.curr_data_str = curr_data = self.q.get()
            start_index = self.get_start_index(self.curr_data_str)

        self.curr_data_str = self.curr_data_str[start_index:]

        while not self._stopped:
            # If there is data to be analysed from the previous data str,
            # do not take the new data off the queue
            curr_data_item = self.data_storage.curr_data
            if len(self.curr_data_str) < GlobalConstants.HEADER_LEN:
                self.curr_data_str += self.q.get()


            # try to find end code if data analysis of current data has not been finished
            if curr_data_item.data_payload: #if data_payload is not empty
                self.find_end_index()
                continue

            # NEW DATA PIECE
            expected_start_code = self.curr_data_str[:GlobalConstants.START_END_CODE_LENGTH]
            # if start index was not found
            if expected_start_code != GlobalConstants.START_CODE:
                raise Exception("MISSING START CODE")

            if len(self.curr_data_str) < GlobalConstants.DATA_PAYLOAD_START_INDEX: continue

            # extract buffer length
            curr_data_item.packet_len = StrManipulator.extract(self.curr_data_str, GlobalConstants.PACKET_LEN_START_INDEX,
                                                               GlobalConstants.PACKET_LEN_END_INDEX)
            int_len = Calculator.get_int(curr_data_item.packet_len)
            # number of hex digits
            curr_data_item.len_of_hex = int_len * 2

            # extract data counter
            data_index = StrManipulator.extract(self.curr_data_str, GlobalConstants.DATA_COUNTER_START_INDEX,
                                                GlobalConstants.DATA_COUNTER_END_INDEX)

            curr_data_item.data_index = Calculator.get_int(data_index)
            curr_data_item.data_index_hex = data_index

            # remove all all data that has been analysed and saved already
            self.curr_data_str = self.curr_data_str[GlobalConstants.DATA_PAYLOAD_START_INDEX:]

            self.find_end_index()


    def find_end_index(self):
        curr_data_item = self.data_storage.curr_data
        data_length = len(self.curr_data_str)
        payload_length = len(curr_data_item.data_payload)
        end_code_index = curr_data_item.len_of_hex - GlobalConstants.DATA_PAYLOAD_START_INDEX - GlobalConstants.START_END_CODE_LENGTH - payload_length

        # if data_str is shorter than expected length
        if data_length < end_code_index:
            self.add_data_payload(data_length)
            return False
        else:
            # check if end code is placed in agreement with packet length

            expected_end_code = self.curr_data_str[
                                    end_code_index: end_code_index + GlobalConstants.START_END_CODE_LENGTH]

            if expected_end_code == GlobalConstants.END_CODE:
                self.add_data_payload(end_code_index)
                self.analyse_data_payload()
                self.check_data_index()
                self.data_storage.save_curr_data()
            # if can't find the end code within data
            else:
                raise Exception("MISSING END_CODE, expected_end_code: ", expected_end_code, "end_code index: ",
                                end_code_index, " data_str: ", self.curr_data_str)

            return True

    def add_data_payload(self, end_index):
        curr_data_item = self.data_storage.curr_data

        curr_data_item.data_payload += self.curr_data_str[:end_index]

        # remove the analysed data from curr_data_str
        self.curr_data_str = self.curr_data_str[end_index + GlobalConstants.START_END_CODE_LENGTH:]

    def analyse_data_payload(self):
        curr_data_item = self.data_storage.curr_data
        data_payload = curr_data_item.data_payload
        index_list = []
        # split the data string into chunks of length 4
        for i in range(0, len(data_payload) - GlobalConstants.DATA_BLOCK_LEN_HEX, GlobalConstants.DATA_BLOCK_LEN_HEX):
            index_list.append(data_payload[i:i + GlobalConstants.DATA_BLOCK_LEN_HEX])

        index_list = StrManipulator.remove_every_other(index_list)
        index_list = list(map(Calculator.get_int, index_list))

        # generate a sequence of numbers according to data buffer length
        # (number of data chunks)
        packet_len = Calculator.get_int(curr_data_item.packet_len)
        BYTES_PER_DATA_CHUNK = 2
        data_payload_len = packet_len - GlobalConstants.DATA_PARAMS_LEN
        num_seq_len = data_payload_len / BYTES_PER_DATA_CHUNK

        # divide by 2 because of taking into account every other num
        num_seq_len /= 2
        num_seq_len = int(num_seq_len)
        num_seq = list(range(0, num_seq_len))

        if index_list != num_seq:
            raise Exception("Indices in the list were not sorted!", index_list, "num seq: ", num_seq)

    def check_data_index(self):
        # check if curr_data.data_index == prev_data.data_index + 1
        curr_data_item = self.data_storage.curr_data
        all_data = self.data_storage.data_arr

        if len(all_data) == 0:
            return True

        prev_data_item = all_data[-1]
        curr_index = curr_data_item.data_index
        prev_index = prev_data_item.data_index

        if prev_index != GlobalConstants.MAX_DATA_INDEX:
            if curr_index != prev_index + 1:
                raise Exception("Unexpected data index! Prev index:", prev_index, prev_data_item.data_index_hex , "curr data: ",
                                curr_data_item.data_index, curr_data_item.data_index_hex ,
                                "curr data string: ", self.curr_data_str,
                                "queue ", self.q.queue)
        else:
            if curr_index == 0:
                raise Exception("Unexpected data index! Prev index:", prev_index, prev_data_item.data_index_hex,
                                "curr data: ",
                                curr_data_item.data_index, curr_data_item.data_index_hex ,
                                "curr data string: ", self.curr_data_str,
                                "queue ", self.q.queue)
