import os
import json
import subprocess
import threading
from gi.repository import Gtk, GLib

from textwrap import dedent

if os.name == 'nt':  # Windows
    config_dir = os.path.join(os.environ['APPDATA'], 'Maa-Gtk')
else:  # Linux/Mac
    config_dir = os.path.expanduser('~/.config/maa-gtk')

os.makedirs(config_dir, exist_ok=True)

config_file = os.path.join(config_dir, 'config.json')
def read_maa_gtk_config():
    if not os.path.isfile(config_file):
        print("配置文件不存在")
        return None

    try:
        # 读取配置文件内容
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            return config_data
    except json.JSONDecodeError:
        print("配置文件解析失败")
        return None
    except Exception as e:
        print("配置文件读取失败:", str(e))
        return None
    
def save_maa_gtk_config(config):
    try:
        with open(config_file, 'w') as f:
            f.write(json.dumps(config))
    except:
        print("写入配置文件失败")
    
def test_connection(maa_core, adb_device):
    ping_filepath = os.path.join(config_dir, 'ping.py');
    ping_code = dedent(f"""
        import json
        import pathlib
        import time
        import sys

        sys.path.append('{maa_core}/Python')

        from asst.asst import Asst
        from asst.utils import InstanceOptionType

        path = '{maa_core}'
        Asst.load(path=path, user_dir='{config_dir}')
        asst = Asst()
        asst.set_instance_option(InstanceOptionType.touch_type, 'maatouch')
        if asst.connect('adb', '{adb_device}'):
            print('连接成功')
        else:
            print('连接失败')
    """)

    with open(ping_filepath, 'w') as f:
        f.write(ping_code)

    result = subprocess.run(['python', ping_filepath], capture_output=True, text=True)
    return result.stdout.strip() == '连接成功'

class EditConfigDialog(Gtk.Dialog):
    def __init__(self, parent, config = None):
        Gtk.Dialog.__init__(self, "设置", parent, 0, Gtk.ButtonsType.NONE)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK,
                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.set_default_size(500, 150)
        self.set_border_width(10)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        box = self.get_content_area()

        # 创建两个 Entry，并添加到对话框中
        self.maa_path_label = Gtk.Label(label = "MAA 路径")
        self.maa_path_label.set_halign(Gtk.Align.END)
        self.maa_path_entry = Gtk.Entry()
        self.maa_path_entry.set_hexpand(True)
        if config is not None:
            self.maa_path_entry.set_text(config.get('maa_core', "/usr/share/maa-assistant-arknights"))
        self.maa_path_file_button = Gtk.Button(label="选择文件")
        self.maa_path_file_button.connect("clicked", self.on_file_button_clicked)
        grid.attach(self.maa_path_label, 0, 0, 1, 1)
        grid.attach(self.maa_path_entry, 1, 0, 1, 1)
        grid.attach(self.maa_path_file_button, 2, 0, 1, 1)

        self.adb_device_label = Gtk.Label(label = "ADB 设备")
        self.adb_device_label.set_halign(Gtk.Align.END)
        self.adb_device_entry = Gtk.Entry()
        self.adb_device_entry.set_hexpand(True)
        if config is not None:
            self.adb_device_entry.set_text(config.get('adb_device', "192.168.240.112:5555"))
        grid.attach(self.adb_device_label, 0, 1, 1, 1)
        grid.attach(self.adb_device_entry, 1, 1, 1, 1)

        self.ping_button = Gtk.Button(label="连接测试")
        self.ping_button.connect('clicked', self.on_ping_test_clicked)
        grid.attach(self.ping_button, 2, 1, 1, 1)

        self.status_label = Gtk.Label(label="请先通过连接测试")
        self.status_label.set_halign(Gtk.Align.START)
        grid.attach(self.status_label, 1, 2, 2, 1)

        box.add(grid)

        self.ok_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        self.ok_button.set_sensitive(False)

        self.show_all()

    def on_file_button_clicked(self, _):
        dialog = Gtk.FileChooserDialog(
            title="选择目录",
            parent=None,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.maa_path_entry.set_text(filename)

        dialog.destroy()

    def on_ping_test_clicked(self, _):
        maa_core = self.maa_path_entry.get_text()
        adb_device = self.adb_device_entry.get_text()

        if maa_core == "" or adb_device == "":
            self.status_label.set_text("请完善表格内容")
            return

        # 在另一个线程中运行测试连接的函数
        self.status_label.set_text("测试中...")
        self.set_sensitive(False)
        threading.Thread(target=self.run_test_connection, args=(maa_core, adb_device)).start()

    # 运行测试连接函数，将结果返回给主线程更新状态
    def run_test_connection(self, maa_core, adb_device):
        success = test_connection(maa_core, adb_device)
        GLib.idle_add(self.update_status_label, (success, maa_core, adb_device))

    def update_status_label(self, args):
        success, maa_core, adb_device = args
        self.set_sensitive(True)
        if success:
            self.status_label.set_text("连接成功")
            self.ok_button.set_sensitive(True)
            self.config = {
                'maa_core': maa_core,
                'adb_device': adb_device
            }
        else:
            self.status_label.set_text("连接失败")
