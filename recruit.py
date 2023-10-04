from gui import Gtk

stars = [1, 2, 3, 4, 5, 6]
servers = ["CN", "US", "JP", "KR"]

class RecruitConfigBox(Gtk.Box):
    def __init__(self, config = {}):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        # 刷新三星标签
        self.refresh_check = Gtk.CheckButton(label="刷新三星标签")
        self.refresh_check.set_active(config.get('refresh', False))
        grid.attach(self.refresh_check, 0, 0, 2, 1)

        # 点击标签的等级
        self.select_label = Gtk.Label(label="点击标签等级")
        self.select_label.set_halign(Gtk.Align.END)
        self.select_box = Gtk.Box(spacing=10)
        self.select_checkboxes = []
        for star in stars:
            checkbox = Gtk.CheckButton(label=str(star))
            checkbox.set_active(star in config.get('select', [4]))
            self.select_checkboxes.append(checkbox)
            self.select_box.add(checkbox)
        self.select_box.set_hexpand(True)
        grid.attach(self.select_label, 0, 1, 1, 1)
        grid.attach(self.select_box, 1, 1, 1, 1)

        # 点击确认的等级
        self.confirm_label = Gtk.Label(label="点击确认等级")
        self.confirm_label.set_halign(Gtk.Align.END)
        self.confirm_box = Gtk.Box(spacing=10)
        self.confirm_checkboxes = []
        for star in stars:
            checkbox = Gtk.CheckButton(label=star)
            checkbox.set_active(star in config.get('confirm', [3, 4]))
            self.confirm_checkboxes.append(checkbox)
            self.confirm_box.add(checkbox)
        self.confirm_box.set_hexpand(True)
        grid.attach(self.confirm_label, 0, 2, 1, 1)
        grid.attach(self.confirm_box, 1, 2, 1, 1)

        # 招募次数
        self.times_label = Gtk.Label(label="招募次数")
        self.times_label.set_halign(Gtk.Align.END)
        self.times_spinbutton_adjustment = Gtk.Adjustment(value=4, lower=0, upper=2147483647, step_increment=1)
        self.times_spinbutton = Gtk.SpinButton()
        self.times_spinbutton.set_adjustment(self.times_spinbutton_adjustment)
        self.times_spinbutton.set_numeric(True)
        self.times_spinbutton.set_value(config.get('times', 4))
        self.times_spinbutton.set_hexpand(True)
        grid.attach(self.times_label, 0, 3, 1, 1)
        grid.attach(self.times_spinbutton, 1, 3, 1, 1)

        # 设置招募时限
        self.set_time_check = Gtk.CheckButton(label="设置招募时限")
        self.set_time_check.set_active(config.get('set_time', True))
        grid.attach(self.set_time_check, 0, 4, 2, 1)

        # 使用加急许可
        self.expedite_check = Gtk.CheckButton(label="使用加急许可")
        self.expedite_check.set_active(config.get('expedite', False))
        grid.attach(self.expedite_check, 0, 5, 2, 1)

        # 加急次数
        self.expedite_times_label = Gtk.Label(label="加急次数")
        self.expedite_times_label.set_halign(Gtk.Align.END)
        self.expedite_times_spinbutton_adjustment = Gtk.Adjustment(value=99999999, lower=0, upper=2147483647, step_increment=1)
        self.expedite_times_spinbutton = Gtk.SpinButton()
        self.expedite_times_spinbutton.set_adjustment(self.expedite_times_spinbutton_adjustment)
        self.expedite_times_spinbutton.set_value(config.get('expedite_times', 99999999))
        self.expedite_times_spinbutton.set_numeric(True)
        self.expedite_times_spinbutton.set_hexpand(True)
        grid.attach(self.expedite_times_label, 0, 6, 1, 1)
        grid.attach(self.expedite_times_spinbutton, 1, 6, 1, 1)
        
        # 跳过小车词条
        self.skip_robot_check = Gtk.CheckButton(label="跳过小车词条")
        self.skip_robot_check.set_active(config.get('skip_robot', True))
        grid.attach(self.skip_robot_check, 0, 7, 2, 1)
        
        # 汇报企鹅物流
        self.report_penguin_check = Gtk.CheckButton(label="汇报企鹅物流")
        self.report_penguin_check.set_active(config.get('report_to_penguin', False))
        grid.attach(self.report_penguin_check, 0, 8, 2, 1)

        self.penguin_id_label = Gtk.Label(label="企鹅物流 ID")
        self.penguin_id_label.set_halign(Gtk.Align.END)
        self.penguin_id_entry = Gtk.Entry()
        self.penguin_id_entry.set_text(config.get('penguin_id', ''))
        self.penguin_id_entry.set_hexpand(True)
        grid.attach(self.penguin_id_label, 0, 9, 1, 1)
        grid.attach(self.penguin_id_entry, 1, 9, 1, 1)
        
        # 汇报一图流
        self.report_yituliu_check = Gtk.CheckButton(label="汇报一图流")
        self.report_yituliu_check.set_active(config.get('report_to_yituliu', False))
        grid.attach(self.report_yituliu_check, 0, 10, 2, 1)

        self.yituliu_id_label = Gtk.Label(label="一图流 ID")
        self.yituliu_id_label.set_halign(Gtk.Align.END)
        self.yituliu_id_entry = Gtk.Entry()
        self.yituliu_id_entry.set_text(config.get('yituliu_id', ''))
        self.yituliu_id_entry.set_hexpand(True)
        grid.attach(self.yituliu_id_label, 0, 11, 1, 1)
        grid.attach(self.yituliu_id_entry, 1, 11, 1, 1)

        # 服务器，企鹅物流和一图流共用
        self.server_label = Gtk.Label(label="服务器")
        self.server_label.set_halign(Gtk.Align.END)
        self.server_combo = Gtk.ComboBoxText()
        for s in servers:
            self.server_combo.append_text(s)
        try:
            self.server_combo.set_active(servers.index(config.get('server', "CN")))
        except:
            self.server_combo.set_active(0)
        self.server_combo.set_hexpand(True)
        grid.attach(self.server_label, 0, 12, 1, 1)
        grid.attach(self.server_combo, 1, 12, 1, 1)

        self.expedite_check.connect("toggled", self.update_sensitive)
        self.report_penguin_check.connect("toggled", self.update_sensitive)
        self.report_yituliu_check.connect("toggled", self.update_sensitive)

        self.update_sensitive(None)

        self.add(grid)

    def update_sensitive(self, _):
        expedite = self.expedite_check.get_active()
        report_to_penguin = self.report_penguin_check.get_active()
        report_to_yituliu = self.report_yituliu_check.get_active()

        self.expedite_times_label.set_sensitive(expedite)
        self.expedite_times_spinbutton.set_sensitive(expedite)
        self.penguin_id_label.set_sensitive(report_to_penguin)
        self.penguin_id_entry.set_sensitive(report_to_penguin)
        self.yituliu_id_label.set_sensitive(report_to_yituliu)
        self.yituliu_id_entry.set_sensitive(report_to_yituliu)
        self.server_label.set_sensitive(report_to_penguin or report_to_yituliu)
        self.server_combo.set_sensitive(report_to_penguin or report_to_yituliu)

        print(self.get_config())

    def get_config(self):
        config = {
            "refresh": self.refresh_check.get_active(),
            "select": [stars[i] for i, checkbox in enumerate(self.select_checkboxes) if checkbox.get_active()],
            "confirm": [stars[i] for i, checkbox in enumerate(self.confirm_checkboxes) if checkbox.get_active()],
            "times": int(self.times_spinbutton.get_text()),
            "set_time": self.set_time_check.get_active(),
            "expedite": self.expedite_check.get_active(),
            "expedite_times": int(self.expedite_times_spinbutton.get_text()),
            "skip_robot": self.skip_robot_check.get_active(),
            "report_to_penguin": self.report_penguin_check.get_active(),
            "penguin_id": self.penguin_id_entry.get_text(),
            "report_to_yituliu": self.report_yituliu_check.get_active(),
            "yituliu_id": self.yituliu_id_entry.get_text(),
            "server": servers[self.server_combo.get_active()],
        }

        return config

__all__ = ['RecruitConfigBox']
