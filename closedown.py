from gui import Gtk

class CloseDownConfigBox(Gtk.Box):
    def __init__(self, config = {}):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.label = Gtk.Label(label="没有什么可以配置的喵～")
        self.pack_start(self.label, False, False, 0)

    def get_config(self):
        return {}

__all__ = ['CloseDownConfigBox']
