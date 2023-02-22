# ------------------------------------------------serial file------------------------------------------
# author by hailong.wang
# date at 2022.3.9
# -----------------------------------------------------------------------------------------------------

import time
import re
from record_mem import RecordMemory
from my_serial import SerialProcess
from my_serial import msg
from my_serial import SERIAL_ID

ERR_VALUE = 0xffff

TEMP_VAL = 25
SW_REGIME_VAL = 0
HW_STR = 'D2'

# temperature station
FT_ON = '[FM,FT_ON]'
MEM_ERASE = '[FM,ERASE_MEM]'
SYS_REBOOT = '[FM,REBOOT_SYS]'
TEMP_CALCULATE = '[FM,TEMP_C,' + str(TEMP_VAL) + ']'
TEMP_GET = '[FM,TEMP_G]'
HW_SET = '[FM,HWVER_S,' + HW_STR + ']'
HW_GET = '[FM,HWVER_G]'
LED_ON = '[FM,LED_C,1]'
LED_OFF = '[FM,LED_C,0]'
RF_TEST = '[FM,RF_ON]'
MB_UNLOCK = '[FM,MB_UNLOCK]'
MB_10NC_SET = '[FM,MB_10NC_S,9137010576]'
MB_NAME_SET = '[FM,MB_NAME_S,LLC7852]'
MB_DATE_S = '[FM,MB_DATE_S,20221213]'
MB_SW_REGIME_S = '[FM,SW_REGIME_S,' + str(SW_REGIME_VAL) + ']'
MB_LUXLV_ON_S = '[FM,LUXLV_ON_S,30]'
MB_LUXLV_OFF_S = '[FM,LUXLV_OFF_S,10]'
MB_DIM_S = '[FM,DIM_S,0]'
MB_AS_SUNRISEA_S = '[FM,AS_SUNRISEA_S,12]'
MB_AS_SUNSETA_S = '[FM,AS_SUNSETA_S,13]'
MB_AS_TMSUNRISE_S = '[FM,AS_TMSUNRISE_S,22]'
MB_AS_TMSUNSET_S = '[FM,AS_TMSUNSET_S,23]'


RESP_FT_ON = '[FM,FT_ON,1]'
RESP_MEM_ERASE = '[FM,ERASE_MEM,1]'
RESP_SYS_REBOOT = '[FM,REBOOT_SYS,1]'
RESP_TEMP_CALCULATE = '[FM,TEMP_C,1]'
RESP_TEMP_OFFSET = '[FW,TEMP_OFFSET,'
RESP_TEMP_GET = '[FM,TEMP_G,1]'
RESP_TEMP_VALUE = '[FM,TEMP_G,1]'
RESP_HW_SET = '[FM,HWVER_S,1]'
RESP_HW_GET = '[FM,HWVER_G,1]'
RESP_HW_VALUE = '[FM,HWVER_R,'
RESP_LED_C = '[FM,LED_C,1]'

# BFT station
VDC_C = '[FM,VDC_C]'
VEDLC_C = '[FM,VEDLC_C]'
SETTINGS_G = '[FM,SETTINGS_G]'

VDC_R = '[FM,VDC_C,1]'
VEDLC_R = '[FM,VEDLC_C,1]'
RESP_SETTINGS_G = '[FM,SETTINGS_R,L]'
SETTINGS_R = '[FM,SETTINGS_R,'
DALI_TOOL_RESP_SETTINGS_G = '[FM,SETTINGS_G,1]'
DALI_TOOL_RESP_RF_ON = '[FM,RF_ON,1]'
DALI_TOOL_RESP_RESULT_RF = '[FM,RF_ON_R,1]'

REBOOT_START_INFOR = 'debug init success'

# ----------------  fail log ----------------------------  command  ----  response   -------------- timeout - retry - #
ate_framework = [
                    ['enter FT mode fail!\n',               FT_ON,          RESP_FT_ON,                 5,      3],
                    ['memory bank erase fail!\n',           MEM_ERASE,      RESP_MEM_ERASE,             3,      3],
                    ['system reboot fail!\n',               SYS_REBOOT,     RESP_SYS_REBOOT,            3,      3],
                    ['temperature calculate fail!\n',       TEMP_CALCULATE, RESP_TEMP_CALCULATE,        3,      3],
                    ['temp get fail!\n',                    TEMP_GET,       RESP_TEMP_GET,              3,      3],
                ]


