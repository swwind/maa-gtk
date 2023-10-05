import webbrowser
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ssscopilot import SSSCopilotConfigBox
from roguelike import RoguelikeConfigBox
from closedown import CloseDownConfigBox
from startup import StartUpConfigBox
from copilot import CopilotConfigBox
from recruit import RecruitConfigBox
from infrast import InfrastConfigBox
from fight import FightConfigBox
from award import AwardConfigBox
from mall import MallConfigBox

from config import EditConfigDialog, read_maa_gtk_config, save_maa_gtk_config, test_connection

items = [
    ["启动游戏", "StartUp"],
    ["关闭游戏", "CloseDown"],
    ["自动刷图", "Fight"],
    ["公开招募", "Recruit"],
    ["基建换班", "Infrast"],
    ["信用商店", "Mall"],
    ["任务奖励", "Award"],
    ["刷肉鸽", "Roguelike"],
    ["抄作业", "Copilot"],
    ["保全派驻", "SSSCopilot"],
]

class CreateTaskDialog(Gtk.Dialog):
    def __init__(self, parent, name = "新建任务"):
        Gtk.Dialog.__init__(self, "创建新任务", parent, 0, Gtk.ButtonsType.NONE)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK,
                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.set_default_size(954, 518)
        self.set_border_width(10)

        vbox = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(spacing=10)

        self.right_box = Gtk.Box(spacing=10)

        # 创建一个ListBox，并添加一些项目
        self.listbox = Gtk.ListBox()
        self.listbox.set_size_request(200, -1)
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)

        for mname, mtype in items:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=f"{mname} - {mtype}")
            row.add(label)
            self.listbox.add(row)
        self.listbox.connect("row-selected", self.on_row_selected)
        self.listbox.select_row(self.listbox.get_row_at_index(0))

        hbox.pack_start(self.listbox, False, False, 0)
        hbox.pack_start(self.right_box, True, True, 0)

        self.name_label = Gtk.Label(label="任务名称")
        self.name_entry = Gtk.Entry()
        self.name_entry.set_text(name)
        self.name_entry.set_hexpand(True)
        self.name_box = Gtk.Box(spacing=10)
        self.name_box.add(self.name_label)
        self.name_box.add(self.name_entry)

        vbox.pack_start(self.name_box, False, False, 0)
        vbox.pack_start(hbox, True, True, 0)

        area = self.get_content_area()
        area.pack_start(vbox, True, True, 0)

        self.connect('response', self.on_response)
        self.show_all()

    def on_row_selected(self, _, row):
        type = items[row.get_index()][1]
        self.component = None

        if type == "StartUp":
            self.component = StartUpConfigBox()
        elif type == "CloseDown":
            self.component = CloseDownConfigBox()
        elif type == "Fight":
            self.component = FightConfigBox()
        elif type == "Recruit":
            self.component = RecruitConfigBox()
        elif type == "Infrast":
            self.component = InfrastConfigBox()
        elif type == "Mall":
            self.component = MallConfigBox()
        elif type == "Award":
            self.component = AwardConfigBox()
        elif type == "Roguelike":
            self.component = RoguelikeConfigBox()
        elif type == "Copilot":
            self.component = CopilotConfigBox()
        elif type == "SSSCopilot":
            self.component = SSSCopilotConfigBox()

        if self.component is not None:
            children = self.right_box.get_children()
            for child in children:
                self.right_box.remove(child)
                child.destroy()
            self.right_box.add(self.component)
            self.component.show_all()

    def on_response(self, _, response_id):
        if response_id == Gtk.ResponseType.OK:
            self.type = items[self.listbox.get_selected_row().get_index()][1]
            self.name = self.name_entry.get_text()
            self.config = self.component.get_config()

