import binascii
from model.Calculator import Calculator
from model.GlobalConstants import GlobalConstants


class Checksum:
    def crc32(data) -> int:
        """
        Extracts MSG_CODE and DATA fields
        of a data packet for the established protocol
        and calculates crc32 for its values

        :param data for checksum calculation of type int or bytearray
        :raises Exception if data is not of bytearray or int type

        :return: checksum [int]
        """
        data_type = type(data)
        if not (data_type is bytearray or data_type is int):
            raise Exception('Unsupported argument data type: ' + str(data_type))

        if data_type is int:
            data = Calculator.get_bytearray(data)
        checksum = binascii.crc32(data[GlobalConstants.MSG_CODE_BYTE: len(data) - 1])
        return checksum
