#!/usr/bin/env  python3
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from xdg import DesktopEntry


path_filename = str(sys.argv[1])
deskfile = DesktopEntry.DesktopEntry(path_filename)
name = deskfile.getName()
exe = deskfile.getExec()
comment = deskfile.getComment()

icon_theme = Gtk.IconTheme.get_default()
file_icon = icon_theme.lookup_icon(deskfile.getIcon(), 64, 0)
if file_icon:
	icon = file_icon.get_filename()
else:
	icon = "None"

print ('%s' % (icon))


#print ('NAME = %s\nEXEC = %s\nICON = %s\nCOMMENT = %s' % (name, exe, icon, comment))
