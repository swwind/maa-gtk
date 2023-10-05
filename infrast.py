from gi.repository import Gtk

class InfrastConfigBox(Gtk.Box):
    def __init__(self, config={}):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        # mode
        self.mode_label = Gtk.Label(label="换班工作模式")
        self.mode_label.set_halign(Gtk.Align.END)
        self.mode_combobox = Gtk.ComboBoxText()
        self.mode_combobox.append("0", "默认换班模式")
        self.mode_combobox.append("10000", "自定义换班模式")
        self.mode_combobox.set_active_id(str(config.get("mode", 0)))
        self.mode_combobox.set_hexpand(True)
        grid.attach(self.mode_label, 0, 0, 1, 1)
        grid.attach(self.mode_combobox, 1, 0, 1, 1)

        # facility
        self.facility_label = Gtk.Label(label="要换班的设施")
        self.facility_label.set_halign(Gtk.Align.END)
        self.facility_entry = Gtk.Entry()
        self.facility_entry.set_text(", ".join(config.get("facility", ["Mfg", "Trade", "Power", "Control", "Reception", "Office", "Dorm"])))
        self.facility_entry.set_hexpand(True)
        grid.attach(self.facility_label, 0, 1, 1, 1)
        grid.attach(self.facility_entry, 1, 1, 1, 1)

        # drones
        self.drones_label = Gtk.Label(label="无人机用途")
        self.drones_label.set_halign(Gtk.Align.END)
        self.drones_combo = Gtk.ComboBoxText()
        self.drones_combo.append("_NotUse", "不使用")
        self.drones_combo.append("Money", "加速龙门币")
        self.drones_combo.append("SyntheticJade", "加速合成玉")
        self.drones_combo.append("CombatRecord", "加速作战记录")
        self.drones_combo.append("PureGold", "加速赤金")
        self.drones_combo.append("OriginStone", "加速源石碎片")
        self.drones_combo.append("Chip", "加速芯片")
        self.drones_combo.set_active_id(config.get("drones", "_NotUse"))
        self.drones_combo.set_hexpand(True)
        grid.attach(self.drones_label, 0, 2, 1, 1)
        grid.attach(self.drones_combo, 1, 2, 1, 1)

        # threshold
        self.threshold_label = Gtk.Label(label="工作心情阈值")
        self.threshold_label.set_halign(Gtk.Align.END)
        self.threshold_scale_adjustment = Gtk.Adjustment(
            value=config.get("threshold", 0.3),
            lower=0, upper=1, step_increment=0.01)
        self.threshold_scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL,
            adjustment=self.threshold_scale_adjustment)
        self.threshold_scale.set_digits(2)
        self.threshold_scale.set_hexpand(True)
        grid.attach(self.threshold_label, 0, 3, 1, 1)
        grid.attach(self.threshold_scale, 1, 3, 1, 1)

        # replenish
        self.replenish_check = Gtk.CheckButton(label="贸易站“源石碎片”自动补货")
        self.replenish_check.set_active(config.get("replenish", False))
        grid.attach(self.replenish_check, 0, 4, 2, 1)

        # dorm_notstationed_enabled
        self.dorm_notstationed_enabled_check = Gtk.CheckButton(label="启用宿舍“未进驻”选项")
        self.dorm_notstationed_enabled_check.set_active(config.get("dorm_notstationed_enabled", False))
        grid.attach(self.dorm_notstationed_enabled_check, 0, 5, 2, 1)

        # dorm_trust_enabled
        self.dorm_trust_enabled_check = Gtk.CheckButton(label="将宿舍剩余位置填入信赖未满干员")
        self.dorm_trust_enabled_check.set_active(config.get("dorm_trust_enabled", False))
        grid.attach(self.dorm_trust_enabled_check, 0, 6, 2, 1)

        self.add(grid)

    def get_config(self):
        config = {
            "mode": int(self.mode_combobox.get_active_id()),
            "facility": [f.strip() for f in self.facility_entry.get_text().split(",")],
            "drones": self.drones_combo.get_active_id(),
            "threshold": self.threshold_scale.get_value(),
            "replenish": self.replenish_check.get_active(),
            "dorm_notstationed_enabled": self.dorm_notstationed_enabled_check.get_active(),
            "dorm_trust_enabled": self.dorm_trust_enabled_check.get_active(),
        }
        return config
