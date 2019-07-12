class Calculator:
    def getInt(self, hexnum: str):
        HEX_BASE = 16
        return int(hexnum, HEX_BASE)

    def getHex(self, decnum: int):
        return format(decnum, '02x')

    def extract(self, data, start, end):
        return data[start: end + 1]