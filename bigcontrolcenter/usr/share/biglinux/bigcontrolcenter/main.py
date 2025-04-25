#!/usr/bin/env python3
"""
BigControlCenter - A GTK4-based control center for system settings

This is the main entry point for the BigControlCenter application.
"""

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gio

from ui.application import BigControlCenterApp


def main():
    """Main application entry point"""
    app = BigControlCenterApp("bigcontrolcenter", Gio.ApplicationFlags.DEFAULT_FLAGS)
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
