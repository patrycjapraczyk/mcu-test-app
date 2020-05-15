from queue import Queue
from threading import Thread

from model.Calculator import Calculator
from model.DataStorage import DataStorage
from model.Data import Data
from model.GlobalConstants import GlobalConstants
from model.StrManipulator import StrManipulator
from model.Checksum import Checksum
from model.ComErrorStorage import ComErrorStorage
from model.ComError import ComError

from model.Observer.Observer import Observer
from model.Observer.Subject import Subject


class DataProcessingThread(Thread, Subject):
    def __init__(self, queue: Queue, com_error_storage: ComErrorStorage, data_storage: DataStorage):
        Thread.__init__(self)
        self._stopped = False
        self.q = queue
        self.data_storage = data_storage
        self.com_error_storage = com_error_storage
        self.curr_data_str = ""
        self.heartbeat_received_id = ''

    def notify(self) -> None:
        self._observer.update(self)

    def detach(self) -> None:
        self._observer = None

    def attach(self, observer: Observer) -> None:
        self._observer = observer

    def stop(self):
        self._stopped = True

    def get_start_index(self, data_str):
        return data_str.find(GlobalConstants.START_CODE)

    def run(self):
        #look for start code initially
        start_index = self.get_start_index(self.curr_data_str)
        # take another data packet off the queue if it was not found
        # and continue the search for the start code
        if start_index < 0:
            self.curr_data_str = self.q.get()
            start_index = self.get_start_index(self.curr_data_str)

        self.curr_data_str = self.curr_data_str[start_index:]

        while not self._stopped:
            # If there is data to be analysed from the previous data str,
            # do not take the new data off the queue
            curr_data_item = self.data_storage.curr_data

            if curr_data_item.data_payload == '':
                while len(self.curr_data_str) < GlobalConstants.HEADER_LEN:
                    new_data = self.q.get()
                    self.curr_data_str += new_data

            while curr_data_item.data_payload != '':
                new_data = self.q.get()
                if new_data != '':
                    self.curr_data_str += new_data
                    break

            # try to find end code if data analysis of current data has not been finished
            if curr_data_item.data_payload: #if data_payload is not empty
                self.find_end_index()
                continue

            # NEW DATA PIECE
            expected_start_code = self.curr_data_str[:GlobalConstants.START_END_CODE_LENGTH]
            # if start index was not found
            if expected_start_code != GlobalConstants.START_CODE:
                com_error = ComError('MISSING START CODE', self.curr_data_str)
                self.com_error_storage.add_error(com_error, self.data_storage.data_cnt)
                continue

            if len(self.curr_data_str) < GlobalConstants.DATA_PAYLOAD_START_INDEX: continue

            header_str = self.curr_data_str[:GlobalConstants.DATA_PAYLOAD_START_INDEX]
            self.data_storage.curr_data.add_header_info(header_str)

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
                # perform data analysis functions and save data
                self.add_data_payload(end_code_index)
                if not self.analyse_data_payload(curr_data_item):
                    return False
                if not self.check_data_index():
                    return False
                if not self.verify_checksum(curr_data_item):
                    return False
                self.check_heartbeat(curr_data_item)
                self.data_storage.save_curr_data()
            # if can't find the end code within data
            else:
                com_error = ComError('MISSING END CODE', self.curr_data_str)
                self.com_error_storage.add_error(com_error, self.data_storage.data_cnt)

            return True

    def check_heartbeat(self, curr_data_item: Data):
        HEARTBEAT_RESPONSE_CODE = 0x01
        if curr_data_item.msg_code == HEARTBEAT_RESPONSE_CODE:
            #TODO: move data extraction into a data packet
            heartbeat = StrManipulator.split_string(curr_data_item.data_payload, GlobalConstants.PAYLOAD_INDICES_LEN)
            heartbeat = StrManipulator.remove_every_other(heartbeat, True)
            heartbeat = StrManipulator.list_into_str(heartbeat)
            heartbeat = Calculator.get_int(heartbeat)
            
            self.heartbeat_received_id = heartbeat
            self.notify()

    def add_data_payload(self, end_index):
        curr_data_item = self.data_storage.curr_data

        payload = self.curr_data_str[:end_index]
        curr_data_item.data_payload += payload
        curr_data_item.complete_data += payload

        # remove the analysed data from curr_data_str
        self.curr_data_str = self.curr_data_str[end_index + GlobalConstants.START_END_CODE_LENGTH:]

    def analyse_data_payload(self, curr_data_item):
        data_payload = curr_data_item.data_payload

        # split the data string into chunks of length 4
        index_list = StrManipulator.split_string(data_payload, GlobalConstants.PAYLOAD_INDICES_LEN)
        if not index_list:
            return True

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
            com_error = ComError('UNORDERED DATA CONTENT', self.data_storage.curr_data.complete_data)
            self.com_error_storage.add_error(com_error, self.data_storage.data_cnt)
            return False

        return True

    def check_data_index(self):
        # check if curr_data.data_index == prev_data.data_index + 1
        curr_data_item = self.data_storage.curr_data
        prev_data_item = self.data_storage.prev_data

        if not prev_data_item:
            return True

        curr_index = curr_data_item.data_index
        prev_index = prev_data_item.data_index

        max_index = GlobalConstants.MAX_DATA_INDEX

        if prev_index != GlobalConstants.MAX_DATA_INDEX:
            if curr_index != prev_index + 1:
                com_error = ComError('UNORDERED DATA_CNT', self.data_storage.curr_data.complete_data, extra_data=' prev data_index: '+str(prev_index) +
                                                                                                                 ', curr data index: ' + str(curr_index) + '\n')
                self.com_error_storage.add_error(com_error, self.data_storage.data_cnt)
                return False
        else:
            if curr_index != 0:
                com_error = ComError('UNORDERED DATA_CNT', self.data_storage.curr_data.complete_data, extra_data=' prev data_index: '+str(prev_index) + ''
                                                                                                                                                        ', curr data index: ' + str(curr_index) + '\n')
                self.com_error_storage.add_error(com_error, self.data_storage.data_cnt)
                return False
        return True

    def verify_checksum(self, data: Data):
        data_type = '0' + str(data.msg_code)
        data_for_checksum = data_type + data.data_payload
        byte_len = int(len(data_for_checksum) / GlobalConstants.HEX_DIGITS_PER_BYTE)
        dec_num = Calculator.get_int(data_for_checksum)
        data_int = Calculator.get_bytearray(dec_num, byte_len)
        expected_checksum = Checksum.crc32(data_int)
        return data.checksum == expected_checksum

