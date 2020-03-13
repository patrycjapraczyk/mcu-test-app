from ComInterfaceFactory import ComInterfaceFactory

INTERFACE_TYPE = 'SERIAL'


def main():
    com_interface = ComInterfaceFactory().get_interface(INTERFACE_TYPE)
    com_interface.init_connection()
    com_interface.readData()

main()