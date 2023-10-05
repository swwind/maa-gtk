from gi.repository import Gtk, Gio

class CopilotConfigBox(Gtk.Box):
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

        # formation check
        self.formation_check = Gtk.CheckButton(label="快捷编队")
        self.formation_check.set_active(config.get("formation", True))
        grid.attach(self.formation_check, 0, 1, 3, 1)

        self.add(grid)

    def on_file_button_clicked(self, _):
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
            "formation": self.formation_check.get_active()
        }
        return config
