from gi.repository import Gtk

class RoguelikeConfigBox(Gtk.Box):
    def __init__(self, config = {}):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        # theme
        self.theme_label = Gtk.Label(label="肉鸽名称")
        self.theme_label.set_halign(Gtk.Align.END)
        self.theme_combo = Gtk.ComboBoxText()
        self.theme_combo.append("Phantom", "傀影与猩红血钻 - Phantom")
        self.theme_combo.append("Mizuki", "水月与深蓝之树 - Mizuki")
        self.theme_combo.append("Sami", "探索者的银凇止境 - Sami")
        self.theme_combo.set_active_id(config.get("theme", "Phantom"))
        self.theme_combo.set_hexpand(True)
        grid.attach(self.theme_label, 0, 0, 1, 1)
        grid.attach(self.theme_combo, 1, 0, 1, 1)

        # mode
        self.mode_label = Gtk.Label(label="模式")
        self.mode_label.set_halign(Gtk.Align.END)
        self.mode_combo = Gtk.ComboBoxText()
        self.mode_combo.append("0", "刷蜡烛，尽可能稳定地打更多层数")
        self.mode_combo.append("1", "刷源石锭，第一层投资完就退出")
        self.mode_combo.append("2", "【即将弃用】两者兼顾，投资过后再退出，没有投资就继续往后打")
        self.mode_combo.set_active_id(str(config.get("mode", 0)))
        self.mode_combo.set_hexpand(True)
        grid.attach(self.mode_label, 0, 1, 1, 1)
        grid.attach(self.mode_combo, 1, 1, 1, 1)

        # starts count
        self.starts_count_label = Gtk.Label(label="开始探索次数")
        self.starts_count_label.set_halign(Gtk.Align.END)
        self.starts_count_spinbutton = Gtk.SpinButton()
        self.starts_count_spinbutton.set_hexpand(True)
        self.starts_count_spinbutton.set_range(0, 2147483647)
        self.starts_count_spinbutton.set_value(config.get("starts_count", 99999999))
        self.starts_count_spinbutton.set_increments(1, 10)
        grid.attach(self.starts_count_label, 0, 2, 1, 1)
        grid.attach(self.starts_count_spinbutton, 1, 2, 1, 1)

        # investment enabled
        self.investment_enabled_check = Gtk.CheckButton(label="投资源石锭")
        self.investment_enabled_check.set_active(config.get("investment_enabled", True))
        grid.attach(self.investment_enabled_check, 0, 3, 2, 1)

        # investments count
        self.investments_count_label = Gtk.Label(label="投资源石锭次数")
        self.investments_count_label.set_halign(Gtk.Align.END)
        self.investments_count_spinbutton = Gtk.SpinButton()
        self.investments_count_spinbutton.set_hexpand(True)
        self.investments_count_spinbutton.set_range(0, 2147483647)
        self.investments_count_spinbutton.set_value(config.get("investments_count", 99999999))
        self.investments_count_spinbutton.set_increments(1, 10)
        grid.attach(self.investments_count_label, 0, 4, 1, 1)
        grid.attach(self.investments_count_spinbutton, 1, 4, 1, 1)

        # stop when investment full
        self.stop_when_investment_full_check = Gtk.CheckButton(label="投资满了自动停止任务")
        self.stop_when_investment_full_check.set_active(config.get("stop_when_investment_full", False))
        grid.attach(self.stop_when_investment_full_check, 0, 5, 2, 1)

        # squad
        self.squad_label = Gtk.Label(label="开局分队")
        self.squad_label.set_halign(Gtk.Align.END)
        self.squad_entry = Gtk.Entry()
        self.squad_entry.set_text(config.get("squad", "指挥分队"))
        self.squad_entry.set_hexpand(True)
        grid.attach(self.squad_label, 0, 6, 1, 1)
        grid.attach(self.squad_entry, 1, 6, 1, 1)

        # roles
        self.roles_label = Gtk.Label(label="开局职业组")
        self.roles_label.set_halign(Gtk.Align.END)
        self.roles_entry = Gtk.Entry()
        self.roles_entry.set_text(config.get("roles", "取长补短"))
        self.roles_entry.set_hexpand(True)
        grid.attach(self.roles_label, 0, 7, 1, 1)
        grid.attach(self.roles_entry, 1, 7, 1, 1)

        # core char
        self.core_char_label = Gtk.Label(label="开局干员名")
        self.core_char_label.set_halign(Gtk.Align.END)
        self.core_char_entry = Gtk.Entry()
        self.core_char_entry.set_placeholder_text("仅支持单个干员中文名")
        self.core_char_entry.set_text(config.get("core_char", ""))
        self.core_char_entry.set_hexpand(True)
        grid.attach(self.core_char_label, 0, 8, 1, 1)
        grid.attach(self.core_char_entry, 1, 8, 1, 1)

        # use support
        self.use_support_check = Gtk.CheckButton(label="开局使用助战干员")
        self.use_support_check.set_active(config.get("use_support", False))
        grid.attach(self.use_support_check, 0, 9, 2, 1)

        # use nonfriend support
        self.use_nonfriend_support_check = Gtk.CheckButton(label="使用非好友助战干员")
        self.use_nonfriend_support_check.set_active(config.get("use_nonfriend_support", False))
        grid.attach(self.use_nonfriend_support_check, 0, 10, 2, 1)

        # refresh trader with dice
        self.refresh_trader_with_dice_check = Gtk.CheckButton(label="用骰子刷新商店（仅限水月肉鸽）")
        self.refresh_trader_with_dice_check.set_active(config.get("refresh_trader_with_dice", False))
        grid.attach(self.refresh_trader_with_dice_check, 0, 11, 2, 1)

        self.investment_enabled_check.connect("toggled", self.update_sensitives)

        self.update_sensitives(None)

        self.add(grid)

    def update_sensitives(self, _):
        investment_enabled = self.investment_enabled_check.get_active()
        self.investments_count_label.set_sensitive(investment_enabled)
        self.investments_count_spinbutton.set_sensitive(investment_enabled)
        self.stop_when_investment_full_check.set_sensitive(investment_enabled)

    def get_config(self):
        config = {
            "theme": self.theme_combo.get_active_id(),
            "mode": int(self.mode_combo.get_active_id()),
            "starts_count": self.starts_count_spinbutton.get_value_as_int(),
            "investment_enabled": self.investment_enabled_check.get_active(),
            "investments_count": self.investments_count_spinbutton.get_value_as_int(),
            "stop_when_investment_full": self.stop_when_investment_full_check.get_active(),
            "squad": self.squad_entry.get_text(),
            "roles": self.roles_entry.get_text(),
            "core_char": self.core_char_entry.get_text(),
            "use_support": self.use_support_check.get_active(),
            "use_nonfriend_support": self.use_nonfriend_support_check.get_active(),
            "refresh_trader_with_dice": self.refresh_trader_with_dice_check.get_active(),
        }

        return config
