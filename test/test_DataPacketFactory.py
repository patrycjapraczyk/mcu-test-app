from unittest import TestCase
from model.StaticClasses.DataPacketFactory import DataPacketFactory


class TestDataPacketFactory(TestCase):

    def test_append_len(self):
        data_packet = DataPacketFactory.get_packet('RESET', 0)
        #expected length 13

    def test_append_checksum(self):
        self.fail()

    def test_append_data(self):
        self.fail()
