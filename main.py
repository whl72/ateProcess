# -----------------------------------------------main file---------------------------------------------
# author by hailong.wang
# date at 2021.8.10
# -----------------------------------------------------------------------------------------------------

import threading
import my_ui
import tkinter
import my_serial
import queue
from my_serial import msg, SERIAL_ID
from my_ui import UI_ID, OPEN_SERIAL, CLOSE_SERIAL
import time


init_window = tkinter.Tk()
serial_ui = my_ui.MyUi(init_window)
serial_port = my_serial.SerialProcess


def start_ui():
    serial_ui.ui_set_init_window()
    init_window.mainloop()


def main_fun(que, threadname):
    while True:
        try:
            # main function, get all messages form other thread, and process them
            data = que.get(block=True, timeout=0.05)
            if data is None:
                break
            if SERIAL_ID in data:
                serial_ui.ui_write_receive_data(data[len(SERIAL_ID):])
            elif UI_ID in data:
                if OPEN_SERIAL in data:
                    serial_port.open_serial(serial_ui.ui_get_current_port(), 115200)
                elif CLOSE_SERIAL in data:
                    serial_port.close_serial()
        except queue.Empty:
            info = None
        # time.sleep(2)
        ports = serial_port.get_current_ports()
        # print(ports)
        serial_ui.ui_update_serial_port(serial_port.get_current_ports())


if __name__ == '__main__':
    closeThread = threading.Thread(target=serial_port.switch_run, args=("CloseThread",))
    serialThread = threading.Thread(target=serial_port.serial_run, args=("SerialThread",))
    funcThread = threading.Thread(target=main_fun, args=[msg, "MainFunctionThread"])

    closeThread.start()
    serialThread.start()
    funcThread.start()
    serialThread.join(timeout=0.01)
    funcThread.join(timeout=0.01)

    start_ui()
