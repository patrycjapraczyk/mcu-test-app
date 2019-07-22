class Calculator:
    def get_int(hexnum: str) -> int:
        """
        :param hexnum: (str) a hexdecimal number
        :return: decimal representation of hexnum (int)
        """
        HEX_BASE = 16
        return int(hexnum, HEX_BASE)

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
