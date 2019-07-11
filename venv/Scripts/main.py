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
err_cnt = 0
len_of_hex= 0

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
    global err_cnt, start_index, data_payload, end_index, len_of_hex, data_arr, data, len_of_hex
    while True:
        data, addr = s.recvfrom(512)  # buffer size is 512 bytes
        data = data.hex()
        # if there is some data payload left from the previous iteration
        if data_payload:
            if not findEndIndex(): continue
        start_index = data.find(START_CODE)
        # continue if start_code was not found
        if start_index < -1 : continue
        # break if there is errors
        err_cnt = extract(data, start_index + ERR_CNT_START_INDEX, start_index + ERR_CNT_END_INDEX)
        if (getInt(err_cnt) > 0):
            raise Exception('ERRORS OCCURED! ', err_cnt)

        buffer_len = extract(data, start_index + BUF_LEN_START_INDEX, start_index + BUF_LEN_END_INDEX)
        int_len = getInt(buffer_len)
        len_of_hex = int_len * 2 - START_END_CODE_LENGTH

        findEndIndex()

def findEndIndex():
    global err_cnt, start_index, data_payload, end_index, len_of_hex, data_arr
    end_index = data.find(END_CODE)
    if end_index < 0:
        data_payload += data
        return False
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
            return True

exec()