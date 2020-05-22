from unittest import TestCase
from model.Data.MemErrorData import MemErrorData


class TestMemErrorData(TestCase):
    def test_clean_data_indices(self):
        data_str = '000066660002333300033333'
        mem_error = MemErrorData(data_str)
        self.assertEqual('666633333333', mem_error.data)

    def test_extract_mem_error_id(self):
        data_str = '000000660002333300033333'
        mem_error = MemErrorData(data_str)
        self.assertEqual('0066', mem_error.mem_error_id)
        data_str = '000011000002333300033333'
        mem_error = MemErrorData(data_str)
        self.assertEqual('1100', mem_error.mem_error_id)

    def test_extract_err_cnt(self):
        data_str = '000000660001000000020033'
        mem_error = MemErrorData(data_str)
        self.assertEqual(0, mem_error.error_num)

        data_str = '000000660001000000020133'
        mem_error = MemErrorData(data_str)
        self.assertEqual(1, mem_error.error_num)

        data_str = '000000660001000100020133'
        mem_error = MemErrorData(data_str)
        self.assertEqual(257, mem_error.error_num)

        data_str = '000000660001ffff0002ff33'
        mem_error = MemErrorData(data_str)
        self.assertEqual(16777215, mem_error.error_num)

    def test_check_overflow(self):
        data_str = '000000660001ffff0002ff00'
        mem_error = MemErrorData(data_str)
        self.assertEqual(False, mem_error.overflow)

        data_str = '000000660001ffff0002ffff'
        mem_error = MemErrorData(data_str)
        self.assertEqual(True, mem_error.overflow)

    def test_extract_addresses(self):
        data_str = '000066660001ffff0002ff000003ffff0004ff'
        mem_error = MemErrorData(data_str)
        self.assertEqual(['ffffff'], mem_error.faulty_addresses)

        data_str = '000066660001ffff0002ff000003ffff0004ffee0005eeee'
        mem_error = MemErrorData(data_str)
        self.assertEqual(['ffffff', 'eeeeee'], mem_error.faulty_addresses)

        data_str = '000066660001ffff0002ff000003ffff0004ffee0005eeee00061212000712'
        mem_error = MemErrorData(data_str)
        self.assertEqual(['ffffff', 'eeeeee', '121212'], mem_error.faulty_addresses)
