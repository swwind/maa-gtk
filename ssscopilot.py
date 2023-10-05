from gi.repository import Gtk

class SSSCopilotConfigBox(Gtk.Box):
    def __init__(self, config={}):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        # filename label
        self.filename_label = Gtk.Label(label="作业文件路径")
        self.filename_label.set_halign(Gtk.Align.END)
        grid.attach(self.filename_label, 0, 0, 1, 1)

        # filename entry
        self.filename_entry = Gtk.Entry()
        self.filename_entry.set_text(config.get("filename", ""))
        self.filename_entry.set_hexpand(True)
        grid.attach(self.filename_entry, 1, 0, 1, 1)

        # filename button
        self.filename_button = Gtk.Button(label="选择文件")
        self.filename_button.connect("clicked", self.on_file_button_clicked)
        grid.attach(self.filename_button, 2, 0, 1, 1)

        # loop times label
        self.loop_times_label = Gtk.Label(label="循环执行次数")
        self.loop_times_label.set_halign(Gtk.Align.END)
        grid.attach(self.loop_times_label, 0, 1, 1, 1)

        # loop times adjustment
        adjustment = Gtk.Adjustment(
            value=config.get("loop_times", 1),
            lower=0,
            upper=2147483647,
            step_increment=1,
            page_increment=10
        )

        # loop times spin button
        self.loop_times_spin = Gtk.SpinButton()
        self.loop_times_spin.set_adjustment(adjustment)
        grid.attach(self.loop_times_spin, 1, 1, 2, 1)

        self.add(grid)

    def on_file_button_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="选择作业文件",
            parent=None,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        # 添加文件过滤器
        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON 文件")
        filter_json.add_mime_type("application/json")
        dialog.add_filter(filter_json)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.filename_entry.set_text(filename)

        dialog.destroy()

    def get_config(self):
        config = {
            "filename": self.filename_entry.get_text(),
            "loop_times": self.loop_times_spin.get_value_as_int()
        }
        return config
