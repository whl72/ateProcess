# ------------------------------------------------serial file------------------------------------------
# author by hailong.wang
# date at 2022.3.9
# -----------------------------------------------------------------------------------------------------

import time
from my_serial import SerialProcess
from my_serial import msg
from my_serial import SERIAL_ID

FT_ON = '[FM,FT_ON]'
MEM_ERASE = '[FM,ERASE_MEM]'
SYS_REBOOT = '[FM,REBOOT_SYS]'
TEMP_CALCULATE = '[FM,TEMP_C,20]'
TEMP_GET = '[FM,TEMP_G]'
HW_SET = '[FM,HWVER_S,A0]'
HW_GET = '[FM,HWVER_G]'

RESP_FT_ON = '[FM,FT_ON,1]'
RESP_MEM_ERASE = '[FM,ERASE_MEM,1]'
RESP_SYS_REBOOT = '[FM,REBOOT_SYS,1]'
RESP_TEMP_CALCULATE = '[FM,TEMP_C,1]'
RESP_TEMP_OFFSET = '[FW,TEMP_OFFSET,'
RESP_TEMP_GET = '[FM,TEMP_G,1]'
RESP_TEMP_VALUE = '[FM,TEMP_G,1]'

# ----------------  fail log ----------------------------  command  ----  response   -------------- timeout - retry - #
ate_framework = [
                    ['enter FT mode fail!\n',               FT_ON,          RESP_FT_ON,                 5,      3],
                    ['memory bank erase fail!\n',           MEM_ERASE,      RESP_MEM_ERASE,             3,      3],
                    ['system reboot fail!\n',               SYS_REBOOT,     RESP_SYS_REBOOT,            3,      3],
                    ['temperature calculate fail!\n',       TEMP_CALCULATE, RESP_TEMP_CALCULATE,        3,      3],
                    ['temp get fail!\n',                    TEMP_GET,       RESP_TEMP_GET,              3,      3],
                ]

class AteProcess:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def send_cmd(cmd):
        print(cmd)
        SerialProcess.send_data(cmd.encode())

    @staticmethod
    def check_response(resp, tm_out):
        # clear message queue to avoid receive old data.
        msg.queue.clear()

        try:
            data_response = msg.get(timeout=tm_out)
        except:
            print('queue empty')
            return False
        if not SERIAL_ID in data_response:
            return False
        data_response = data_response.lstrip(SERIAL_ID).strip()
        print('\nexpect resp : ' + resp + '  fact resp : ' + data_response.lstrip(SERIAL_ID) + '\n')
        if resp == data_response:
            return True
        else:
            # print('\nexpect resp : ' + resp + '  fact resp : ' + data_response.lstrip(SERIAL_ID) + '\n')
            return False

    @staticmethod
    def launch_ate(start_cmd_item, redo, redo_delay, total_cmd_num):
        index = start_cmd_item
        cmds = total_cmd_num

        for i in range(cmds):
            index += i
            for retry in range(redo):
                AteProcess.send_cmd(ate_framework[index][1])
                SerialProcess.switch_queue_flag(True)
                result = AteProcess.check_response(ate_framework[index][2], ate_framework[index][3])
                if result:
                    index = start_cmd_item
                    # must delay 1 second to send next command
                    time.sleep(1)
                    break
                elif not result and retry == redo - 1:
                    SerialProcess.switch_queue_flag(False)
                    return False
                time.sleep(redo_delay)

        SerialProcess.switch_queue_flag(False)
        return True

    @staticmethod
    def temperature_station():
        # AteProcess.send_cmd(FT_ON)
        # if not AteProcess.check_response(RESP_FT_ON, 3):
        #     print('enter FT mode fail!!!\n')
        #     return False
        # AteProcess.send_cmd(MEM_ERASE)
        # if not AteProcess.check_response(RESP_MEM_ERASE, 3):
        #     print('memory bank erase fail!!!\n')

        # for i in range(3):
        #     AteProcess.send_cmd(ate_framework[i][1])
        #     if not AteProcess.check_response(ate_framework[i][2], ate_framework[i][3]):
        #         print(ate_framework[i][0])
        #         return False

        # time.sleep(10)
        # AteProcess.send_cmd(FT_ON)
        # if not AteProcess.check_response(RESP_FT_ON, 5):
        #     print('enter FT mode fail!!!\n')
        #     return False
        #
        # index = 3
        # for i in range(2):
        #     index += i
        #     for retry in range(ate_framework[index][4]):
        #         AteProcess.send_cmd(ate_framework[index][1])
        #         if not AteProcess.check_response(ate_framework[index][2], ate_framework[index][3]) and \
        #                 retry == ate_framework[index][4] - 1:
        #             print(ate_framework[index][0])
        #             return False

        if not AteProcess.launch_ate(start_cmd_item=0, redo=3, redo_delay=2, total_cmd_num=3):
            return False

        time.sleep(10)

        if not AteProcess.launch_ate(start_cmd_item=0, redo=5, redo_delay=2, total_cmd_num=1):
            return False
        if not AteProcess.launch_ate(start_cmd_item=3, redo=3, redo_delay=2, total_cmd_num=2):
            return False

        return True

    def bft_station(self):
        res = False

        return res
