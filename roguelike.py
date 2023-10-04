from gui import Gtk

class RoguelikeConfigBox(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        # theme
        self.theme_label = Gtk.Label(label="肉鸽名称")
        self.theme_label.set_halign(Gtk.Align.END)
        self.theme_combo = Gtk.ComboBoxText()
        themes = [
            "傀影与猩红血钻 - Phantom",
            "水月与深蓝之树 - Mizuki",
            "探索者的银凇止境 - Sami" ]
        for t in themes:
            self.theme_combo.append_text(t)
        self.theme_combo.set_active(0)
        self.theme_combo.set_hexpand(True)
        grid.attach(self.theme_label, 0, 0, 1, 1)
        grid.attach(self.theme_combo, 1, 0, 1, 1)

        # mode
        self.mode_label = Gtk.Label(label="模式")
        self.mode_label.set_halign(Gtk.Align.END)
        self.mode_combo = Gtk.ComboBoxText()
        modes = [
            "刷蜡烛，尽可能稳定地打更多层数",
            "刷源石锭，第一层投资完就退出",
            "【即将弃用】两者兼顾，投资过后再退出，没有投资就继续往后打" ]
        for t in modes:
            self.mode_combo.append_text(t)
        self.mode_combo.set_active(0)
        self.mode_combo.set_hexpand(True)
        grid.attach(self.mode_label, 0, 1, 1, 1)
        grid.attach(self.mode_combo, 1, 1, 1, 1)

        # starts count
        self.starts_count_label = Gtk.Label(label="开始探索次数")
        self.starts_count_label.set_halign(Gtk.Align.END)
        self.starts_count_spinbutton_adjustment = Gtk.Adjustment(value=99999999, lower=0, upper=2147483647, step_increment=1)
        self.starts_count_spinbutton = Gtk.SpinButton()
        self.starts_count_spinbutton.set_adjustment(self.starts_count_spinbutton_adjustment)
        self.starts_count_spinbutton.set_numeric(True)
        self.starts_count_spinbutton.set_hexpand(True)
        grid.attach(self.starts_count_label, 0, 2, 1, 1)
        grid.attach(self.starts_count_spinbutton, 1, 2, 1, 1)

        # investment enabled
        self.investment_enabled_check = Gtk.CheckButton(label="投资源石锭")
        self.investment_enabled_check.set_active(True)
        self.investment_enabled_check.connect("toggled", self.on_investment_enabled_check_toggled)
        grid.attach(self.investment_enabled_check, 0, 3, 2, 1)

        # investments count
        self.investments_count_label = Gtk.Label(label="投资源石锭次数")
        self.investments_count_label.set_halign(Gtk.Align.END)
        self.investments_count_spinbutton_adjustment = Gtk.Adjustment(value=99999999, lower=0, upper=2147483647, step_increment=1)
        self.investments_count_spinbutton = Gtk.SpinButton()
        self.investments_count_spinbutton.set_adjustment(self.investments_count_spinbutton_adjustment)
        self.investments_count_spinbutton.set_numeric(True)
        self.investments_count_spinbutton.set_hexpand(True)
        grid.attach(self.investments_count_label, 0, 4, 1, 1)
        grid.attach(self.investments_count_spinbutton, 1, 4, 1, 1)

        # stop when investment full
        self.stop_when_investment_full_check = Gtk.CheckButton(label="投资满了自动停止任务")
        grid.attach(self.stop_when_investment_full_check, 0, 5, 2, 1)

        # squad
        self.squad_label = Gtk.Label(label="开局分队")
        self.squad_label.set_halign(Gtk.Align.END)
        self.squad_entry = Gtk.Entry()
        self.squad_entry.set_placeholder_text("指挥分队")
        self.squad_entry.set_hexpand(True)
        grid.attach(self.squad_label, 0, 6, 1, 1)
        grid.attach(self.squad_entry, 1, 6, 1, 1)

        # roles
        self.roles_label = Gtk.Label(label="开局职业组")
        self.roles_label.set_halign(Gtk.Align.END)
        self.roles_entry = Gtk.Entry()
        self.roles_entry.set_placeholder_text("取长补短")
        self.roles_entry.set_hexpand(True)
        grid.attach(self.roles_label, 0, 7, 1, 1)
        grid.attach(self.roles_entry, 1, 7, 1, 1)

        # core char
        self.core_char_label = Gtk.Label(label="开局干员名")
        self.core_char_label.set_halign(Gtk.Align.END)
        self.core_char_entry = Gtk.Entry()
        self.core_char_entry.set_placeholder_text("仅支持单个干员中文名")
        self.core_char_entry.set_hexpand(True)
        grid.attach(self.core_char_label, 0, 8, 1, 1)
        grid.attach(self.core_char_entry, 1, 8, 1, 1)

        # use support
        self.use_support_check = Gtk.CheckButton(label="开局使用助战干员")
        grid.attach(self.use_support_check, 0, 9, 2, 1)

        # use nonfriend support
        self.use_nonfriend_support_check = Gtk.CheckButton(label="使用非好友助战干员")
        grid.attach(self.use_nonfriend_support_check, 0, 10, 2, 1)

        # refresh trader with dice
        self.refresh_trader_with_dice_check = Gtk.CheckButton(label="用骰子刷新商店（仅限水月肉鸽）")
        grid.attach(self.refresh_trader_with_dice_check, 0, 11, 2, 1)

        self.add(grid)

    def on_investment_enabled_check_toggled(self, checkbox):
        is_checked = checkbox.get_active()
        self.investments_count_label.set_sensitive(is_checked)
        self.investments_count_spinbutton.set_sensitive(is_checked)

__all__ = ['RoguelikeConfigBox']
