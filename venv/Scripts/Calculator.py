class Calculator:
    #
    def getInt(hexnum: str) -> int:
        """
        :parameter: hexnum (str) 
        :return: hexnum converted to int
        """
        HEX_BASE = 16
        return int(hexnum, HEX_BASE)

    def getHex(decnum: int) -> str:
        return format(decnum, '02x')

    def extract(data: str, start: int, end: int) -> str:
        return data[start: end + 1]