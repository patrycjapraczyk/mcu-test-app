from queue import Queue
from unittest import TestCase

from model.Data.Data import Data
from model.DataProcessingThread import DataProcessingThread


class TestDataProcessingThread(TestCase):
    # def test_run_correct(self):
    #     data_num = 10
    #     q = self.get_correct_queue(data_num)
    #     data_processing_thread = DataProcessingThread(q)
    #     data_processing_thread.start()
    #     data_arr = data_processing_thread.data_storage.data_arr
    #
    #     time.sleep(3)
    #
    #     #compare the analysed data saved into data_storage
    #     #to the data that have been formerly generated
    #     for i in range(0, data_num):
    #         correct_data = self.get_correct_data(i)[1]
    #         curr_data = data_arr[i]
    #
    #         self.assertEqual(correct_data.data_payload, curr_data.data_payload)
    #         self.assertEqual(correct_data.packet_len, curr_data.packet_len)
    #
    #     data_processing_thread.stop()

    # def test_run_correct_partition(self):
    #     q = Queue()
    #     data_processing_thread = DataProcessingThread(q)
    #     data_arr = data_processing_thread.data_storage.data_arr
    #
    #     part1 = True
    #     data_index = 0
    #     for i in range(1, 10):
    #         correct_data = self.get_correct_data(data_index)[0]
    #         half_data_point = int(len(correct_data) / 2)
    #         correct_data = correct_data[:half_data_point] if part1 else correct_data[half_data_point:]
    #         part1 = not part1
    #         if not part1:
    #             data_index += 1
    #         q.put(correct_data)
    #
    #     data_processing_thread.start()
    #     time.sleep(3)
    #
    #     for i in range(1, 4):
    #         correct_data = self.get_correct_data(i)[1]
    #         curr_data = data_arr[i]
    #         self.assertEqual(correct_data.data_payload, curr_data.data_payload)
    #         self.assertEqual(correct_data.packet_len, curr_data.packet_len)

    # def test_no_start_index(self):
    #     q = Queue()
    #     q.put("276357826")
    #     q.put(self.get_correct_data(0)[0])
    #     q.put("4333")
    #     data_processing_thread = DataProcessingThread(q)
    #
    #     self.assertRaises(Exception, data_processing_thread.run)
    #
    # def test_missing_end_code(self):
    #     correct_data_str = self.get_correct_data()[0]
    #     correct_data_str = correct_data_str.replace("81", "22")  # replace end index with some random string
    #     q = Queue()
    #     q.put(correct_data_str)
    #     data_processing_thread = DataProcessingThread(q)
    #
    #     self.assertRaises(Exception, data_processing_thread.run)

    # def test_incorrect_buffer_len(self):
    #     def exec_incorrect_packet_len(packet_len):
    #         correct_data_str = self.get_correct_data()[0]
    #         no_packet_len = correct_data_str[GlobalConstants.PACKET_LEN_END_INDEX + 1:]
    #         data_str = GlobalConstants.START_CODE + packet_len + no_packet_len
    #         q = Queue()
    #         q.put(data_str)
    #         data_processing_thread = DataProcessingThread(q)
    #         data_processing_thread.run()
    #
    #     self.assertRaises(Exception, exec_incorrect_packet_len, "0017")
    #     self.assertRaises(Exception, exec_incorrect_packet_len, "0015")

    def test_check_data_index(self):
        header = 'aa' \
                 '0019' \
                 '00000000' \
                 '00000000' \
                 '01'
        unordered_payload = '000066660002333300033333'
        data = Data()
        data.add_header_info(header)
        data.data_payload = unordered_payload
        data_processing_thread = DataProcessingThread(Queue())

        self.assertFalse(data_processing_thread.analyse_data_payload(data))

        unordered_payload = '000066660000333300033333'
        data.data_payload = unordered_payload
        self.assertFalse(data_processing_thread.analyse_data_payload(data))

        ordered_payload = '000066660001333300023333'
        data.data_payload = ordered_payload

        self.assertTrue(data_processing_thread.analyse_data_payload(data))

    # def test_ordered_data(self):
    #     index1 = 35
    #     index2 = 36
    #     data1 = self.get_correct_data(index1)
    #     data2 = self.get_correct_data(index2)
    #
    #     q = Queue()
    #     q.put(data1[0])
    #     q.put(data2[0])
    #
    #     data_processing_thread = DataProcessingThread(q)
    #     data_processing_thread.start()
    #
    #     time.sleep(2)
    #
    #     data_storage = data_processing_thread.data_storage
    #     self.assertEqual(data1[1].data_payload, data_storage.data_arr[0].data_payload)
    #     self.assertEqual(index1, data_storage.data_arr[0].data_index)
    #
    #     self.assertEqual(data1[1].data_payload, data_storage.data_arr[1].data_payload)
    #     self.assertEqual(index2, data_storage.data_arr[1].data_index)

    # def test_unordered_data(self):
    #     index1 = 34
    #     index2 = 36
    #     data1 = self.get_correct_data(index1)
    #     data2 = self.get_correct_data(index2)
    #
    #     q = Queue()
    #     q.put(data1[0])
    #     q.put(data2[0])
    #
    #     data_processing_thread = DataProcessingThread(q)
    #
    #     self.assertRaises(Exception, data_processing_thread.run)
    #
    # def get_correct_data(self, data_cnt=0):
    #     packet_len = '0015'
    #     data_cnt = Calculator.get_hex(data_cnt, 8)
    #     checksum = '00006666'
    #     msg_code = '01'
    #
    #     data_payload = "0000333300013333"
    #     correct_str = GlobalConstants.START_CODE + packet_len + data_cnt + checksum + msg_code + data_payload + GlobalConstants.END_CODE
    #     return correct_str, Data(data_payload, packet_len)

    # def get_correct_queue(self, num=10) -> None:
    #     q = Queue()
    #     for i in range(0, num):
    #         q.put(self.get_correct_data(i)[0])
    #     return q

    # def missing_start_code(self):
    #     return
