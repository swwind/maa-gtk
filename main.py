from fight import FightConfigBox
from gui import Gtk
from recruit import RecruitConfigBox, default_recruit_config

from roguelike import RoguelikeConfigBox
from startup import StartUpConfigBox

class ItemList(Gtk.ListBox):
    def __init__(self, detail_panel):
        Gtk.ListBox.__init__(self)
        self.set_size_request(200, -1)
        self.set_selection_mode(Gtk.SelectionMode.SINGLE)

        items = ["Roguelike", "Fight"]
        for item in items:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=item)
            row.add(label)
            self.add(row)

        self.connect("row-selected", self.on_row_selected)
        self.detail_panel = detail_panel

    def on_row_selected(self, _listbox, row):
        index = row.get_index()
        print(f"选择了 {index}")

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Item List Demo")
        self.set_default_size(1280, 720)
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=10)
        self.add(hbox)

        detail_panel = RecruitConfigBox()
        item_list = ItemList(detail_panel)

        hbox.pack_start(item_list, False, False, 0)
        hbox.pack_start(detail_panel, True, True, 0)

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
