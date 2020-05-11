from model.ComInterfaceFactory import ComInterfaceFactory
from model.DataPacketFactory import DataPacketFactory
from model.DataProcessingThread import DataProcessingThread
from model.ComErrorStorage import ComErrorStorage
from model.DataStorage import DataStorage
from model.GlobalConstants import GlobalConstants
from model.Data import Data
from threading import Thread


class MainController:
    INTERFACE_TYPE = 'SERIAL'

    def __init__(self):
        self.com_error_storage = ComErrorStorage()
        self.com_interface = ComInterfaceFactory.get_interface(self.INTERFACE_TYPE, self.com_error_storage)
        self.data_storage = DataStorage()
        self.stopped = False
        data = Data()
        data.complete_data = 'aa002000000000168d0499040000ffff00010000000201000003000000040081'
        data.data_payload = '0000ffff000100000002010000030000000400'
        self.data_storage.curr_data = data
        data.add_header_info('aa002000000000168d049904')
        self.data_storage.save_curr_data()
        self.curr_data = None

    def start_test(self, serial_port, baudrate):
        self.com_interface.init_connection(serial_port, int(baudrate))
        heartbeat_thread = Thread(target=self.com_interface.heartbeat_loop)
        # pass the data to the thread via the queue
        analysis_thread = DataProcessingThread(self.com_interface.read_data_queue, self.com_error_storage, self.data_storage)
        analysis_thread.attach(self.com_interface)

        analysis_thread.start()
        heartbeat_thread.start()

    def stop_test(self):
        self.stopped = True
        self.com_interface.stop()
        total_packets_received = self.data_storage.data_cnt
        self.com_error_storage.end(total_packets_received)

    def get_all_data(self):
        return self.data_storage.data_arr

    def get_heartbeat_periods(self):
        return self.com_interface.heartbeat_period_rates

    def get_ecc_check_periods(self):
        return list(GlobalConstants.ECC_CHECK_PERIODS.keys())

    def send_rest_request(self):
        counter = self.com_interface.sent_counter
        reset_packet = DataPacketFactory.get_packet('RESET', counter)
        self.com_interface.add_data_to_send_queue(reset_packet)

    def set_heartbeat_period(self, heartbeat_period):
        return self.com_interface.set_heartbeat_period(heartbeat_period)

    def set_ecc_period(self, ecc_check_period):
        return self.com_interface.set_ecc_period(ecc_check_period)

    def get_data(self, data_id):
        return self.data_storage.get_data(data_id)

    def get_com_err(self):
        return self.com_error_storage.com_error_arr

    def get_mem_err_list(self):
        mem_error_storage = self.data_storage.mem_error_storage
        return mem_error_storage.mem_error_arr

    def get_mem_err(self, index):
        mem_error_storage = self.data_storage.mem_error_storage
        return mem_error_storage.get_mem_err(index)