class Task:
    def __init__(self, name, type, config):
        self.name = name
        self.type = type
        self.config = config

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="MAA GTK")
        self.set_default_size(335, 518)
        self.tasks = []  # 初始化任务列表
        self.config = read_maa_gtk_config()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        self.menubar = Gtk.MenuBar()
        vbox.pack_start(self.menubar, False, False, 0)

        filem = Gtk.MenuItem(label="选项")
        filemenu = Gtk.Menu()
        filem.set_submenu(filemenu)
        self.menubar.append(filem)

        configb = Gtk.MenuItem(label="设置")
        configb.connect('activate', self.open_edit_config_page)
        filemenu.append(configb)

        exitb = Gtk.MenuItem(label="退出")
        exitb.connect('activate', Gtk.main_quit)
        filemenu.append(exitb)

        aboutm = Gtk.MenuItem(label="关于")
        aboutmenu = Gtk.Menu()
        aboutm.set_submenu(aboutmenu)
        self.menubar.append(aboutm)

        configb = Gtk.MenuItem(label="GitHub...")
        configb.connect('activate', self.open_github_page)
        aboutmenu.append(configb)

        innerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        innerbox.set_border_width(10)
        vbox.pack_start(innerbox, True, True, 0)

        # 创建一个 ListBox 来展示任务列表
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        innerbox.pack_start(self.listbox, True, True, 0)

        # 添加任务项到 ListBox
        for task in self.tasks:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=task.name)
            row.add(label)
            self.listbox.add(row)

        # 创建一个按钮 Box
        self.button_box = Gtk.Box()
        innerbox.pack_start(self.button_box, False, False, 0)

        button1 = Gtk.Button(label="添加")
        button1.connect("clicked", self.create_new_task)
        self.button_box.pack_start(button1, True, True, 0)

        button2 = Gtk.Button(label="编辑")
        self.button_box.pack_start(button2, True, True, 0)

        button3 = Gtk.Button(label="上移")
        button3.connect("clicked", self.move_task_up)
        self.button_box.pack_start(button3, True, True, 0)

        button4 = Gtk.Button(label="下移")
        button4.connect("clicked", self.move_task_down)
        self.button_box.pack_start(button4, True, True, 0)

        button5 = Gtk.Button(label="删除")
        self.button_box.pack_start(button5, True, True, 0)

        self.last_selected_row = None

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def open_edit_config_page(self, _):
        dialog = EditConfigDialog(self, self.config or {})
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.config = dialog.config
            save_maa_gtk_config(self.config)
        dialog.destroy()

    def open_github_page(self, _):
        webbrowser.open("https://github.com")

    def create_new_task(self, _):
        dialog = CreateTaskDialog(self, name = f"任务 {len(self.tasks) + 1}")
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            task = Task(
                name=dialog.name,
                type=dialog.type,
                config=dialog.config)
            self.tasks.append(task)  # 将任务添加到列表中

            # 在 ListBox 中添加新的任务项
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=task.name)
            row.add(label)
            self.listbox.add(row)

            self.show_all()

        dialog.destroy()

    def move_task_up(self, _):
        # 实现将当前选中的任务提前的代码逻辑
        row = self.listbox.get_selected_row() or self.last_selected_row

        # 如果还没有选择，那么返回
        if row is None:
            return

        # 如果当前选中的是第一个任务项，则无法再往前移动
        index = row.get_index()
        if index == 0:
            return

        # 将当前选中的任务项和它的前一个任务项交换位置
        self.tasks[index], self.tasks[index-1] = self.tasks[index-1], self.tasks[index]

        # 更新 ListBox 中的任务项顺序
        self.listbox.remove(row)
        self.listbox.insert(row, index-1)
        self.last_selected_row = row

    def move_task_down(self, _):
        # 实现将当前选中的任务延后的代码逻辑
        row = self.listbox.get_selected_row() or self.last_selected_row

        # 如果还没有选择，那么返回
        if row is None:
            return

        # 如果当前选中的是最后一个任务项，则无法再往后移动
        index = row.get_index()
        if index == len(self.tasks) - 1:
            return

        # 将当前选中的任务项和它的后一个任务项交换位置
        self.tasks[index], self.tasks[index+1] = self.tasks[index+1], self.tasks[index]

        # 更新 ListBox 中的任务项顺序
        self.listbox.remove(row)
        self.listbox.insert(row, index+1)
        self.last_selected_row = row

# test_connection(read_maa_gtk_config())

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
