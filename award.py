from gi.repository import Gtk

class AwardConfigBox(Gtk.Box):
    def __init__(self, config = {}):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)

    def get_config(self):
        return {}
