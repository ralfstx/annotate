#!/usr/bin/env python

import sys
import signal

from lib.app import Application

if __name__ == "__main__":
    app = Application()
    # https://stackoverflow.com/questions/16410852/keyboard-interrupt-with-with-python-gtk
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
