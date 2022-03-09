# -----------------------------------------------main file---------------------------------------------
# author by hailong.wang
# date at 2021.8.10
# -----------------------------------------------------------------------------------------------------

import threading
import my_serial
import time


serial_port = my_serial.SerialProcess


if __name__ == '__main__':
    closeThread = threading.Thread(target=serial_port.cmd_run, args=("CloseThread",))
    serialThread = threading.Thread(target=serial_port.serial_run, args=("SerialThread",))

    closeThread.start()
    serialThread.start()
    serialThread.join(timeout=0.01)
