# ------------------------------------------------serial file------------------------------------------
# author by hailong.wang
# date at 2021.8.10
# -----------------------------------------------------------------------------------------------------

import serial
import serial.tools.list_ports
import datetime
from queue import Queue

global myser
file_name = 'serial_data.txt'
serial_flag = False
msg = Queue()
SERIAL_ID = 'MSG_SERIAL_314'


class SerialProcess:
    def __init__(self, name):
        self.name = name

    def switch_run(self):
        # print(self + ' start\n')

        global serial_flag
        while True:
            flag = input("enter 'close/open' to close/open serial port\n").strip()
            if flag == 'close':
                print('close serial\n')
                serial_flag = False
                myser.close()
            elif flag == 'open':
                print('open serial\n')
                myser.open()
                serial_flag = True
            elif flag == 'exit':
                print('exit serial\n')
            else:
                print('unknown command!\n')

    def serial_run(self):
        # print(self + ' start\n')
        global myser

        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            print("serial port can't find!")
        else:
            print("serial is ready!")
            for item in port_list:
                print(item)

        # the serial port should be COM4
        # print(port_list[1][0])
        # myser = serial.Serial(port_list[1][0], 115200, timeout=60)
        # if myser.isOpen():
        #     print("open success")
        # else:
        #     print("open failed")
        #
        while True:
            if serial_flag:
                data = myser.readline()
                if data != b'':
                    data = data.decode()
                    data = data.strip()
                    data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '  ' + data
                    print(data)
                    store_serial_data(str(data) + '\n')
                    msg.put(SERIAL_ID + str(data) + '\n')

    @staticmethod
    def get_current_ports():
        port_list = list(serial.tools.list_ports.comports())
        port_quantity = len(port_list)
        ret_list = [0 for i in range(port_quantity)]
        for index in range(port_quantity):
            ret_list[index] = port_list[port_quantity - 1 - index][0]
        return ret_list

    @staticmethod
    def open_serial(port, bit_rate):
        global myser, serial_flag
        myser = serial.Serial(port, bit_rate, timeout=60)
        if myser.isOpen():
            print("open success")
            serial_flag = True
        else:
            print("open failed")

    @staticmethod
    def close_serial():
        global myser, serial_flag
        serial_flag = False
        myser.close()


def store_serial_data(data):
    try:
        with open(file_name, 'a') as f_obj:
            f_obj.write(data)
    except FileNotFoundError:
        print('No data file existed, crate a new file\r\n')
        with open(file_name, 'w') as f_obj:
            f_obj.write(data)
        return None
