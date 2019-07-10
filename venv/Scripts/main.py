import socket

HOST = '192.168.1.100'
PORT = 7771

START_CODE = 'aa'
END_CODE = '81'

BUF_LEN_START_INDEX = 2
BUF_LEN_END_INDEX = 5
TCP_LEN_START_INDEX = 6
TCP_LEN_END_INDEX = 13
ACQ1_LEN_START_INDEX = 14
ACQ1_LEN_END_INDEX = 17
ACQ2_LEN_START_INDEX = 18
ACQ2_LEN_END_INDEX = 21
ERR_CNT_START_INDEX = 22
ERR_CNT_END_INDEX = 25

DATA_PAYLOAD_START_INDEX = 26

START_END_CODE_LENGTH = 2

data_payload = ""
data = ""
start_index = -1
end_index = -1
len_of_hex = -1

data_arr = []


def checkStartMessage(data):
    start = data[0: 2]
    return start == START_CODE


def extract(data, start, end=len(data)):
    return data[start: end + 1]


def getInt(num):
    HEX_BASE = 16
    return int(num, HEX_BASE)


def getHex(num):
    return format(num, '02x')


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" % (err))

# connecting to the server
s.connect((HOST, PORT))


def exec():
    while True:
        data, addr = s.recvfrom(512)  # buffer size is 512 bytes
        data = data.hex()
        #
        if data_payload:
            if not findEndIndex(): continue

        start_index = data.find(START_CODE)
        # stop if there is errors
        err_cnt = extract(data, start_index + ERR_CNT_START_INDEX, start_index + ERR_CNT_END_INDEX)
        if (getInt(err_cnt) > 0):
            raise Exception('ERRORS OCCURED!')

        buffer_len = extract(data, start_index + BUF_LEN_START_INDEX, start_index + BUF_LEN_END_INDEX)
        int_len = getInt(buffer_len)
        len_of_hex = int_len * 2 - START_END_CODE_LENGTH

        findEndIndex()

def findEndIndex():
    end_index = data.find(END_CODE)
    if end_index < 0:
        data_payload += data
        return false
    else:
        while end_index - start_index < len_of_hex:
            end_index = data.find(END_CODE, end_index + 1)

        # if can't find end code within data length
        if (end_index - start_index > len_of_hex):
            raise Exception('MISSING END_CODE!')

        if start_index > 0:
            data_payload += extract(data, start_index + DATA_PAYLOAD_START_INDEX, end_index)
            data_arr.append(data_payload)
            data_payload = ""
            return true

exec()


# def getEndCode():
#     end_index = data.find(END_CODE)
#     if end_index < 0:
#         curr_data += data
#     else:
#         while (end_index - start_index != len_of_hex or end_index - start_index < len_of_hex):
#             end_index = data.find(END_CODE, end_index + 1)
#
#             # if can't find end code within data length
#         if (end_index - start_index < len_of_hex):
#             return false
#
#
# def execAll():
#     while True:
#         data, addr = s.recvfrom(512)  # buffer size is 512 bytes
#         data = data.hex()
#
#         # find AA - start code
#         start_index = data.find("aa")
#
#         # stop if there is errors
#         err_cnt = extract(data, start_index + ERR_CNT_START_INDEX, start_index + ERR_CNT_END_INDEX)
#         if (getInt(err_cnt) > 0):
#             break
#
#         # data buffer length in bytes
#         buffer_len = extract(data, start_index + BUF_LEN_START_INDEX, start_index + BUF_LEN_END_INDEX)
#         int_len = getInt(buffer_len)
#
#         # find 81 - end code
#         end_index = data.find("81")
#
#         # if no end_index in data chunk
#         if (end_index < 0):
#             prev_data = extract(data, start_index + DATA_PAYLOAD_START_INDEX)
#
#         # length of characters in hex representation
#         len_of_hex = int_len * 2 - START_END_CODE_LENGTH
#
#         while (end_index - start_index != len_of_hex or end_index - start_index < len_of_hex):
#             end_index = data.find("81", end_index + 1)
#
#         # if can't find end code within data length
#         if (end_index - start_index < len_of_hex):
#             continue
#
#         data_payload += extract(data, start_index + DATA_PAYLOAD_START_INDEX, end_index)
#         data_arr.append(data_payload)

