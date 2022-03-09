# ------------------------------------------------serial file------------------------------------------
# author by hailong.wang
# date at 2022.3.9
# -----------------------------------------------------------------------------------------------------

from my_serial import msg

FT_ON = '[FM,FT_ON]'
MEM_ERASE = '[FM,ERASE_MEM]'
SYS_REBOOT = '[FM,REBOOT_SYS]'
TEMP_CALCULATE = '[FM,TEMP_C,20]'
TEMP_GET = '[FM,TEMP_G]'
HW_SET = '[FM,HWVER_S,A0]'
HW_GET = '[FM,HWVER_G]'

RESP_FT_ON = '[FM,FT_ON,1]'
RESP_MEM_ERASE = '[FM,ERASE_MEM,1]'

ate_framework = [
                    ['enter FT mode fail!\n',               FT_ON,          RESP_FT_ON,         5000],
                    ['memory bank erase fail!\n',           MEM_ERASE,      RESP_MEM_ERASE,     3000]
                ]

class AteProcess:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def send_cmd(cmd):
        print(cmd)

    @staticmethod
    def check_response(resp, tm_out):
        data_response = msg.get(timeout = tm_out)
        if resp == data_response:
            return True
        else:
            return False

    def temprature_station(self):
        # AteProcess.send_cmd(FT_ON)
        # if not AteProcess.check_response(RESP_FT_ON, 5000):
        #     print('enter FT mode fail!!!\n')
        #     return False
        # AteProcess.send_cmd(MEM_ERASE)
        # if not AteProcess.send_cmd(RESP_MEM_ERASE, 3000):
        #     print('memory bank erase fail!!!\n')

        i = 0
        for i in range(2):
            AteProcess.send_cmd(ate_framework[i][1])
            if not AteProcess.check_response(ate_framework[i][2], ate_framework[i][3]):
                print(ate_framework[i][0])
                return False

        return True
