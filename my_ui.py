# ----------------------------------------------------ui file------------------------------------------
# author by hailong.wang
# date at 2021.8.10
# -----------------------------------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from my_serial import msg

global serial_ui
global comboxlist
UI_ID = 'MSG_UI_159'
OPEN_SERIAL = 'open_ser'
CLOSE_SERIAL = 'close_ser'


class MyUi:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def ui_set_init_window(self):
        self.init_window_name.title("配置工具_v1.0")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        # 标签
        self.receive_data_label = Label(self.init_window_name, text="接收区")
        self.receive_data_label.grid(row=0, column=0)
        self.send_data_label = Label(self.init_window_name, text="发送区")
        self.send_data_label.grid(row=13, column=0)
        # self.log_label = Label(self.init_window_name, text="日志")
        # self.log_label.grid(row=12, column=0)
        # 文本框
        self.receive_data_Text = Text(self.init_window_name, width=70, height=35)
        self.receive_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.send_data_Text = Text(self.init_window_name, width=70, height=5)
        self.send_data_Text.grid(row=14, column=0, rowspan=10, columnspan=10)
        # self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        # self.log_data_Text.grid(row=14, column=0, columnspan=10)
        # 按钮
        self.clear_button = Button(self.init_window_name, text="清除窗口", bg="lightblue", width=10,
                                              command=self.ui_clear_receive_data)  # 调用内部方法  加()为直接调用
        self.clear_button.grid(row=12, column=0)
        self.send_button = Button(self.init_window_name, text="发 送", bg="lightblue", width=10,
                                   command=self.ui_clear_receive_data)  # 调用内部方法  加()为直接调用
        self.send_button.grid(row=44, column=0)
        # 串口选择、波特率设置
        # comval = StringVar(self.init_window_name)
        # comboxlist = ttk.Combobox(self.init_window_name, textvariable=comval)
        # comboxlist["values"] = ('DEFAULT')
        # comboxlist.current(0)
        # comboxlist.grid()
        self.normal_ddl = Label(self.init_window_name, text='串口选择')
        self.ddl = ttk.Combobox(self.init_window_name)
        self.ddl['value'] = ('Default')
        self.ddl.grid()
        # 打开串口按钮
        # buttontext = StringVar(self.init_window_name)
        # buttontext.set('打开串口')
        self.switch_serial_button = Button(self.init_window_name, text='打开串口', width=10,
                                           command=self.ui_switch_serial)
        self.switch_serial_button.grid()

    # 清除接收区
    def ui_clear_receive_data(self):
        self.receive_data_Text.delete(1.0, END)

    # 显示接收内容
    def ui_write_receive_data(self, data):
        self.receive_data_Text.insert('end', data)

    # 更新当前串口
    def ui_update_serial_port(self, data):
        # global comboxlist
        # comboxlist["values"] = data
        self.ddl['value'] = data

    # 获取当前选中的串口
    def ui_get_current_port(self):
        return self.ddl.get()

    # 开关串口
    def ui_switch_serial(self):
        if self.switch_serial_button["text"] == '打开串口':
            self.switch_serial_button["text"] = '关闭串口'
            msg.put(UI_ID + OPEN_SERIAL)
        else:
            self.switch_serial_button["text"] = '打开串口'
            msg.put(UI_ID + CLOSE_SERIAL)
