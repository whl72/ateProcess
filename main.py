# -----------------------------------------------main file---------------------------------------------
# author by hailong.wang
# date at 2021.8.10
# -----------------------------------------------------------------------------------------------------

import threading
import my_serial
import shell


serial_port = my_serial.SerialProcess


if __name__ == '__main__':
    shell_cmd = threading.Thread(target=shell.AteShell.cmd_run, args=("ShellThread",))
    serialThread = threading.Thread(target=serial_port.serial_run, args=("SerialThread",))

    shell_cmd.start()
    serialThread.start()
    serialThread.join(timeout=0.01)
