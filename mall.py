from gi.repository import Gtk

class MallConfigBox(Gtk.Box):
    def __init__(self, config={}):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        # shopping
        self.shopping_check = Gtk.CheckButton(label="是否购物")
        self.shopping_check.set_active(config.get("shopping", True))
        grid.attach(self.shopping_check, 0, 0, 2, 1)

        # buy_first
        self.buy_first_label = Gtk.Label(label="优先购买列表")
        self.buy_first_label.set_halign(Gtk.Align.END)
        self.buy_first_entry = Gtk.Entry()
        buy_first_text = ", ".join(config.get("buy_first", ["招聘许可", "龙门币"]))
        self.buy_first_entry.set_text(buy_first_text)
        self.buy_first_entry.set_hexpand(True)
        grid.attach(self.buy_first_label, 0, 1, 1, 1)
        grid.attach(self.buy_first_entry, 1, 1, 1, 1)

        # blacklist
        self.blacklist_label = Gtk.Label(label="黑名单列表")
        self.blacklist_label.set_halign(Gtk.Align.END)
        self.blacklist_entry = Gtk.Entry()
        blacklist_text = ", ".join(config.get("blacklist", ["加急许可", "家具零件"]))
        self.blacklist_entry.set_text(blacklist_text)
        self.blacklist_entry.set_hexpand(True)
        grid.attach(self.blacklist_label, 0, 2, 1, 1)
        grid.attach(self.blacklist_entry, 1, 2, 1, 1)

        # force_shopping_if_credit_full
        self.force_shopping_check = Gtk.CheckButton(label="信用溢出时无视黑名单")
        self.force_shopping_check.set_active(config.get("force_shopping_if_credit_full", True))
        grid.attach(self.force_shopping_check, 0, 3, 2, 1)

        self.add(grid)

    def get_config(self):
        config = {
            "shopping": self.shopping_check.get_active(),
            "buy_first": [item.strip() for item in self.buy_first_entry.get_text().split(",")],
            "blacklist": [item.strip() for item in self.blacklist_entry.get_text().split(",")],
            "force_shopping_if_credit_full": self.force_shopping_check.get_active(),
        }
        return config

__all__ = ['MallConfigBox']