class AteProcess:
    def __init__(self):
        self.software_ver = []
        self.hardware_ver = []
        self.imei = []
        self.ccid = []
        self.imsi = []
        self.modem_hw_ver = []
        self.modem_sw_ver = []
        self.ctcid = []

    def send_cmd(self, cmd):
        print(cmd)
        SerialProcess.send_data(cmd.encode())

    def check_response(self, resp, tm_out):
        # clear message queue to avoid receive old data.
        msg.queue.clear()

        try:
            data_response = msg.get(timeout=tm_out)
        except:
            print('queue empty')
            return False
        if SERIAL_ID not in data_response:
            return False
        data_response = data_response.lstrip(SERIAL_ID).strip()
        if resp == data_response:
            return True
        else:
            print('\nexpect resp : ' + resp + '  fact resp : ' + data_response.lstrip(SERIAL_ID) + '\n')
            return False


    def check_key_str(self, target_str, try_times, tm_out):
        # clear message queue to avoid receive old data.
        msg.queue.clear()

        reboot_infor = []
        for retry in range(try_times):
            try:
                reboot_infor = msg.get(timeout=tm_out)
            except:
                print('queue empty')

            print('receive reboot infor\n')
            if target_str in reboot_infor:
                return True


    def launch_ate(self, start_cmd_item, redo, redo_delay, total_cmd_num):
        index = start_cmd_item
        cmds = total_cmd_num

        for i in range(cmds):
            index += i
            for retry in range(redo):
                self.send_cmd(ate_framework[index][1])
                SerialProcess.switch_queue_flag(True)
                result = self.check_response(ate_framework[index][2], ate_framework[index][3])
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

    def get_response_value(self, resp, tm_out, is_str):
        # clear message queue to avoid receive old data.
        msg.queue.clear()

        try:
            value_response = msg.get(timeout=tm_out)
        except:
            print('queue empty\n')
            return ERR_VALUE

        value_response = value_response.lstrip(SERIAL_ID).strip()
        if resp == value_response:
            try:
                value_response = msg.get(timeout=tm_out)
                # print('msg2 = ' + value_response)
            except:
                print('queue empty\n')
                return ERR_VALUE
            if not is_str:
                value_response = value_response.lstrip(SERIAL_ID).strip()
                r_value = re.sub("\D", "", value_response)
                if '-' in value_response:
                    rst = int(r_value) * (-1)
                else:
                    rst = int(r_value)
                return rst
            else:
                # [FM,HWVER_R,A0] to FM,HWVER_R,A0
                value_response = value_response.strip(']' + '[')
                # ['FM', 'HWVER_R', 'A0']
                rst = value_response.split(',')
                # delete 'FM' 'HWVER_R'
                return rst[2]

        else:
            return ERR_VALUE

    def temperature_station(self):
        # create memory bank xml file
        RecordMemory.create_xml()

        # 1.enter FT mode 2.erase memory bank 3.reboot system
        if not self.launch_ate(start_cmd_item=0, redo=3, redo_delay=2, total_cmd_num=3):
            return False
        # waiting for system reboot
        # time.sleep(15)
        SerialProcess.switch_queue_flag(True)
        if not self.check_key_str(target_str=REBOOT_START_INFOR, try_times=5, tm_out=10):
            return False
        time.sleep(1)
        # enter FT mode
        if not self.launch_ate(start_cmd_item=0, redo=5, redo_delay=2, total_cmd_num=1):
            return False

        # 1.temperature calibration 2.read temperature
        time.sleep(2)
        self.send_cmd(TEMP_CALCULATE)
        SerialProcess.switch_queue_flag(True)
        t_offset = self.get_response_value(resp=RESP_TEMP_CALCULATE, tm_out=3, is_str=False)
        if ERR_VALUE != t_offset:
            RecordMemory.update_item_xml('Toffset', t_offset)
            rst = True
        else:
            print('temperature calibration fail!!!\n')
            rst = False

        if rst:
            time.sleep(2)
            self.send_cmd(TEMP_GET)
            SerialProcess.switch_queue_flag(True)
            t_value = self.get_response_value(resp=RESP_TEMP_GET, tm_out=3, is_str=False)
            if (ERR_VALUE != t_value) and ((TEMP_VAL - 2) <= t_value <= (TEMP_VAL + 2)):
                rst = True
            else:
                print('temperature get value fail!!!\n')
                rst = False

        SerialProcess.switch_queue_flag(False)
        return rst

    def vdc_vedlc_check(self, v_resp, vcc_h, vcc_l, v_tmout):
        v_value = self.get_response_value(resp=v_resp, tm_out=v_tmout, is_str=False)
        if ERR_VALUE != v_value:
            if vcc_h > int(v_value) > vcc_l:
                return True
            else:
                return False
        else:
            return False

    def get_board_information(self):
        self.send_cmd(SETTINGS_G)
        SerialProcess.switch_queue_flag(True)
        # clear message queue to avoid receive old data.
        msg.queue.clear()

        try:
            response = msg.get(timeout=50)
            # print('msg1 = ' + response)
        except:
            print('queue empty\n')
            return False

        response = response.lstrip(SERIAL_ID).strip()
        if response == RESP_SETTINGS_G:
            try:
                value_response = msg.get(timeout=2)
                # print('msg2 = ' + value_response)
            except:
                print('queue empty\n')
                return False
            if SETTINGS_R in value_response:
                value_response = value_response.lstrip(SERIAL_ID + SETTINGS_R).strip('[').strip(']')
                infor_buff = value_response.split(',')
                self.software_ver = infor_buff[0]
                self.hardware_ver = infor_buff[1]
                self.imei = infor_buff[2]
                self.ccid = infor_buff[3]
                self.imsi = infor_buff[4]
                self.modem_hw_ver = infor_buff[5]
                self.modem_sw_ver = infor_buff[6]
                self.ctcid = infor_buff[7]
                RecordMemory.update_item_xml('HardwareRevision', self.hardware_ver)
                RecordMemory.update_item_xml('IMEI', self.imei)
                RecordMemory.update_item_xml('Version', self.modem_hw_ver + self.modem_sw_ver)
                RecordMemory.update_item_xml('UniqueId', self.ctcid)
                return True
            else:
                return False
        else:
            return False

    def bft_station(self):
        rst = False

        # enter FT mode
        for retry in range(3):
            self.send_cmd(FT_ON)
            SerialProcess.switch_queue_flag(True)
            result = self.check_response(RESP_FT_ON, 3)
            if result:
                rst = True
                break
            elif not result and retry == 2:
                SerialProcess.switch_queue_flag(False)
            time.sleep(1)

        # set hardware version
        if rst:
            time.sleep(2)
            self.send_cmd(HW_SET)
            SerialProcess.switch_queue_flag(True)
            result = self.check_response(RESP_HW_SET, 3)
            if result:
                self.send_cmd(HW_GET)
                hw = self.get_response_value(resp=RESP_HW_GET, tm_out=3, is_str=True)
                if ERR_VALUE != hw and HW_STR == str(hw):
                    rst = True
                else:
                    print('HW ver is error!!!\n')
                    rst = False
            else:
                rst = False

        # check vdc
        if rst:
            time.sleep(2)
            self.send_cmd(VDC_C)
            if self.vdc_vedlc_check(v_resp=VDC_R, vcc_h=26000, vcc_l=23000, v_tmout=15):
                rst = True
            else:
                print('vdc check fail!!!\n')
                rst = False

        # check vedlc
        if rst:
            time.sleep(2)
            self.send_cmd(VEDLC_C)
            if self.vdc_vedlc_check(v_resp=VEDLC_R, vcc_h=4000, vcc_l=3500, v_tmout=3):
                rst = True
            else:
                rst = False
                print('vedlc check fail.\n')

        # get board information
        if rst:
            time.sleep(2)
            if self.get_board_information():
                rst = True
            else:
                rst = False

        return rst


    def led_check(self):
        rst = False
        self.send_cmd(LED_ON)
        if(self.check_response(RESP_LED_C, 1)):
            time.sleep(5)
            self.send_cmd(LED_OFF)
            if(self.check_response(RESP_LED_C, 1)):
                rst = True
            else:
                rst = False
        else:
            rst = False

        return rst

    def dali_tool_get_board_info(self):
        self.send_cmd(SETTINGS_G)
        SerialProcess.switch_queue_flag(True)
        # clear message queue to avoid receive old data.
        msg.queue.clear()

        try:
            response = msg.get(timeout=60)
            # print('msg1 = ' + response)
        except:
            print('queue empty\n')
            return False

        response = response.lstrip(SERIAL_ID).strip()
        if response == DALI_TOOL_RESP_SETTINGS_G:
            try:
                value_response = msg.get(timeout=2)
                # print('msg2 = ' + value_response)
            except:
                print('queue empty\n')
                return False
            if SETTINGS_R in value_response:
                value_response = value_response.lstrip(SERIAL_ID + SETTINGS_R).strip('[').strip(']')
                infor_buff = value_response.split(',')
                self.software_ver = infor_buff[0]
                self.hardware_ver = infor_buff[1]
                self.imei = infor_buff[2]
                self.ccid = infor_buff[3]
                return True
            else:
                return False
        else:
            return False

    def dali_tool_settings_g(self):
        rst = False

        # enter FT mode
        for retry in range(3):
            self.send_cmd(FT_ON)
            SerialProcess.switch_queue_flag(True)
            result = self.check_response(RESP_FT_ON, 5)
            if result:
                rst = True
                break
            elif not result and retry == 2:
                SerialProcess.switch_queue_flag(False)
            time.sleep(1)

        time.sleep(1)
        if rst:
            for retry in range(3):
                if self.dali_tool_get_board_info():
                    rst = True
                    break
                else:
                    rst = False

        return rst


    def dali_tool_rf_test(self):
        rst = False

        self.send_cmd(RF_TEST)
        if(self.check_response(DALI_TOOL_RESP_RF_ON, 3)):
            if(self.check_response(DALI_TOOL_RESP_RESULT_RF, 40)):
                rst = True
            else:
                rst = False
        else:
            rst = False

        return rst


    def dali_tool_mem_set(self):
        rst = False

        # enter FT mode
        SerialProcess.switch_queue_flag(True)
        for retry in range(3):
            self.send_cmd(FT_ON)
            result = self.check_response(RESP_FT_ON, 5)
            if result:
                rst = True
                break
            elif not result and retry == 2:
                SerialProcess.switch_queue_flag(False)
            time.sleep(1)

        time.sleep(1)
        if rst:
            self.send_cmd(MB_UNLOCK)
            result = self.check_response(RESP_FT_ON, 5)

        return rst


    def test_func(self):

        # if 0:
        #     if not self.launch_ate(start_cmd_item=0, redo=5, redo_delay=2, total_cmd_num=1):
        #         return False
        #
        #     SerialProcess.switch_queue_flag(True)
        #     # 1.temperature calibration 2.read temperature
        #     self.send_cmd(TEMP_CALCULATE)
        #     t_offset = self.get_response_value(resp=RESP_TEMP_CALCULATE, tm_out=3, is_str=False)
        #     if ERR_VALUE != t_offset:
        #         RecordMemory.update_item_xml('Toffset', t_offset)
        #         rst = True
        #     else:
        #         print('vdc check fail!!!\n')
        #         rst = False
        #
        #     return True

        if 0:
            RecordMemory.create_xml()
            RecordMemory.update_item_xml('Toffset', '24')

            return True

        if 1:
            rst = False
            self.send_cmd(VDC_C)
            if self.vdc_vedlc_check(v_resp=VDC_R, vcc_h=26000, vcc_l=23000, v_tmout=15):
                rst = True
            else:
                print('vdc check fail!!!\n')
                rst = False

            return rst
