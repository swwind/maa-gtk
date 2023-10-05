from gi.repository import Gtk

class StatusDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "正在运行 MAA", parent, 0, Gtk.ButtonsType.NONE)
        self.set_default_size(335, 518)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textview.set_editable(False)  # 设置文本框为只读

        scrollbar = Gtk.ScrolledWindow()
        scrollbar.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrollbar.add(self.textview)

        area = self.get_content_area()
        area.pack_start(scrollbar, True, True, 0)

        self.show_all()

    def add_text(self, text):
        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.insert(end_iter, text + '\n')
        self.textview.queue_draw()
        
        # 滚动到最下面
        mark = self.textbuffer.create_mark(None, end_iter, False)
        self.textview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)
