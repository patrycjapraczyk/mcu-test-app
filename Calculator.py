class Calculator:
    def get_int(hexnum: str) -> int:
        """
        :param hexnum: (str) a hexdecimal number
        :return: decimal representation of hexnum (int)
        """
        HEX_BASE = 16
        return int(hexnum, HEX_BASE)

    def get_hex(decnum: int) -> str:
        """
        :param decnum: (int) a decimal number
        :return: hexdecimal representation of decnum (str)
        """
        return format(decnum, '02x')