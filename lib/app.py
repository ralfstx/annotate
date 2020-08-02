import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from .main_window import MainWindow

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.example.myapp",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )
        self.window = None

        self.add_main_option(
            "test",
            ord("t"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Command line test",
            None,
        )

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(self)
        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()
        if "test" in options:
            print("Test argument received: %s" % options["test"])

        self.activate()
        return 0
