class Calculator:
    def getInt(hexnum: str) -> int:
        """
        :param hexnum: (str) a hexdecimal number
        :return: decimal representation of hexnum (int)
        """
        HEX_BASE = 16
        return int(hexnum, HEX_BASE)

    def getHex(decnum: int) -> str:
        """
        :param decnum: (int) a decimal number
        :return: hexdecimal representation of decnum (str)
        """
        return format(decnum, '02x')

    def extract(data: str, start: int, end: int) -> str:
        """
        :param data: a string to be extracted
        :param start: start index of a string (int)
        :param end: end index of a string (int)
        :return: data[start : end + 1]
        """
        return data[start: end + 1]
