"""
BigControlCenter - Program grid component
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk, Pango


class ProgramGrid(Gtk.Box):
    """Grid view of program entries"""

    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.app = app

        self.set_hexpand(True)
        self.set_vexpand(True)

        # Add CSS for program buttons - remove background and frames
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .program-button {
                background: none;
                border: none;
                box-shadow: none;
                outline: none;
                padding: 8px;
            }
            
            .program-button:hover {
                background-color: alpha(currentColor, 0.08);
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # Create a scrolled window for the grid
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        self.append(scrolled_window)

        # Create a flow box for the program grid
        self.flow_box = Gtk.FlowBox()
        self.flow_box.set_valign(Gtk.Align.START)
        self.flow_box.set_max_children_per_line(20)
        self.flow_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flow_box.set_homogeneous(True)
        self.flow_box.set_min_children_per_line(2)
        self.flow_box.set_column_spacing(12)
        self.flow_box.set_row_spacing(12)
        self.flow_box.set_margin_start(16)
        self.flow_box.set_margin_end(16)
        self.flow_box.set_margin_top(16)
        self.flow_box.set_margin_bottom(16)
        scrolled_window.set_child(self.flow_box)

    def update_grid(self, programs):
        """Update the grid with the given list of programs"""
        # Remove all existing children
        while True:
            child = self.flow_box.get_first_child()
            if child is None:
                break
            self.flow_box.remove(child)

        # Add program buttons
        for program in programs:
            program_button = self._create_program_button(program)
            self.flow_box.append(program_button)

    def _create_program_button(self, program):
        """Create a button for a program"""
        # Create a button
        button = Gtk.Button()
        button.add_css_class("program-button")
        button.connect(
            "clicked", lambda w: self.app.run_program(program.get("app_exec", ""))
        )

        # In GTK4, we need to use motion controller for mouse enter/leave events
        # This will update the status bar instead of showing tooltips
        motion = Gtk.EventControllerMotion.new()
        motion.connect(
            "enter",
            lambda c, x, y: self.app.show_description(
                program.get("app_description", "")
            ),
        )
        motion.connect("leave", lambda c: self.app.hide_description())
        button.add_controller(motion)

        # Create the content box
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        content.set_halign(Gtk.Align.CENTER)
        button.set_child(content)

        # Program icon - set to 64x64 standard size
        icon_file = program.get("app_icon", "")
        if icon_file and icon_file.startswith("/"):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_file, 64, 64)
                icon = Gtk.Picture.new_for_pixbuf(pixbuf)
                icon.set_content_fit(Gtk.ContentFit.SCALE_DOWN)
                icon.set_can_shrink(
                    False
                )  # Prevent icon from becoming smaller than natural size
            except GLib.Error:
                # Fallback to generic icon
                icon = Gtk.Image.new_from_icon_name("application-x-executable")
                icon.set_pixel_size(64)
        else:
            # Use icon name or fallback
            icon_name = icon_file or "application-x-executable"
            icon = Gtk.Image.new_from_icon_name(icon_name)
            icon.set_pixel_size(64)

        content.append(icon)

        # Program name - allow text to wrap when it exceeds the window width
        name_label = Gtk.Label(label=program.get("app_name", ""))
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_max_width_chars(20)  # Increased from 15 to allow longer text
        name_label.set_width_chars(10)  # Set minimum width
        name_label.set_wrap(True)
        name_label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        name_label.set_lines(2)  # Allow up to two lines for wrapped text
        # name_label.set_line_wrap(True)    # This line is causing the error - removed
        # name_label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)  # Not needed in GTK4
        name_label.set_justify(Gtk.Justification.CENTER)
        name_label.add_css_class("program-name")
        content.append(name_label)

        return button
