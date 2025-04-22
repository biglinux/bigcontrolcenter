"""
BigControlCenter - Device Connection Dialog
Provides information about connecting Android or iOS devices via USB tethering
"""

import gi
import gettext

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gdk, GdkPixbuf

# Setup translations
try:
    lang_translations = gettext.translation(
        "bigcontrolcenter", localedir="/usr/share/locale", fallback=True
    )
    lang_translations.install()
    _ = lang_translations.gettext
except Exception:
    # Fallback if translation fails
    _ = lambda x: x


class DeviceConnectionDialog:
    """Dialog for showing USB tethering instructions for mobile devices"""

    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.dialog = None

    def show_android_dialog(self):
        """Show dialog with Android USB tethering instructions"""
        title = _("Using Your Android Device's Internet on Linux via USB")
        instructions = [
            _(
                "Connect your Android smartphone to the Linux computer using a USB cable."
            ),
            _(
                "On your smartphone, open 'Settings' and navigate to 'Network & Internet' or 'Connections & Sharing'."
            ),
            _(
                "Look for 'USB Tethering', 'USB Tether', or similar terms and enable it."
            ),
        ]
        note = _(
            "This will automatically establish the internet connection on your Linux computer without requiring any additional configuration."
        )
        warning = _(
            "If your Android device is not connected to Wi-Fi and is using cellular data, this tethering will consume data from your cellular plan. To avoid data charges, ensure that your Android device is connected to a Wi-Fi network before enabling tethering."
        )

        self._show_dialog(title, instructions, note, warning)

    def show_ios_dialog(self):
        """Show dialog with iOS USB tethering instructions"""
        title = _("Using Your iOS Device's Internet on Linux via USB")
        instructions = [
            _("Connect your iOS device to the Linux computer using a USB cable."),
            _("On your iOS device, go to 'Settings', then select 'Personal Hotspot'."),
            _(
                "Enable 'Allow Others to Join'. This may automatically enable 'USB Tethering' if a USB connection is detected."
            ),
        ]
        note = _(
            "This will automatically establish the internet connection on your Linux computer without requiring any additional configuration."
        )
        warning = _(
            "If your iOS device is not connected to Wi-Fi and is using cellular data, this tethering will consume data from your cellular plan. To avoid data charges, ensure that your iOS device is connected to a Wi-Fi network before enabling tethering."
        )

        self._show_dialog(title, instructions, note, warning)

    def _show_dialog(self, title, instructions, note, warning):
        """Create and show a dialog with the given content"""
        # Create a new dialog window
        self.dialog = Adw.Window()
        self.dialog.set_title(title)
        self.dialog.set_default_size(600, -1)  # Width 600, default height
        self.dialog.set_transient_for(self.parent_window)
        self.dialog.set_modal(True)
        self.dialog.set_hide_on_close(True)

        # Create content area with a toolbar view for header
        toolbar_view = Adw.ToolbarView()

        # Add header
        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)

        # Create content area
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        toolbar_view.set_content(content_box)

        # Add intro text
        intro = Gtk.Label(
            label=_(
                "To share your smartphone's internet connection with a Linux computer using a USB cable, follow these steps:"
            )
        )
        intro.set_wrap(True)
        intro.set_xalign(0)
        intro.set_margin_bottom(12)
        content_box.append(intro)

        # Add bullet points
        for instruction in instructions:
            bullet_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            bullet_box.set_margin_start(12)

            bullet = Gtk.Label(label="•")
            bullet.set_xalign(0)
            bullet_box.append(bullet)

            text = Gtk.Label(label=instruction)
            text.set_wrap(True)
            text.set_xalign(0)
            text.set_hexpand(True)
            bullet_box.append(text)

            content_box.append(bullet_box)

        # Add note
        if note:
            note_label = Gtk.Label(label=note)
            note_label.set_wrap(True)
            note_label.set_xalign(0)
            note_label.set_margin_top(12)
            content_box.append(note_label)

        # Add warning with icon
        if warning:
            warning_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            warning_box.set_margin_top(24)

            warning_icon = Gtk.Image.new_from_icon_name("dialog-warning-symbolic")
            warning_box.append(warning_icon)

            warning_text = Gtk.Label(label=warning)
            warning_text.set_wrap(True)
            warning_text.set_xalign(0)
            warning_text.set_hexpand(True)
            warning_text.add_css_class("caption")
            warning_box.append(warning_text)

            content_box.append(warning_box)

        # Add close button
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.set_halign(Gtk.Align.END)
        button_box.set_margin_top(24)

        close_button = Gtk.Button(label=_("Close"))
        close_button.add_css_class("suggested-action")
        close_button.connect("clicked", self._on_close_clicked)
        button_box.append(close_button)

        content_box.append(button_box)

        # Set dialog content and show
        self.dialog.set_content(toolbar_view)
        self.dialog.present()

    def _on_close_clicked(self, button):
        """Handle close button click"""
        if self.dialog:
            self.dialog.close()
