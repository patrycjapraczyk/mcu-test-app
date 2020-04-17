from unittest import TestCase
from model.Checksum import Checksum
from model.Calculator import Calculator


class TestChecksum(TestCase):
    def test_get_checksum_unsupported_type(self):
        with self.assertRaises(Exception):
            Checksum.crc32('jelwrhkl')

    #TODO adjust test cases so that they match the packet

    # def test_get_checksum_int(self):
    #     self.assertEqual(732146036, Checksum.crc32(12345))
    #     self.assertEqual(4280040127, Checksum.crc32(912892082018202880218))
    #     self.assertEqual(3523407757, Checksum.crc32(0))


    # def test_get_checksum_bytearray(self):
    #     self.assertEqual(732146036, Checksum.crc32(Calculator.get_bytearray(12345)))
    #     self.assertEqual(4280040127, Checksum.crc32(Calculator.get_bytearray(91289208201820288021)))
    #     self.assertEqual(3523407757, Checksum.crc32(Calculator.get_bytearray(0)))
