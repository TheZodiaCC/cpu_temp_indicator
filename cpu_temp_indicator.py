import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import GObject
from threading import Thread
import time

class MyIndicator():
    def __init__(self):
        self.app = "cpu_temp_indicator"
        iconpath = ""
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label("--°C", self.app)

        self.update = Thread(target=self.show_temp)
        self.update.setDaemon(True)
        self.update.start()

    def create_menu(self):
        menu = Gtk.Menu()
        name = Gtk.MenuItem("CPU Temp Indicator")
        name.set_sensitive(False)
        menu.append(name)
        sep = Gtk.SeparatorMenuItem()
        menu.append(sep)
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def show_temp(self):
        file = "/sys/class/thermal/thermal_zone0/temp"
        while True:
            with open(file) as data:
                mention = f"{(data.read())[:2]}°C"
            GObject.idle_add(self.indicator.set_label, mention, self.app, priority=GObject.PRIORITY_DEFAULT)
            time.sleep(3)

    def stop(self, source):
        Gtk.main_quit()

if __name__ == "__main__":

    MyIndicator()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()