from gui import Gtk

from roguelike import RoguelikeConfigBox
from startup import StartUpConfigBox
from recruit import RecruitConfigBox
from infrast import InfrastConfigBox
from fight import FightConfigBox

items = [
    ["启动游戏", "StartUp"],
    ["关闭游戏", "CloseDown"],
    ["自动刷图", "Fight"],
    ["公开招募", "Recruit"],
    ["基建换班", "Infrast"],
    ["信用商店", "Mall"],
    ["任务奖励", "Award"],
    ["自动刷肉鸽", "Roguelike"],
    ["自动抄作业", "Copilot"],
]

class CreateTaskDialog(Gtk.Dialog):
    def __init__(self, parent):
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

        for name, type in items:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=f"{name} - {type}")
            row.add(label)
            self.listbox.add(row)

        self.listbox.connect("row-selected", self.on_row_selected)
        self.listbox.select_row(self.listbox.get_row_at_index(0))

        hbox.pack_start(self.listbox, False, False, 0)
        hbox.pack_start(self.right_box, True, True, 0)

        self.name_label = Gtk.Label(label="任务名称")
        self.name_entry = Gtk.Entry()
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
        print(row.get_index(), type)
        self.component = None

        if type == "StartUp":
            self.component = StartUpConfigBox()
        elif type == "CloseDown":
            pass
        elif type == "Fight":
            self.component = FightConfigBox()
        elif type == "Recruit":
            self.component = RecruitConfigBox()
        elif type == "Infrast":
            self.component = InfrastConfigBox()
        elif type == "Mall":
            pass
        elif type == "Award":
            pass
        elif type == "Roguelike":
            self.component = RoguelikeConfigBox()
        elif type == "Copilot":
            pass

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
            self.config = self.component.get_config()

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="MAA GTK")

        button = Gtk.Button(label="点击我啊")
        button.connect("clicked", self.create_new_task)
        self.add(button)

    def create_new_task(self, button):
        dialog = CreateTaskDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print('OK')
            print(dialog.type)
            print(dialog.config)
        elif response == Gtk.ResponseType.CANCEL:
            print('Cancel')

        dialog.destroy()

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
