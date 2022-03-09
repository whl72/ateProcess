# ------------------------------------------------serial file------------------------------------------
# author by hailong.wang
# date at 2021.8.10
# -----------------------------------------------------------------------------------------------------

import serial
import serial.tools.list_ports
import datetime
from queue import Queue

myser = serial.Serial()
msg = Queue()

file_name = 'serial_data.txt'
SERIAL_ID = 'MSG_SERIAL_314'

serial_flag = False
data = [0] * 2000


class SerialProcess:
    def __init__(self, name):
        self.name = name

    def cmd_run(self):
        # print(self + ' start\n')

        global serial_flag
        while True:
            cmd = input("enter 'close/open' to close/open serial port\n").strip()
            if cmd == 'close' or cmd == 'CLOSE':
                print('close serial\n')
                serial_flag = False
                # myser.close()
                SerialProcess.close_serial()
            elif cmd == 'open' or cmd == 'OPEN':
                port_list = list(serial.tools.list_ports.comports())
                if len(port_list) <= 0:
                    print("serial port can't find!")
                else:
                    print("===============alive serial port as below=================")
                    for item in port_list:
                        print(item)
                    print("==========================================================")
                com_number = input('please select a serial port.\n')
                result = SerialProcess.is_right_port(com_number)
                if result:
                    SerialProcess.open_serial(com_number, 115200)
                    print('open serial\n')
                    serial_flag = True
                else:
                    print('please enter right port number!')
            elif cmd == 'exit':
                print('exit serial\n')
            else:
                print('unknown command!\n')

    def serial_run(self):
        global data

        while True:
            if serial_flag:
                data = myser.readline()
                if data != b'':
                    # should ignore decode errors, or it will crash
                    data = data.decode('utf-8', errors='ignore')
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

    @staticmethod
    def is_right_port(ser_port):
        port_list = list(serial.tools.list_ports.comports())
        for item in port_list:
            if ser_port in item:
                return True

        return False


def store_serial_data(data):
    try:
        with open(file_name, 'a') as f_obj:
            f_obj.write(data)
    except FileNotFoundError:
        print('No data file existed, crate a new file\r\n')
        with open(file_name, 'w') as f_obj:
            f_obj.write(data)
        return None
