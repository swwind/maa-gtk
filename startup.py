from gui import Gtk

class StartUpConfigBox(Gtk.Box):
    def __init__(self, config = {}):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        # client type
        self.client_type_label = Gtk.Label(label="指定客户端版本")
        self.client_type_label.set_halign(Gtk.Align.END)
        self.client_type_combo = Gtk.ComboBoxText()
        self.client_type_combo.append("", "默认")
        self.client_type_combo.append("Official", "Official")
        self.client_type_combo.append("Bilibili", "Bilibili")
        self.client_type_combo.append("txwy", "txwy")
        self.client_type_combo.append("YoStarEN", "YoStarEN")
        self.client_type_combo.append("YoStarJP", "YoStarJP")
        self.client_type_combo.append("YoStarKR", "YoStarKR")
        self.client_type_combo.set_active_id(config.get("client_type", ""))
        self.client_type_combo.set_hexpand(True)
        grid.attach(self.client_type_label, 0, 0, 1, 1)
        grid.attach(self.client_type_combo, 1, 0, 1, 1)

        # start game checkbox
        self.start_game_check = Gtk.CheckButton(label="自动启动客户端")
        self.start_game_check.set_active(config.get("start_game_enabled", False))
        grid.attach(self.start_game_check, 0, 1, 2, 1)

        # account name
        self.account_name_usage_checkbox = Gtk.CheckButton(label="切换账号")
        self.account_name_usage_checkbox.set_active("account_name" in config)
        grid.attach(self.account_name_usage_checkbox, 0, 2, 2, 1)

        self.account_name_label = Gtk.Label(label="账号名称")
        self.account_name_label.set_halign(Gtk.Align.END)
        self.account_name_entry = Gtk.Entry()
        self.account_name_entry.set_text(config.get("account_name", ""))
        self.account_name_entry.set_hexpand(True)
        grid.attach(self.account_name_label, 0, 3, 1, 1)
        grid.attach(self.account_name_entry, 1, 3, 1, 1)

        self.account_name_usage_checkbox.connect("toggled", self.update_sensitives)

        self.update_sensitives(None)

        self.add(grid)

    def update_sensitives(self, _):
        switch_account_name = self.account_name_usage_checkbox.get_active()
        self.account_name_label.set_sensitive(switch_account_name)
        self.account_name_entry.set_sensitive(switch_account_name)

    def get_config(self):
        config = {
            "client_type": self.client_type_combo.get_active_id(),
            "start_game_enabled": self.start_game_check.get_active()
        }
        if self.account_name_usage_checkbox.get_active():
            config["account_name"] = self.account_name_entry.get_text()
        return config

__all__ = ['StartUpConfigBox']
