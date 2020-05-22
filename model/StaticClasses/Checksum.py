import binascii


class Checksum:
    @staticmethod
    def crc32(data: int) -> int:
        checksum = binascii.crc32(data)
        return checksum
