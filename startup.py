from gui import Gtk

class StartUpConfigBox(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        # client type
        self.client_type_label = Gtk.Label(label="指定客户端版本")
        self.client_type_label.set_halign(Gtk.Align.END)
        self.client_type_combo = Gtk.ComboBoxText()
        client_types = ["Official", "Bilibili", "txwy", "YoStarEN", "YoStarJP", "YoStarKR"]
        for t in client_types:
            self.client_type_combo.append_text(t)
        self.client_type_combo.set_active(0)
        self.client_type_combo.set_hexpand(True)
        grid.attach(self.client_type_label, 0, 0, 1, 1)
        grid.attach(self.client_type_combo, 1, 0, 1, 1)

        # start game checkbox
        self.start_game_check = Gtk.CheckButton(label="自动启动客户端")
        grid.attach(self.start_game_check, 0, 1, 2, 1)

        # account name
        self.account_name_usage_checkbox = Gtk.CheckButton(label="切换账号")
        grid.attach(self.account_name_usage_checkbox, 0, 2, 2, 1)

        self.account_name_label = Gtk.Label(label="账号名称")
        self.account_name_label.set_halign(Gtk.Align.END)
        self.account_name_entry = Gtk.Entry()
        self.account_name_entry.set_hexpand(True)
        grid.attach(self.account_name_label, 0, 3, 1, 1)
        grid.attach(self.account_name_entry, 1, 3, 1, 1)

        self.account_name_usage_checkbox.connect("toggled", self.on_account_name_checkbox_toggled)
        self.account_name_label.set_sensitive(False)
        self.account_name_entry.set_sensitive(False)

        self.add(grid)

    def on_account_name_checkbox_toggled(self, checkbox):
        is_checked = checkbox.get_active()
        self.account_name_label.set_sensitive(is_checked)
        self.account_name_entry.set_sensitive(is_checked)

__all__ = ['StartUpConfigBox']
