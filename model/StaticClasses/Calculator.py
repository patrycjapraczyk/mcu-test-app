import binascii


class Calculator:
    @staticmethod
    def get_int(hexnum: str) -> int:
        """
        :param hexnum: (str) a hexdecimal number
        :return: decimal representation of hexnum (int)
        """
        HEX_BASE = 16
        return int(hexnum, HEX_BASE)

    @staticmethod
    def get_hex(decnum: int, num_hex=8) -> str:
        """
        :param decnum: (int) a decimal number,
        :param num_hex: (int) length of hexadecimal string returned,
                        8 by default
        :return: hexdecimal representation of decnum (str)
        """
        hex_num = format(decnum, '02x')
        while len(hex_num) != num_hex:
            hex_num = "0" + hex_num
        return hex_num

    @staticmethod
    def get_bytearray(decnum: int, bytelen=0) -> bytearray:
        """
        :param decnum: (int) a decimal number,
        :return: a bytearray representation od decnum (int)
        """
        bitlen = decnum.bit_length()
        if bytelen == 0:
            bytelen = int(bitlen / 8)
            if bitlen % 8 != 0:
                bytelen += 1
            if decnum == 0:
                bytelen = 1
        bytes = decnum.to_bytes(bytelen, byteorder='big')
        byte_array = bytearray(bytes)
        return byte_array

    @staticmethod
    def get_hex_str(arr: bytearray) -> str:
        """
        returns hexadecimal str
        :param arr: bytearray
        """
        hex_representation = binascii.hexlify(arr)
        return str(hex_representation)
