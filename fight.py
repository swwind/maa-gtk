from gui import Gtk

servers = ["CN", "US", "JP", "KR"]
client_types = ["Official", "Bilibili", "txwy", "YoStarEN", "YoStarJP", "YoStarKR"]

class FightConfigBox(Gtk.Box):
    def __init__(self, config = {}):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)

        # stage
        self.stage_label = Gtk.Label(label="关卡名")
        self.stage_label.set_halign(Gtk.Align.END)
        self.stage_entry = Gtk.Entry()
        self.stage_entry.set_placeholder_text("默认上次作战")
        self.stage_entry.set_text(config.get("stage", ""))
        self.stage_entry.set_hexpand(True)
        grid.attach(self.stage_label, 0, 0, 1, 1)
        grid.attach(self.stage_entry, 1, 0, 1, 1)

        # medicine
        self.medicine_label = Gtk.Label(label="使用理智药数量")
        self.medicine_label.set_halign(Gtk.Align.END)
        self.medicine_spin = Gtk.SpinButton()
        self.medicine_spin.set_hexpand(True)
        self.medicine_spin.set_range(0, 2147483647)
        self.medicine_spin.set_value(config.get("medicine", 0))
        self.medicine_spin.set_increments(1, 10)
        grid.attach(self.medicine_label, 0, 1, 1, 1)
        grid.attach(self.medicine_spin, 1, 1, 1, 1)

        # expiring medicine
        self.expiring_medicine_label = Gtk.Label(label="使用快过期理智药数量")
        self.expiring_medicine_label.set_halign(Gtk.Align.END)
        self.expiring_medicine_spin = Gtk.SpinButton()
        self.expiring_medicine_spin.set_hexpand(True)
        self.expiring_medicine_spin.set_range(0, 2147483647)
        self.expiring_medicine_spin.set_value(config.get("expiring_medicine", 0))
        self.expiring_medicine_spin.set_increments(1, 10)
        grid.attach(self.expiring_medicine_label, 0, 2, 1, 1)
        grid.attach(self.expiring_medicine_spin, 1, 2, 1, 1)

        # stone
        self.stone_label = Gtk.Label(label="吃石头数量")
        self.stone_label.set_halign(Gtk.Align.END)
        self.stone_spin = Gtk.SpinButton()
        self.stone_spin.set_hexpand(True)
        self.stone_spin.set_range(0, 2147483647)
        self.stone_spin.set_value(config.get("stone", 0))
        self.stone_spin.set_increments(1, 10)
        grid.attach(self.stone_label, 0, 3, 1, 1)
        grid.attach(self.stone_spin, 1, 3, 1, 1)

        # times
        self.times_label = Gtk.Label(label="刷取次数")
        self.times_label.set_halign(Gtk.Align.END)
        self.times_spin = Gtk.SpinButton()
        self.times_spin.set_hexpand(True)
        self.times_spin.set_range(0, 2147483647)
        self.times_spin.set_value(config.get("times", 99999999))
        self.times_spin.set_increments(1, 10)
        grid.attach(self.times_label, 0, 4, 1, 1)
        grid.attach(self.times_spin, 1, 4, 1, 1)

        # TODO
        # drops
        self.drops_label = Gtk.Label(label="指定掉落数量")
        self.drops_label.set_halign(Gtk.Align.END)
        self.drops_entry = Gtk.Entry()
        self.drops_entry.set_hexpand(True)
        grid.attach(self.drops_label, 0, 5, 1, 1)
        grid.attach(self.drops_entry, 1, 5, 1, 1)

        # report to penguin
        self.report_to_penguin_check = Gtk.CheckButton(label="汇报企鹅物流")
        self.report_to_penguin_check.connect("toggled", self.update_sensitive)
        grid.attach(self.report_to_penguin_check, 0, 6, 2, 1)

        # penguin id
        self.penguin_id_label = Gtk.Label(label="企鹅物流汇报 ID")
        self.penguin_id_label.set_halign(Gtk.Align.END)
        self.penguin_id_entry = Gtk.Entry()
        self.penguin_id_entry.set_text(config.get("penguin_id", ""))
        self.penguin_id_entry.set_hexpand(True)
        grid.attach(self.penguin_id_label, 0, 7, 1, 1)
        grid.attach(self.penguin_id_entry, 1, 7, 1, 1)

        # server
        self.server_label = Gtk.Label(label="服务器")
        self.server_label.set_halign(Gtk.Align.END)
        self.server_combo = Gtk.ComboBoxText()
        for s in servers:
            self.server_combo.append_text(s)
        try:
            self.server_combo.set_active(servers.index(config.get("server", "CN")))
        except:
            self.server_combo.set_active(0)
        self.server_combo.set_hexpand(True)
        grid.attach(self.server_label, 0, 8, 1, 1)
        grid.attach(self.server_combo, 1, 8, 1, 1)

        # client type
        self.client_type_label = Gtk.Label(label="客户端版本")
        self.client_type_label.set_halign(Gtk.Align.END)
        self.client_type_combo = Gtk.ComboBoxText()
        for t in client_types:
            self.client_type_combo.append_text(t)
        try:
            self.client_type_combo.set_active(client_types.index(config.get("client_type", "Official")))
        except:
            self.client_type_combo.set_active(0)
        self.client_type_combo.set_hexpand(True)
        grid.attach(self.client_type_label, 0, 9, 1, 1)
        grid.attach(self.client_type_combo, 1, 9, 1, 1)

        # DrGrandet
        self.drgrandet_check = Gtk.CheckButton(label="节省理智碎石模式")
        self.drgrandet_check.set_active(config.get("DrGrandet", False))
        grid.attach(self.drgrandet_check, 0, 10, 2, 1)

        self.update_sensitive(None)

        self.add(grid)

    def update_sensitive(self, _):
        is_checked = self.report_to_penguin_check.get_active()
        self.penguin_id_label.set_sensitive(is_checked)
        self.penguin_id_entry.set_sensitive(is_checked)
        self.server_label.set_sensitive(is_checked)
        self.server_combo.set_sensitive(is_checked)
        self.client_type_label.set_sensitive(is_checked)
        self.client_type_combo.set_sensitive(is_checked)

    def get_config(self):
        config = {
            "stage": self.stage_entry.get_text(),
            "medicine": int(self.medicine_spin.get_text()),
            "expiring_medicine": int(self.expiring_medicine_spin.get_text()),
            "stone": int(self.stone_spin.get_text()),
            "report_to_penguin": self.report_to_penguin_check.get_active(),
            "penguin_id": self.penguin_id_entry.get_text(),
            "server": servers[self.server_combo.get_active()],
            "client_type": client_types[self.client_type_combo.get_active()],
            "DrGrandet": self.drgrandet_check.get_active()
        }

        return config

__all__ = ['FightConfigBox']