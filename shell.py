# ------------------------------------------------serial file------------------------------------------
# author by hailong.wang
# date at 2021.8.10
# -----------------------------------------------------------------------------------------------------
import time

import serial
from my_serial import SerialProcess
from ate_process import AteProcess

class AteShell:
    def cmd_run(self):
        print("please type a command.\n")

        while True:
            cmd = input().strip()
            if cmd == 'close' or cmd == 'CLOSE':
                print('close serial\n')
                SerialProcess.set_serial_flag(False)
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
                    SerialProcess.set_serial_flag(True)
                else:
                    print('please enter right port number!')
            elif cmd == 'exit':
                print('exit serial\n')
            elif cmd == 'runate' or cmd == 'RUNATE':
                print('start run ate.\n')
                if AteProcess().temperature_station():
                    print('temperature station success.\n')
                else:
                    print('temperature station fail.\n')

                if AteProcess().bft_station():
                    print('bft station success.\n')
                else:
                    print('bft station fail.\n')

                if AteProcess().led_check():
                    print('led check success.\n')
                else:
                    print('led check fail.\n')
            elif cmd == 'rundaliate' or cmd == 'RUNDALIATE':
                print('start run dali tool ate.\n')
                if AteProcess().dali_tool_settings_g():
                    print('dali ate success.\n')
                else:
                    print('dali ate fail.\n')
                time.sleep(2)
                if AteProcess().dali_tool_rf_test():
                    print('rf test success.\n')
                else:
                    print('rf test fail.\n')
            elif cmd == 'testate' or cmd == 'TESTATE':
                print('start test ate.\n')
                AteProcess().test_func()
            elif cmd == '':
                print("shell.")
            else:
                print('unknown command!\n')

